from django.urls import path
from . import views
from .views import EstimatePrice, GenerateInvoice

urlpatterns = [
    path('api/estimate-price/', EstimatePrice.as_view(), name='EstimatePrice'),
    path('api/generate-invoice/', GenerateInvoice.as_view(), name='GenerateInvoice'),

    path('', views.pricing_config_list, name='pricing_config_list'),
    path('create/', views.pricing_config_create, name='pricing_config_create'),
    path('pricing-configs/<int:pk>/', views.pricing_config_detail, name='pricing_config_detail'),
    path('<int:pk>/update/', views.pricing_config_update, name='pricing_config_update'),
    path('<int:pricing_config_id>/day-pricing/create/', views.day_pricing_config_create, name='day_pricing_config_create'),
]
