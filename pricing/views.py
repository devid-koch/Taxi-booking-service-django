from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .models import PricingConfig, DayPricingConfig
from .forms import PricingConfigForm, DayPricingConfigForm
from .serializers import PricingConfigSerializer, DayPricingConfigSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from decimal import Decimal,ROUND_HALF_UP
from rest_framework.response import Response
from rest_framework import status

# API Views
class PricingConfigViewSet(viewsets.ModelViewSet):
    queryset = PricingConfig.objects.all()
    serializer_class = PricingConfigSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Pricing configuration deleted successfully.'}, status=status.HTTP_200_OK)

class DayPricingConfigViewSet(viewsets.ModelViewSet):
    queryset = DayPricingConfig.objects.all()
    serializer_class = DayPricingConfigSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Pricing configuration deleted successfully.'}, status=status.HTTP_200_OK)


# Admin Views
def create_pricing_config(request):
    if request.method == 'POST':
        form = PricingConfigForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pricing_list')
    else:
        form = PricingConfigForm()
    return render(request, 'pricing/create_pricing_config.html', {'form': form})

def update_pricing_config(request, pk):
    pricing_config = get_object_or_404(PricingConfig, pk=pk)
    if request.method == 'POST':
        form = PricingConfigForm(request.POST, instance=pricing_config)
        if form.is_valid():
            form.save()
            return redirect('pricing_list')
    else:
        form = PricingConfigForm(instance=pricing_config)
    return render(request, 'pricing/update_pricing_config.html', {'form': form})

def create_day_pricing_config(request, pricing_config_id):
    pricing_config = get_object_or_404(PricingConfig, id=pricing_config_id)
    if request.method == 'POST':
        form = DayPricingConfigForm(request.POST)
        if form.is_valid():
            day_pricing = form.save(commit=False)
            day_pricing.pricing_config = pricing_config
            day_pricing.save()
            return redirect('pricing_list')
    else:
        form = DayPricingConfigForm()
    return render(request, 'pricing/create_day_pricing_config.html', {'form': form, 'pricing_config': pricing_config})

def pricing_list(request):
    configs = PricingConfig.objects.all()
    return render(request, 'pricing/pricing_list.html', {'configs': configs})


@api_view(['DELETE'])
def delete_pricing_config(request, pk):
    try:
        pricing_config = PricingConfig.objects.get(pk=pk)
        pricing_config.delete()
        return JsonResponse({'message': 'Pricing configuration deleted successfully.'}, status=200)
    except PricingConfig.DoesNotExist:
        return JsonResponse({'error': 'Pricing configuration not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def calculate_price(request):
    data = request.data
    pricing_config_id = data.get('pricing_config_id')
    distance = Decimal(data.get('distance'))
    travel_time = Decimal(data.get('travel_time'))
    waiting_time = Decimal(data.get('waiting_time'))
    day_of_week = data.get('day')

    try:
        pricing_config = PricingConfig.objects.get(id=pricing_config_id, is_active=True)
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

        return JsonResponse({'price': float(final_price)})

    except PricingConfig.DoesNotExist:
        return JsonResponse({'error': 'Pricing config not found or inactive.'}, status=404)
    except DayPricingConfig.DoesNotExist:
        return JsonResponse({'error': f'Pricing config for {day_of_week} not found.'}, status=404)
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
