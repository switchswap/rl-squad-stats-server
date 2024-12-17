import os
import schedule
import time
import logging
import requests
from pymongo import MongoClient

# Can't put myself in map since I'm always the uploader, so I'll always be in.
# This could totally probably be a list but idc anymore
ID_MAP = {
    "76561198104498918": "Calcifer",
    "76561198034834341": "armada",
    "3d10c9ba3d8d499d8002f684299a2259": "MrSaltroll",
    "d7840d81ecec4933ba34e96757cb627b": "LainIwakra",
    "0b1c159f6ba344ed83997df24896876e": "MrSaltea",
    "a5908295a92848d6b1ad7e1ce6556502": "JC11111118",
}

HEADERS = {
    "Content-Type": "json",
    "Authorization": os.environ["API_KEY"]
}

BASE_URL = "https://ballchasing.com/api"


class ReplayDB:
    def __init__(self):
        self.mongodb_client = MongoClient(host=os.environ["HOSTNAME"],
                                          username=os.environ["USERNAME"],
                                          password=os.environ["PASSWORD"])
        self.database = self.mongodb_client[os.environ["DB_NAME"]]
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.logger = logging.getLogger('replay_db')
        self.logger.info(f"Server version: {self.mongodb_client.server_info()['version']}")

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
        req = requests.Request('GET', BASE_URL + "/replays", params=params)
        while True:
            req.headers = HEADERS
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
            self.logger.debug(f"Already in db, id = {replay['rocket_league_id']}")
            return False

        if "players" not in replay["blue"] or "players" not in replay["orange"]:
            self.logger.debug(f"Bad replay with no players, id = {replay['rocket_league_id']}")
            # Bad replay with no players
            return False

        # First loop will pretty much always guarantee the result.
        # Like, why would we all be on orange team? Randos not in the map, on blue?
        for team in ["blue", "orange"]:
            for player in replay[team]["players"]:
                if "id" not in player["id"]:
                    # Replay has bot and I'm ruling out those games
                    return False
                if player["id"]["id"] in ID_MAP.keys():
                    return True
        return False

    def get_replay_details(self):
        self.logger.info("Updating replays...")
        replays = self.get_all_replays()
        self.logger.info(f"Replays to fetch: {len(replays)}")
        for replay in replays:
            self.logger.debug(f"Fetching replay {replay['rocket_league_id']}")
            r = self.session.get(BASE_URL + "/replays/" + replay["id"])

            if r.status_code != 200:
                self.logger.error(f"Received status {r.status_code}")
                self.logger.error(r.json())
                break

            replay_details = r.json()
            # Only return processed replays
            if replay_details["status"] == "ok":
                self.database["replays"].insert_one(replay_details)
            else:
                self.logger.error(f"Replay status for id = {replay_details['id']}  was {replay_details['status']}")
            time.sleep(1)
        self.logger.info("Replays updated!")

    def set_last_updated_time(self):
        """
        Sets the last updated time in the database to the current time.
        This should be called after the replays are freshly updated.
        """
        self.logger.info("Setting last update time...")
        current_timestamp = time.time_ns()
        update = {"$set": {"lastUpdatedTimestamp": time.time_ns()}}
        self.database["info"].update_one(filter={}, update=update, upsert=True)
        self.logger.info(f"Set last update time: {current_timestamp}.")


if __name__ == '__main__':
    logging.basicConfig()
    # Enable schedule logs
    logging.getLogger('schedule').setLevel(level=logging.DEBUG)
    # Enable replay_db logs
    logging.getLogger('replay_db').setLevel(level=logging.DEBUG)

    replay_db = ReplayDB()


    def update_replays():
        replay_db.get_replay_details()
        replay_db.set_last_updated_time()


    schedule.every().day.at("02:00").do(update_replays)
    while True:
        schedule.run_pending()
        time.sleep(1)
