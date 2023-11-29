import time

import requests
from dotenv import dotenv_values
from pymongo import MongoClient


# Can't put myself in map since I'm always the uploader, so I'll always be in.
# This could totally probably be a list but idc anymore
id_map = {
    "76561198104498918": "Calcifer",
    "76561198034834341": "armada",
    "3d10c9ba3d8d499d8002f684299a2259": "MrSaltroll",
    "d7840d81ecec4933ba34e96757cb627b": "LainIwakra",
    "0b1c159f6ba344ed83997df24896876e": "MrSaltea",
    "a5908295a92848d6b1ad7e1ce6556502": "JC11111118",
}

config = dotenv_values(".env")
headers = {
    "Content-Type": "json",
    "Authorization": config["API_KEY"]
}

base_url = "https://ballchasing.com/api"


class ReplayDB:
    def __init__(self):
        self.mongodb_client = MongoClient(host=config["HOSTNAME"],
                                          username=config["USERNAME"],
                                          password=config["PASSWORD"])
        self.database = self.mongodb_client[config["DB_NAME"]]
        self.session = requests.Session()
        self.session.headers.update(headers)
        print("Server version:", self.mongodb_client.server_info()["version"])

    def get_all_replays(self):
        """
        Gets private matches played with Nap Gang!
        """
        replay_list = []
        params = {
            "uploader": "me",
            "playlist": "private",
            "count": 200
        }
        req = requests.Request('GET', base_url + "/replays", params=params)
        while True:
            req.headers = headers
            replay_page = self.session.send(req.prepare()).json()
            replay_list = replay_list + (replay_page["list"])
            if "next" not in replay_page:
                break
            req = requests.Request('GET', replay_page["next"])

        # Filter to the replays we want
        return list(filter(lambda replay: self.is_target_replay(replay), replay_list))

    def is_target_replay(self, replay: dict):
        """
        Checks if replay is needed in the database, properly parsed, and has valid players.
        :param replay: The replay to check
        :return: Whether the replay is one we want
        """
        if self.database["replays"].find_one({"rocket_league_id": replay["rocket_league_id"]}) is not None:
            # Db already has this replay saved
            # print(f"Already have id: {replay['rocket_league_id']}")
            return False

        if "players" not in replay["blue"] or "players" not in replay["orange"]:
            # Bad replay with no players
            return False

        # First loop will pretty much always guarantee the result.
        # Like, why would we all be on orange team? Randos not in the map, on blue?
        for team in ["blue", "orange"]:
            for player in replay[team]["players"]:
                if "id" not in player["id"]:
                    # Replay has bot and I'm ruling out those games
                    return False
                if player["id"]["id"] in id_map.keys():
                    return True
        return False

    def get_replay_details(self):
        replays = self.get_all_replays()
        print(f"Replays to fetch: {len(replays)}")
        for replay in replays:
            print(f"Fetching replay {replay['rocket_league_id']}")
            r = self.session.get(base_url + "/replays/" + replay["id"])

            if r.status_code != 200:
                print(r.json())
                break

            replay_details = r.json()
            # Only return processed replays
            if replay_details["status"] == "ok":
                self.database["replays"].insert_one(replay_details)
            time.sleep(1)


replay_db = ReplayDB()
replay_db.get_replay_details()
print("Replays updated!")
