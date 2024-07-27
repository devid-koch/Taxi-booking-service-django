from django.db import models
from django.utils import timezone

class PricingConfig(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class DayPricingConfig(models.Model):

    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    pricing_config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE, related_name='day_pricing')
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    base_price = models.DecimalField(max_digits=5, decimal_places=2)
    base_distance_upto_km = models.DecimalField(max_digits=5, decimal_places=2, default=3.00)
    additional_price_per_km = models.DecimalField(max_digits=5, decimal_places=2)
    time_multiplier_factor = models.JSONField()  # Store as a list of tuples [(hours, multiplier)]
    waiting_charges = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('pricing_config', 'day_of_week')

    def __str__(self):
        return f"{self.pricing_config.name} - {self.day_of_week}"

class PricingLog(models.Model):
    pricing_config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE)
    changed_by = models.CharField(max_length=255)
    change_timestamp = models.DateTimeField(default=timezone.now)
    change_description = models.TextField()

    def __str__(self):
        return f"Log for {self.pricing_config.name} at {self.change_timestamp}"

class Invoice(models.Model):
    user_email = models.EmailField()
    ride_details = models.JSONField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
