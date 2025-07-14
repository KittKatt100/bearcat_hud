import pandas as pd

class BearcatHUD:
    def __init__(self):
        try:
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
        except Exception as e:
            print("❌ Error setting up BearcatHUD:", e)
            self.games = {}

    def get_game_list(self):
        return list(self.games.keys())

    def get_quarters(self, game):
        cleaned_game = game.strip()
        if cleaned_game not in self.games:
            print(f"⚠️ Game '{cleaned_game}' not found in available games: {list(self.games.keys())}")
            return []
        return list(self.games[cleaned_game].keys())

    def get_plays(self, game, quarter):
        plays = self.games.get(game, {}).get(quarter, [])
        return pd.DataFrame(plays)
