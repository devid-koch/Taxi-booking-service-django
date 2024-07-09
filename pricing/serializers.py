from rest_framework import serializers
from .models import PricingConfig, DayPricingConfig

class DayPricingConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayPricingConfig
        fields = '__all__'

class PricingConfigSerializer(serializers.ModelSerializer):
    day_pricing = DayPricingConfigSerializer(many=True, read_only=True)

    class Meta:
        model = PricingConfig
        fields = ['id', 'name', 'is_active', 'created_at', 'updated_at', 'day_pricing']
