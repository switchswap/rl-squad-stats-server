from typing import List, Optional

from pydantic import BaseModel


class Uploader(BaseModel):
    steam_id: str
    name: str
    profile_url: str
    avatar: str


class PlayerCore(BaseModel):
    shots: int
    shots_against: int
    goals: int
    goals_against: int
    saves: int
    assists: int
    score: int
    mvp: bool
    shooting_percentage: float


class PlayerBoost(BaseModel):
    bpm: int
    bcpm: float
    avg_amount: float
    amount_collected: int
    amount_stolen: int
    amount_collected_big: int
    amount_stolen_big: int
    amount_collected_small: int
    amount_stolen_small: int
    count_collected_big: int
    count_stolen_big: int
    count_collected_small: int
    count_stolen_small: int
    amount_overfill: int
    amount_overfill_stolen: int
    amount_used_while_supersonic: int
    time_zero_boost: float
    percent_zero_boost: float
    time_full_boost: float
    percent_full_boost: float
    time_boost_0_25: float
    time_boost_25_50: float
    time_boost_50_75: float
    time_boost_75_100: float
    percent_boost_0_25: float
    percent_boost_25_50: float
    percent_boost_50_75: float
    percent_boost_75_100: float


class PlayerMovement(BaseModel):
    avg_speed: int
    total_distance: int
    time_supersonic_speed: float
    time_boost_speed: float
    time_slow_speed: float
    time_ground: float
    time_low_air: float
    time_high_air: float
    time_powerslide: float
    count_powerslide: int
    avg_powerslide_duration: float
    avg_speed_percentage: float
    percent_slow_speed: float
    percent_boost_speed: float
    percent_supersonic_speed: float
    percent_ground: float
    percent_low_air: float
    percent_high_air: float


class PlayerPositioning(BaseModel):
    avg_distance_to_ball: int
    avg_distance_to_ball_possession: int
    avg_distance_to_ball_no_possession: int
    avg_distance_to_mates: Optional[int] = None  # Looks like a new field from the API
    time_defensive_third: float
    time_neutral_third: float
    time_offensive_third: float
    time_defensive_half: float
    time_offensive_half: float
    time_behind_ball: float
    time_infront_ball: float
    time_most_back: float
    time_most_forward: Optional[float] = 0
    goals_against_while_last_defender: Optional[int] = 0  # Dunno why the API doesn't just default this to 0
    time_closest_to_ball: float
    time_farthest_from_ball: float
    percent_defensive_third: float
    percent_offensive_third: float
    percent_neutral_third: float
    percent_defensive_half: float
    percent_offensive_half: float
    percent_behind_ball: float
    percent_infront_ball: float
    percent_most_back: float
    percent_most_forward: Optional[float] = 0
    percent_closest_to_ball: float
    percent_farthest_from_ball: float


class Demo(BaseModel):
    inflicted: int
    taken: int


class PlayerStats(BaseModel):
    core: PlayerCore
    boost: PlayerBoost
    movement: PlayerMovement
    positioning: PlayerPositioning
    demo: Demo


class Ball(BaseModel):
    possession_time: Optional[float] = 0
    time_in_side: Optional[float] = 0


class TeamCore(BaseModel):
    shots: int
    shots_against: int
    goals: int
    goals_against: int
    saves: int
    assists: int
    score: int
    shooting_percentage: float


class TeamBoost(BaseModel):
    bpm: int
    bcpm: float
    avg_amount: float
    amount_collected: int
    amount_stolen: int
    amount_collected_big: int
    amount_stolen_big: int
    amount_collected_small: int
    amount_stolen_small: int
    count_collected_big: int
    count_stolen_big: int
    count_collected_small: int
    count_stolen_small: int
    amount_overfill: int
    amount_overfill_stolen: int
    amount_used_while_supersonic: int
    time_zero_boost: float
    time_full_boost: float
    time_boost_0_25: float
    time_boost_25_50: float
    time_boost_50_75: float
    time_boost_75_100: float


class TeamMovement(BaseModel):
    total_distance: int
    time_supersonic_speed: float
    time_boost_speed: float
    time_slow_speed: float
    time_ground: float
    time_low_air: float
    time_high_air: float
    time_powerslide: float
    count_powerslide: int


class TeamPositioning(BaseModel):
    time_defensive_third: float
    time_neutral_third: float
    time_offensive_third: float
    time_defensive_half: float
    time_offensive_half: float
    time_behind_ball: float
    time_infront_ball: float


class TeamStats(BaseModel):
    ball: Ball
    core: TeamCore
    boost: TeamBoost
    positioning: TeamPositioning
    demo: Demo


class Id(BaseModel):
    platform: str
    id: str


class Camera(BaseModel):
    fov: int
    height: int
    pitch: int
    distance: int
    stiffness: float
    swivel_speed: float
    transition_speed: float


class Player(BaseModel):
    start_time: float
    end_time: float
    name: str
    id: Id
    car_id: int
    car_name: Optional[str] = None
    camera: Camera
    steering_sensitivity: float
    stats: PlayerStats


class Team(BaseModel):
    color: str
    players: List[Player]
    stats: TeamStats


class Replay(BaseModel):
    id: str
    link: str
    created: str
    uploader: Uploader
    status: str
    rocket_league_id: str
    match_guid: str
    title: str
    map_code: str
    match_type: str
    team_size: int
    playlist_id: str
    duration: int
    overtime: bool
    overtime_seconds: Optional[int] = None
    season: int
    season_type: str
    date: str
    date_has_timezone: bool
    visibility: str
    blue: Team
    orange: Team
    playlist_name: str
    map_name: str
