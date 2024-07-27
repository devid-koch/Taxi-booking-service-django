from django import forms
from .models import PricingConfig, DayPricingConfig

class PricingConfigForm(forms.ModelForm):
    class Meta:
        model = PricingConfig
        fields = ['name', 'is_active']

class DayPricingConfigForm(forms.ModelForm):
    class Meta:
        model = DayPricingConfig
        fields = ['day_of_week', 'base_price', 'base_distance_upto_km', 'additional_price_per_km', 'time_multiplier_factor', 'waiting_charges']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['day_of_week'].widget.attrs.update({'class': 'form-control'})
        self.fields['base_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['base_distance_upto_km'].widget.attrs.update({'class': 'form-control'})
        self.fields['additional_price_per_km'].widget.attrs.update({'class': 'form-control'})
        self.fields['time_multiplier_factor'].widget.attrs.update({'class': 'form-control'})
        self.fields['waiting_charges'].widget.attrs.update({'class': 'form-control'})
