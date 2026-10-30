from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import FarmerProfile, Farm, SoilReading, DiseaseReport

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)
    village = forms.CharField(required=False)
    district = forms.CharField(required=False)
    farm_size_acres = forms.DecimalField(required=False, min_value=0, decimal_places=2)
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone", "village", "district", "farm_size_acres", "password1", "password2")
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            FarmerProfile.objects.create(
                user=user, phone=self.cleaned_data.get("phone", ""),
                village=self.cleaned_data.get("village", ""),
                district=self.cleaned_data.get("district", ""),
                farm_size_acres=self.cleaned_data.get("farm_size_acres") or 0
            )
        return user

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ["name", "location", "area_acres", "soil_type"]

class SoilReadingForm(forms.ModelForm):
    class Meta:
        model = SoilReading
        fields = ["farm", "moisture_percent", "ph", "temperature_c", "nitrogen", "phosphorus", "potassium", "notes"]
        widgets = {"notes": forms.TextInput(attrs={"placeholder": "Optional notes"})}
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["farm"].queryset = Farm.objects.filter(farmer=self.user)

class DiseaseReportForm(forms.ModelForm):
    class Meta:
        model = DiseaseReport
        fields = ["crop_name", "image", "symptoms"]
