from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PricingConfig, DayPricingConfig, Invoice
from django.core.mail import send_mail
from django.template.loader import render_to_string
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import PricingConfig, DayPricingConfig
from .forms import PricingConfigForm, DayPricingConfigForm
from django.http import JsonResponse
from .utils import calculate_price
from django.conf import settings
from django.db import connection
from django.db.models import ForeignKey
from django.apps import apps
from django.db import models
import logging

logger = logging.getLogger(__name__)


class EstimatePrice(APIView):

    def post(self, request):
        try:
            data = request.data
            pricing_config_id = data.get('pricing_config_id')
            distance = Decimal(data.get('distance'))
            travel_time = Decimal(data.get('travel_time'))
            waiting_time = Decimal(data.get('waiting_time'))
            day_of_week = data.get('day')

            pricing_config = PricingConfig.objects.get(id=pricing_config_id, is_active=True)
            final_price = calculate_price(pricing_config, distance, travel_time, waiting_time, day_of_week)

            return JsonResponse({'price': final_price})

        except PricingConfig.DoesNotExist:
            return JsonResponse({'error': 'Pricing config not found or inactive.'}, status=404)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class GenerateInvoice(APIView):

    def post(self, request):
        try:
            data = request.data
            pricing_config_id = data.get('pricing_config_id')
            distance = Decimal(data.get('distance'))
            travel_time = Decimal(data.get('travel_time'))
            waiting_time = Decimal(data.get('waiting_time'))
            day_of_week = data.get('day')
            user_email = data.get('user_email')
            total_tax_percentage = Decimal(request.data.get('total_tax_percentage', 0))

            
            pricing_config = PricingConfig.objects.get(id=pricing_config_id, is_active=True)
            final_price = calculate_price(pricing_config, distance, travel_time, waiting_time, day_of_week)

            total_tax = final_price * (total_tax_percentage / 100)
            total_price = final_price + total_tax

            invoice = Invoice.objects.create(
                user_email=user_email,
                ride_details=data,
                base_price=final_price,
                total_price=total_price,
                total_tax=total_tax
            )

            email_subject = 'Your Invoice'
            email_body = render_to_string('email_invoice.html', {'invoice': invoice})
            try:
                send_mail(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [user_email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"Failed to send email: {str(e)}")

            return Response({'invoice_id': str(invoice.id),'estimate price': Decimal(final_price), 'total_price': Decimal(total_price), 'total_tax': Decimal(total_tax)}, status=status.HTTP_201_CREATED)
        except (TypeError, ValueError) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




def pricing_config_list(request):
    configs = PricingConfig.objects.all()
    return render(request, 'pricing_config_list.html', {'configs': configs})


def pricing_config_detail(request, pk):
    pricing_config = get_object_or_404(PricingConfig, pk=pk)
    day_pricing_configs = pricing_config.day_pricing.all()
    return render(request, 'pricing_config_detail.html', {'pricing_config': pricing_config, 'day_pricing_configs': day_pricing_configs})

def pricing_config_create(request):
    if request.method == 'POST':
        form = PricingConfigForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pricing_config_list')
    else:
        form = PricingConfigForm()
    return render(request, 'pricing_config_form.html', {'form': form})

def pricing_config_update(request, pk):
    config = get_object_or_404(PricingConfig, pk=pk)
    if request.method == 'POST':
        form = PricingConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            return redirect('pricing_config_list')
    else:
        form = PricingConfigForm(instance=config)
    return render(request, 'pricing_config_form.html', {'form': form})

def day_pricing_config_create(request, pricing_config_id):
    pricing_config = get_object_or_404(PricingConfig, id=pricing_config_id)
    if request.method == 'POST':
        form = DayPricingConfigForm(request.POST)
        if form.is_valid():
            day_pricing = form.save(commit=False)
            day_pricing.pricing_config = pricing_config
            day_pricing.save()
            return redirect('pricing_config_list')
    else:
        form = DayPricingConfigForm()
    return render(request, 'day_pricing_config_form.html', {'form': form, 'pricing_config': pricing_config})


# def db_schema_view(request):
#     tables = []
#     with connection.cursor() as cursor:
#         for table_name in connection.introspection.table_names():
#             cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'")
#             columns = cursor.fetchall()
#             tables.append((table_name, columns))
#     return render(request,'db_schema.html',{'tables':tables})


def schema_overview(request):
    all_models = apps.get_models()

    schema_data = []
    for model in all_models:
        model_info = {
            'table_name': model._meta.db_table,
            'fields': [],
            'related_fields': []
        }

        for field in model._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                model_info['related_fields'].append({
                    'name': field.name,
                    'type': 'ForeignKey',
                    'to': field.related_model._meta.db_table
                })
            elif isinstance(field, models.OneToOneField):
                model_info['related_fields'].append({
                    'name': field.name,
                    'type': 'OneToOneField',
                    'to': field.related_model._meta.db_table
                })
            elif isinstance(field, models.ManyToManyField):
                model_info['related_fields'].append({
                    'name': field.name,
                    'type': 'ManyToManyField',
                    'to': field.related_model._meta.db_table
                })
            else:
                model_info['fields'].append({
                    'name': field.name,
                    'type': field.get_internal_type()
                })

        schema_data.append(model_info)

    return render(request, 'schema_overview.html', {'schema_data': schema_data})
