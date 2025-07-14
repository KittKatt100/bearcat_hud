class BearcatHUD:
    def __init__(self):
        # Placeholder sample data structure
        self.games = {
            "Game 1": {
                "1st Quarter": [{"Play": "Run Left"}, {"Play": "Pass Right"}],
                "2nd Quarter": [{"Play": "QB Sneak"}, {"Play": "Screen Pass"}]
            },
            "Game 2": {
                "1st Quarter": [{"Play": "Run Right"}],
                "2nd Quarter": [{"Play": "Field Goal"}]
            }
        }

    def get_game_list(self):
        return list(self.games.keys())

    def get_quarter_list(self, game):
        return list(self.games[game].keys()) if game in self.games else []

    def get_plays(self, game, quarter):
        return self.games.get(game, {}).get(quarter, [])
