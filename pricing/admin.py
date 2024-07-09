from django.contrib import admin
from .models import PricingConfig, DayPricingConfig

class DayPricingConfigInline(admin.TabularInline):
    model = DayPricingConfig
    extra = 1

@admin.register(PricingConfig)
class PricingConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    inlines = [DayPricingConfigInline]

@admin.register(DayPricingConfig)
class DayPricingConfigAdmin(admin.ModelAdmin):
    list_display = ('pricing_config', 'day_of_week', 'base_price', 'base_distance_upto_km', 'additional_price_per_km', 'waiting_charges')
    list_filter = ('pricing_config', 'day_of_week')
