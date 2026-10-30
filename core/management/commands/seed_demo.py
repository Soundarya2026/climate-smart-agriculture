from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Crop, MarketPrice

class Command(BaseCommand):
    help = "Add sample crops and illustrative market prices."
    def handle(self, *args, **kwargs):
        crops = [
            ("Rice", "Kharif", "clay", 20, 35, 1000),
            ("Millet", "Kharif", "sandy", 20, 40, 250),
            ("Groundnut", "Kharif", "sandy", 20, 35, 400),
            ("Maize", "Kharif/Rabi", "loamy", 18, 32, 500),
            ("Cotton", "Kharif", "black", 21, 35, 500),
            ("Pulses", "Rabi", "loamy", 18, 32, 350),
        ]
        for name, season, soil, tmin, tmax, rain in crops:
            Crop.objects.update_or_create(name=name, defaults={"season":season,"soil_type":soil,"min_temperature":tmin,"max_temperature":tmax,"min_rainfall_mm":rain})
        # Clearly marked demo values; replace with current mandi/API data before production.
        for name, price in [("Rice", 2300), ("Millet", 2800), ("Groundnut", 6200), ("Maize", 2100), ("Cotton", 7000)]:
            MarketPrice.objects.get_or_create(crop_name=name, market="Demo market (sample)", price_per_quintal=price, price_date=timezone.localdate(), source="Illustrative demo data")
        self.stdout.write(self.style.SUCCESS("Demo crops and sample prices added."))
