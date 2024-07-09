from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import create_pricing_config, update_pricing_config, create_day_pricing_config, pricing_list, PricingConfigViewSet, DayPricingConfigViewSet,calculate_price,delete_pricing_config

router = DefaultRouter()
router.register(r'pricing-configs', PricingConfigViewSet)
router.register(r'day-pricing-configs', DayPricingConfigViewSet)

urlpatterns = [
    path('create/', create_pricing_config, name='create_pricing_config'),
    path('<int:pk>/update/', update_pricing_config, name='update_pricing_config'),
    path('<int:pricing_config_id>/create-day/', create_day_pricing_config, name='create_day_pricing_config'),
    path('', pricing_list, name='pricing_list'),
    path('<int:pk>/delete/', delete_pricing_config, name='delete_pricing_config'),
    path('api/', include(router.urls)),
    path('api/calculate-price/', calculate_price, name='calculate_price'),
]
