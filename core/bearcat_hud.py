import pandas as pd

class BearcatHUD:
    def __init__(self):
        # Mock data for testing without file dependencies
        self.games = {
            "Game 1": {
                "Q1": [
                    {"play": "Run Left", "yards": 5},
                    {"play": "Pass Right", "yards": 12}
                ],
                "Q2": [
                    {"play": "Run Center", "yards": 3},
                    {"play": "Pass Deep", "yards": 25}
                ]
            },
            "Game 2": {
                "Q1": [
                    {"play": "Run Right", "yards": 7},
                    {"play": "Pass Left", "yards": 8}
                ],
                "Q2": [
                    {"play": "Pass Short", "yards": 4},
                    {"play": "Run Sweep", "yards": 9}
                ]
            }
        }

    def get_game_list(self):
        return list(self.games.keys())

    def get_quarters(self, game):
        return list(self.games.get(game, {}).keys())

    def get_plays(self, game, quarter):
        plays = self.games.get(game, {}).get(quarter, [])
        return pd.DataFrame(plays)
