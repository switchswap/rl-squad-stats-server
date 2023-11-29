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
