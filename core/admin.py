from django.contrib import admin
from .models import FarmerProfile, Crop, Farm, SoilReading, MarketPrice, DiseaseReport, Notification

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "village", "district", "farm_size_acres")
    search_fields = ("user__username", "phone", "district")
@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ("name", "season", "soil_type")
    search_fields = ("name",)
@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("name", "farmer", "area_acres", "soil_type")
    list_filter = ("soil_type",)
@admin.register(SoilReading)
class SoilReadingAdmin(admin.ModelAdmin):
    list_display = ("farmer", "moisture_percent", "ph", "temperature_c", "recorded_at")
    list_filter = ("recorded_at",)
@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ("crop_name", "market", "price_per_quintal", "price_date")
    list_filter = ("price_date",)
@admin.register(DiseaseReport)
class DiseaseReportAdmin(admin.ModelAdmin):
    list_display = ("farmer", "crop_name", "result", "created_at")
    list_filter = ("created_at",)
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_read", "created_at")
