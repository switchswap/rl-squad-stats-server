player_total_wins_pipeline = [
    {
        '$project': {
            'gameId': '$id',
            'blueTeam': {
                '$setUnion': [
                    '$blue.players.id.id', []
                ]
            },
            'orangeTeam': {
                '$setUnion': [
                    '$orange.players.id.id', []
                ]
            },
            'blueGoals': '$blue.stats.core.goals',
            'orangeGoals': '$orange.stats.core.goals'
        }
    }, {
        '$project': {
            '_id': 0,
            'gameId': 1,
            'blueGoals': 1,
            'orangeGoals': 1,
            'teams': [
                {
                    'teamColor': 'blue',
                    'players': '$blueTeam',
                    'won': {
                        '$gt': [
                            '$blueGoals', '$orangeGoals'
                        ]
                    }
                }, {
                    'teamColor': 'orange',
                    'players': '$orangeTeam',
                    'won': {
                        '$gt': [
                            '$orangeGoals', '$blueGoals'
                        ]
                    }
                }
            ]
        }
    }, {
        '$unwind': '$teams'
    }, {
        '$project': {
            'gameId': 1,
            'players': '$teams.players',
            'won': '$teams.won'
        }
    }, {
        '$unwind': '$players'
    }, {
        '$group': {
            '_id': '$players',
            'totalWins': {
                '$sum': {
                    '$cond': {
                        'if': '$won',
                        'then': 1,
                        'else': 0
                    }
                }
            },
            'totalGames': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'id': '$_id',
            'totalWins': 1,
            'totalGames': 1
        }
    }
]
twos_wins_per_team_pipeline = [
    {
        '$project': {
            'gameId': '$id',
            'blueTeam': {
                '$setUnion': [
                    '$blue.players.id.id', []
                ]
            },
            'orangeTeam': {
                '$setUnion': [
                    '$orange.players.id.id', []
                ]
            },
            'blueGoals': '$blue.stats.core.goals',
            'orangeGoals': '$orange.stats.core.goals'
        }
    }, {
        '$match': {
            '$expr': {
                '$and': [
                    {
                        '$eq': [
                            {
                                '$size': '$blueTeam'
                            }, 2
                        ]
                    }, {
                        '$eq': [
                            {
                                '$size': '$orangeTeam'
                            }, 2
                        ]
                    }
                ]
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'gameId': 1,
            'teams': [
                {
                    'teamColor': 'blue',
                    'players': '$blueTeam',
                    'goalsFor': '$blueGoals',
                    'goalsAgainst': '$orangeGoals'
                }, {
                    'teamColor': 'orange',
                    'players': '$orangeTeam',
                    'goalsFor': '$orangeGoals',
                    'goalsAgainst': '$blueGoals'
                }
            ]
        }
    }, {
        '$unwind': '$teams'
    }, {
        '$project': {
            'gameId': 1,
            'team': {
                '$setUnion': [
                    '$teams.players', []
                ]
            },
            'teamColor': '$teams.teamColor',
            'won': {
                '$gt': [
                    '$teams.goalsFor', '$teams.goalsAgainst'
                ]
            }
        }
    }, {
        '$group': {
            '_id': '$team',
            'totalWins': {
                '$sum': {
                    '$cond': {
                        'if': '$won',
                        'then': 1,
                        'else': 0
                    }
                }
            },
            'totalGames': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            '_id': 1
        }
    }, {
        '$project': {
            '_id': 0,
            'players': '$_id',
            'totalWins': 1,
            'totalGames': 1
        }
    }
]
threes_wins_per_team_pipeline = [
    {
        '$project': {
            'gameId': '$id',
            'blueTeam': {
                '$setUnion': [
                    '$blue.players.id.id', []
                ]
            },
            'orangeTeam': {
                '$setUnion': [
                    '$orange.players.id.id', []
                ]
            },
            'blueGoals': '$blue.stats.core.goals',
            'orangeGoals': '$orange.stats.core.goals'
        }
    }, {
        '$match': {
            '$expr': {
                '$and': [
                    {
                        '$eq': [
                            {
                                '$size': '$blueTeam'
                            }, 3
                        ]
                    }, {
                        '$eq': [
                            {
                                '$size': '$orangeTeam'
                            }, 3
                        ]
                    }
                ]
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'gameId': 1,
            'teams': [
                {
                    'teamColor': 'blue',
                    'players': '$blueTeam',
                    'goalsFor': '$blueGoals',
                    'goalsAgainst': '$orangeGoals'
                }, {
                    'teamColor': 'orange',
                    'players': '$orangeTeam',
                    'goalsFor': '$orangeGoals',
                    'goalsAgainst': '$blueGoals'
                }
            ]
        }
    }, {
        '$unwind': '$teams'
    }, {
        '$project': {
            'gameId': 1,
            'team': {
                '$setUnion': [
                    '$teams.players', []
                ]
            },
            'teamColor': '$teams.teamColor',
            'won': {
                '$gt': [
                    '$teams.goalsFor', '$teams.goalsAgainst'
                ]
            }
        }
    }, {
        '$group': {
            '_id': '$team',
            'totalWins': {
                '$sum': {
                    '$cond': {
                        'if': '$won',
                        'then': 1,
                        'else': 0
                    }
                }
            },
            'totalGames': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            '_id': 1
        }
    }, {
        '$project': {
            '_id': 0,
            'players': '$_id',
            'totalWins': 1,
            'totalGames': 1
        }
    }
]
player_stats_pipeline = [
    {
        '$project': {
            'players': {
                '$setUnion': [
                    '$orange.players', '$blue.players'
                ]
            }
        }
    }, {
        '$unwind': '$players'
    }, {
        '$project': {
            'playerName': '$players.name',
            'platform': '$players.id.platform',
            'playerId': '$players.id.id',
            'goals': '$players.stats.core.goals',
            'assists': '$players.stats.core.assists',
            'saves': '$players.stats.core.saves',
            'score': '$players.stats.core.score',
            'shots': '$players.stats.core.shots',
            'demosFor': '$players.stats.demo.inflicted',
            'demosAgainst': '$players.stats.demo.taken',
            'gamesPlayed': 1
        }
    }, {
        '$group': {
            '_id': '$playerId',
            'platform': {
                '$first': '$platform'
            },
            'playerName': {
                '$first': '$playerName'
            },
            'totalGames': {
                '$sum': 1
            },
            'totalGoals': {
                '$sum': '$goals'
            },
            'totalAssists': {
                '$sum': '$assists'
            },
            'totalSaves': {
                '$sum': '$saves'
            },
            'totalScore': {
                '$sum': '$score'
            },
            'totalShots': {
                '$sum': '$shots'
            },
            'totalDemosFor': {
                '$sum': '$demosFor'
            },
            'totalDemosAgainst': {
                '$sum': '$demosAgainst'
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'playerName': 1,
            'platform': 1,
            'playerId': '$_id',
            'totalGames': '$totalGames',
            'totalGoals': '$totalGoals',
            'totalAssists': '$totalAssists',
            'totalSaves': '$totalSaves',
            'totalScore': '$totalScore',
            'totalShots': '$totalShots',
            'totalDemosFor': '$totalDemosFor',
            'totalDemosAgainst': '$totalDemosAgainst'
        }
    }
]


def match_history_pipeline(ids: list[str]):
    history_pipeline = [
        {
            '$match': {
                '$or': [
                    {
                        'blue.players.id.id': {
                            '$all': ids
                        }
                    }, {
                        'orange.players.id.id': {
                            '$all': ids
                        }
                    }
                ]
            }
        }, {
            '$project': {
                '_id': 0,
                'id': 1,
                'link': 1,
                'map_code': 1,
                'map_name': 1,
                'duration': 1,
                'overtime': 1,
                'overtime_seconds': 1,
                'date': 1,
                'date_has_timezone': 1,
                'blue': {
                    'players': {
                        '$map': {
                            'input': '$blue.players',
                            'as': 'player',
                            'in': {
                                'id': '$$player.id.id',
                                'platform': '$$player.id.platform',
                                'name': '$$player.name',
                                'car_id': '$$player.car_id',
                                'car_name': '$$player.car_name',
                                'stats': '$$player.stats'
                            }
                        }
                    },
                    'stats': 1,
                    'name': 1
                },
                'orange': {
                    'players': {
                        '$map': {
                            'input': '$orange.players',
                            'as': 'player',
                            'in': {
                                'id': '$$player.id.id',
                                'platform': '$$player.id.platform',
                                'name': '$$player.name',
                                'car_id': '$$player.car_id',
                                'car_name': '$$player.car_name',
                                'stats': '$$player.stats'
                            }
                        }
                    },
                    'stats': 1,
                    'name': 1
                }
            }
        }
    ]
    # This looks horrendous. There must have been a better way.
    # Make sure matches are symmetrical for non-individual lookups.
    if len(ids) is not 1:
        history_pipeline.insert(1,
                                {
                                    '$match': {
                                        '$and': [
                                            {
                                                'blue.players': {
                                                    '$size': len(ids)
                                                }
                                            }, {
                                                'orange.players': {
                                                    '$size': len(ids)
                                                }
                                            }
                                        ]
                                    }
                                }
                                )
    return history_pipeline
