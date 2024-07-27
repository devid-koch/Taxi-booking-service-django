# my_app/utils.py

from decimal import Decimal, ROUND_HALF_UP
from .models import DayPricingConfig
from django.http import JsonResponse


def calculate_price(pricing_config, distance, travel_time, waiting_time, day_of_week):
    try:

        day_pricing = DayPricingConfig.objects.get(pricing_config=pricing_config, day_of_week=day_of_week)

        DBP = day_pricing.base_price
        base_distance = day_pricing.base_distance_upto_km
        additional_price_per_km = day_pricing.additional_price_per_km
        time_multipliers = day_pricing.time_multiplier_factor  # Example: {"0-1": 1.0, "1-2": 1.25, "2-3": 2.2}
        waiting_charges = day_pricing.waiting_charges

        Dn = max(0, distance - base_distance)
        # Calculate time multiplier based on travel time
        TMF = Decimal(1.0)  # Default multiplier
        for hours_range, multiplier in time_multipliers.items():
            start_hour, end_hour = map(int, hours_range.split('-'))
            if travel_time <= end_hour:
                TMF = Decimal(multiplier)
                break

        # Calculate the price
        price = (DBP + (Dn * additional_price_per_km)) + (travel_time * TMF) + (waiting_time / Decimal(3) * waiting_charges)
            
        final_price = price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return final_price

    except DayPricingConfig.DoesNotExist:
        return JsonResponse({'error': f'Pricing config for {day_of_week} not found.'}, status=404)
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
