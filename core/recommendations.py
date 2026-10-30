# Transparent starter rules. Replace with a validated ML model when you have local farm data.
from .models import Crop

def recommend_crops(ph, moisture, temperature, rainfall, soil_type=""):
    crops = list(Crop.objects.all())
    if not crops:
        crops = [
            type("C", (), {"name":"Rice", "min_temperature":20, "max_temperature":35, "min_rainfall_mm":1000, "soil_type":"clay"})(),
            type("C", (), {"name":"Millet", "min_temperature":20, "max_temperature":40, "min_rainfall_mm":250, "soil_type":"sandy"})(),
            type("C", (), {"name":"Groundnut", "min_temperature":20, "max_temperature":35, "min_rainfall_mm":400, "soil_type":"sandy"})(),
            type("C", (), {"name":"Maize", "min_temperature":18, "max_temperature":32, "min_rainfall_mm":500, "soil_type":"loamy"})(),
            type("C", (), {"name":"Cotton", "min_temperature":21, "max_temperature":35, "min_rainfall_mm":500, "soil_type":"black"})(),
        ]
    ranked = []
    for crop in crops:
        score = 0
        score += 2 if crop.min_temperature <= temperature <= crop.max_temperature else 0
        score += 2 if rainfall >= crop.min_rainfall_mm else 0
        if soil_type and crop.soil_type and soil_type.lower() in crop.soil_type.lower():
            score += 2
        if ph is not None and 5.5 <= ph <= 7.5:
            score += 1
        if moisture is not None and 20 <= moisture <= 80:
            score += 1
        ranked.append((score, crop.name))
    return [name for _, name in sorted(ranked, reverse=True)[:3]]
