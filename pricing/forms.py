from django import forms
from django.core.exceptions import ValidationError
from .models import PricingConfig, DayPricingConfig

class PricingConfigForm(forms.ModelForm):
    class Meta:
        model = PricingConfig
        fields = ['name', 'is_active']

class DayPricingConfigForm(forms.ModelForm):
    class Meta:
        model = DayPricingConfig
        fields = '__all__'
        widgets = {
            'day_of_week': forms.Select(choices=[
                ('Mon', 'Monday'),
                ('Tue', 'Tuesday'),
                ('Wed', 'Wednesday'),
                ('Thu', 'Thursday'),
                ('Fri', 'Friday'),
                ('Sat', 'Saturday'),
                ('Sun', 'Sunday')
            ])
        }

    def clean_day_of_week(self):
        day_of_week = self.cleaned_data.get('day_of_week')
        pricing_config = self.cleaned_data.get('pricing_config')

        if DayPricingConfig.objects.filter(pricing_config=pricing_config, day_of_week=day_of_week).exists():
            raise ValidationError(f"A configuration for {day_of_week} already exists in this pricing config.")

        return day_of_week
