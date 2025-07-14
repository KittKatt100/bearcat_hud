def generate_team_analysis(school_data: dict) -> str:
    return f"""
### I. Opponent Identity
- **School:** {school_data['school_name']}
- **County:** {school_data['county']} County
- **State:** {school_data['state']}
- **Classification:** {school_data.get('classification', 'Unknown')}
- **Record:** {school_data.get('record', 'N/A')}
- **Region Standing:** {school_data.get('region_standing', 'N/A')}
- **Recent Trends:** {school_data.get('recent_trends', 'No data available')}

### II. Offensive Philosophy Summary
- **Run-Pass Balance:** Placeholder
- **Tempo/Rhythm:** Placeholder
- **Playcalling Style:** Placeholder
- **Use of Motion/Shifts:** Placeholder

### III. Quarterback Profile
- **Tools/Skills:** Placeholder
- **Progression Tendencies:** Placeholder
- **Scramble Rate:** Placeholder
- **Clutch Behavior:** Placeholder

### IV. Offensive Line Evaluation
- **Average Size:** Placeholder
- **Protection Bias:** Placeholder
- **Pull/Zone Frequency:** Placeholder
- **Combo Blocks:** Placeholder

### V. Skill Player Impact Review
- **Top 3 Threats:** Placeholder
- **Alignment/Motion Patterns:** Placeholder
- **Yards After Contact:** Placeholder
- **WR Route Trees:** Placeholder

### VI. Formational DNA
- **Most Used Sets:** Placeholder
- **Red Zone Formations:** Placeholder
- **Disguise Frequency:** Placeholder

### VII. Scoring Patterns & Game Flow
- **Points by Quarter:** Placeholder
- **Early Game Behavior:** Placeholder
- **Red Zone Score %:** Placeholder
- **2pt Conversion History:** Placeholder

### VIII. Situational Awareness
- **3rd Down Tendencies:** Placeholder
- **4th Down Aggression:** Placeholder
- **2-Minute Drill:** Placeholder

### IX. Psychological/Culture Profile
- **Penalty Rate/Emotion:** Placeholder
- **Coach Style:** Placeholder
- **Bounce-Back Rating:** Placeholder
- **Team Grit:** Placeholder

### X. Tells and Tactical Cues
- **Pre-Snap Indicators:** Placeholder
- **OL Stance/Depth Hints:** Placeholder
- **QB Behavior Patterns:** Placeholder
- **RB Alignment Cues:** Placeholder

---
_This analysis will auto-expand with tactical overlays, matchup flags, and defensive counter notes as more data is compiled._
"""
