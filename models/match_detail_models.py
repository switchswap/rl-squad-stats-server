from typing import Optional, Annotated

from pydantic import BaseModel, BeforeValidator, Field

from models.base_models import TeamStats, PlayerStats


class Player(BaseModel):
    id: str
    platform: str
    name: str
    car_id: int
    car_name: Optional[str] = None
    stats: PlayerStats


class TeamDetails(BaseModel):
    name: Optional[str] = None
    stats: TeamStats
    players: list[Player]


class MatchDetails(BaseModel):
    id: str
    link: str
    map_code: str
    duration: int
    overtime: bool
    overtime_seconds: Optional[int] = None
    date: str
    date_has_timezone: bool
    map_name: str
    blue: TeamDetails
    orange: TeamDetails
