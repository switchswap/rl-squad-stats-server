from fastapi import APIRouter, Request
import mongo_queries

router = APIRouter()


@router.get("/wins/individual", response_description="List individual player wins")
def get_player_wins(request: Request):
    wins_table = list(request.app.database["replays"].aggregate(mongo_queries.player_total_wins_pipeline))
    return wins_table


@router.get("/wins/2s", response_description="List 2s team wins")
def get_2s_wins(request: Request):
    wins_table = list(request.app.database["replays"].aggregate(mongo_queries.twos_wins_per_team_pipeline))
    return wins_table


@router.get("/wins/3s", response_description="List 3s team wins")
def get_3s_wins(request: Request):
    wins_table = list(request.app.database["replays"].aggregate(mongo_queries.threes_wins_per_team_pipeline))
    return wins_table


@router.get("/details", response_description="List all player details")
def get_player_details(request: Request):
    player_details = list(request.app.database["replays"].aggregate(mongo_queries.player_stats_pipeline))
    return player_details


@router.get("/count", response_description="Get total matches played")
def get_total_match_count(request: Request):
    return {
        "count": request.app.database["replays"].count_documents({})
    }
