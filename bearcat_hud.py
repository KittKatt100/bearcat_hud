class BearcatHUD:
    def __init__(self):
        self.opponent = None
        self.modules = self.get_modules()

    def get_modules(self):
        return [
            "Quarterback Targeting",
            "Offensive Line Scheme Recognition"
        ]

    def set_opponent(self, school, county, state):
        self.opponent = {
            "school": school,
            "county": county,
            "state": state
        }

    def run_module(self, module_name):
        if module_name == "Quarterback Targeting":
            from modules.quarterback_targeting import analyze_qb
            return analyze_qb(self.opponent)
        elif module_name == "Offensive Line Scheme Recognition":
            from modules.ol_scheme import analyze_ol
            return analyze_ol(self.opponent)
        else:
            return f"Module '{module_name}' not found."

    def identify_tells(self, play):
        tells = []
        if play.get("OL_pad_level") == "low": tells.append("Run likely")
        if play.get("QB_eyes") == "deep right": tells.append("Vertical or boundary throw")
        if play.get("motion") == "fast jet": tells.append("Jet sweep or play-action")
        if play.get("alignment") == "tight split twins": tells.append("Crack toss or iso")
        if play.get("OL_weight_distribution") == "back-heavy": tells.append("Pass set coming")
        return tells
