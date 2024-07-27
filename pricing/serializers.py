from rest_framework import serializers
from .models import PricingConfig, DayPricingConfig, Invoice

class PricingConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingConfig
        fields = '__all__'

class DayPricingConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayPricingConfig
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
