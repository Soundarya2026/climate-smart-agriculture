import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import RegisterForm, FarmForm, SoilReadingForm, DiseaseReportForm
from .models import Farm, SoilReading, MarketPrice, DiseaseReport, Crop, Notification
from .recommendations import recommend_crops

def home(request):
    return render(request, "core/home.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your farmer account has been created.")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "core/register.html", {"form": form})

@login_required
def dashboard(request):
    farms = Farm.objects.filter(farmer=request.user)
    readings = SoilReading.objects.filter(farmer=request.user)[:5]
    prices = MarketPrice.objects.all()[:6]
    reports = DiseaseReport.objects.filter(farmer=request.user)[:5]
    notifications = Notification.objects.filter(user__in=[request.user, None])[:5]
    latest = readings.first()
    return render(request, "core/dashboard.html", {
        "farms": farms, "readings": readings, "prices": prices, "reports": reports,
        "notifications": notifications, "latest": latest,
        "farm_count": farms.count(), "report_count": DiseaseReport.objects.filter(farmer=request.user).count()
    })

@login_required
def farms(request):
    if request.method == "POST":
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False); farm.farmer = request.user; farm.save()
            messages.success(request, "Farm added.")
            return redirect("farms")
    else: form = FarmForm()
    return render(request, "core/farms.html", {"form": form, "farms": Farm.objects.filter(farmer=request.user)})

@login_required
def soil(request):
    if request.method == "POST":
        form = SoilReadingForm(request.POST, user=request.user)
        if form.is_valid():
            reading = form.save(commit=False); reading.farmer = request.user; reading.save()
            messages.success(request, "Soil reading saved.")
            return redirect("soil")
    else: form = SoilReadingForm(user=request.user)
    return render(request, "core/soil.html", {"form": form, "readings": SoilReading.objects.filter(farmer=request.user)[:30]})

@login_required
def crop_recommendation(request):
    result = None
    if request.method == "POST":
        try:
            ph = float(request.POST.get("ph") or 6.5)
            moisture = float(request.POST.get("moisture") or 50)
            temperature = float(request.POST.get("temperature") or 28)
            rainfall = float(request.POST.get("rainfall") or 600)
            soil_type = request.POST.get("soil_type", "")
            result = recommend_crops(ph, moisture, temperature, rainfall, soil_type)
        except ValueError:
            messages.error(request, "Please enter valid numeric values.")
    return render(request, "core/recommend.html", {"result": result})

@login_required
def weather(request):
    city = request.GET.get("city", "Chennai")
    data, error = None, None
    api_key = __import__("os").environ.get("OPENWEATHER_API_KEY")
    if api_key:
        try:
            response = requests.get("https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": api_key, "units": "metric"}, timeout=8)
            response.raise_for_status()
            raw = response.json()
            data = {"city": raw["name"], "temperature": raw["main"]["temp"],
                    "humidity": raw["main"]["humidity"], "description": raw["weather"][0]["description"]}
        except requests.RequestException:
            error = "Weather service is unavailable. Check your API key or connection."
    else:
        error = "Add OPENWEATHER_API_KEY to your environment to enable live weather."
    return render(request, "core/weather.html", {"city": city, "data": data, "error": error})

@login_required
def disease(request):
    if request.method == "POST":
        form = DiseaseReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False); report.farmer = request.user
            report.result = "Pending review"
            report.advice = "This starter app stores the image and symptoms; it does not diagnose disease. Consult an agricultural extension officer."
            report.save()
            messages.success(request, "Image submitted. No automated diagnosis has been performed.")
            return redirect("disease")
    else: form = DiseaseReportForm()
    return render(request, "core/disease.html", {"form": form, "reports": DiseaseReport.objects.filter(farmer=request.user)})

@login_required
def market(request):
    prices = MarketPrice.objects.all()
    query = request.GET.get("q", "")
    if query: prices = prices.filter(crop_name__icontains=query)
    return render(request, "core/market.html", {"prices": prices[:100], "query": query})

def admin_required(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    context = {
        "farmer_count": User.objects.filter(is_staff=False, is_superuser=False).count(),
        "farm_count": Farm.objects.count(), "reading_count": SoilReading.objects.count(),
        "report_count": DiseaseReport.objects.count(), "recent_farmers": User.objects.order_by("-date_joined")[:8],
        "recent_reports": DiseaseReport.objects.select_related("farmer")[:8],
        "crop_count": Crop.objects.count(), "price_count": MarketPrice.objects.count()
    }
    return render(request, "core/admin_dashboard.html", context)

@login_required
@user_passes_test(admin_required)
def admin_farmers(request):
    users = User.objects.filter(is_staff=False, is_superuser=False).order_by("-date_joined")
    return render(request, "core/admin_farmers.html", {"users": users})

@login_required
@user_passes_test(admin_required)
def admin_reports(request):
    reports = DiseaseReport.objects.select_related("farmer").all()
    return render(request, "core/admin_reports.html", {"reports": reports})
