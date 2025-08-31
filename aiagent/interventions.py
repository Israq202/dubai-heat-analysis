def generate_intervention(district_name, mean_temp):
    # Simple rule-based intervention for now
    if mean_temp is None:
        return "No data"
    if mean_temp >= 40:
        return f"Install cooling centers in {district_name} and plant shade trees."
    elif mean_temp >= 35:
        return f"Encourage water spraying and increase vegetation in {district_name}."
    else:
        return f"No urgent intervention required in {district_name}."

