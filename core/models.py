from django.db import models
from django.contrib.auth.models import User

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="farmer_profile")
    phone = models.CharField(max_length=20, blank=True)
    village = models.CharField(max_length=120, blank=True)
    district = models.CharField(max_length=120, blank=True)
    farm_size_acres = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    preferred_language = models.CharField(max_length=40, default="English")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    season = models.CharField(max_length=80, blank=True)
    soil_type = models.CharField(max_length=120, blank=True)
    min_temperature = models.FloatField(default=18)
    max_temperature = models.FloatField(default=35)
    min_rainfall_mm = models.FloatField(default=300)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Farm(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="farms")
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=200, blank=True)
    area_acres = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    soil_type = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} ({self.farmer.username})"

class SoilReading(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="soil_readings")
    farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True, blank=True)
    moisture_percent = models.FloatField()
    ph = models.FloatField(null=True, blank=True)
    temperature_c = models.FloatField(null=True, blank=True)
    nitrogen = models.FloatField(null=True, blank=True)
    phosphorus = models.FloatField(null=True, blank=True)
    potassium = models.FloatField(null=True, blank=True)
    notes = models.CharField(max_length=250, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-recorded_at"]

class MarketPrice(models.Model):
    crop_name = models.CharField(max_length=100)
    market = models.CharField(max_length=120, default="Local market")
    price_per_quintal = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=30, default="INR/quintal")
    price_date = models.DateField()
    source = models.CharField(max_length=200, blank=True)
    class Meta:
        ordering = ["-price_date", "crop_name"]

class DiseaseReport(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="disease_uploads/")
    symptoms = models.TextField(blank=True)
    result = models.CharField(max_length=200, blank=True)
    advice = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=160)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
