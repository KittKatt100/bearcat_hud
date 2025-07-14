def analyze_qb(opponent):
    school = opponent.get("school", "Unknown Team")
    return (
        f"[Quarterback Targeting] report for {school}:\n"
        f"- QB favors boundary throws when under pressure\n"
        f"- High % of targets go to slot on 3rd downs\n"
        f"- Tendency to stare down first read vs. zone coverage\n"
    )
