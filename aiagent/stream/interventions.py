def generate_intervention(district_name, metric, value):
    """Return a simple intervention suggestion."""
    if value is None:
        return "No data available for this metric."

    if metric == "Mean Temperature":
        if value > 40:
            return f"Extreme heat: Provide cooling centers in {district_name}."
        elif value > 35:
            return f"High heat: Plant shade trees in {district_name}."
        else:
            return f"Moderate heat: Encourage water access in {district_name}."

    elif metric == "Population Density":
        if value > 10000:
            return f"High density: Expand public spaces in {district_name}."
        else:
            return f"Moderate density: Monitor population growth in {district_name}."

    elif metric == "NDVI":
        if value < 0.2:
            return f"Low vegetation: Plant more greenery in {district_name}."
        else:
            return f"Vegetation adequate in {district_name}."
