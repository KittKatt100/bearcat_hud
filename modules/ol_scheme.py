def analyze_ol(opponent):
    school = opponent.get("school", "Unknown Team")
    return (
        f"[Offensive Line Scheme Recognition] report for {school}:\n"
        f"- Zone blocking in inside run on early downs\n"
        f"- Heavy pulls from LG in short yardage\n"
        f"- Back-heavy stance = pass indicator on film\n"
    )
