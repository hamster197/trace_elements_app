from django.urls import path

from apps.products.api.views import *

app_name = 'api_product_urls'

urlpatterns = [
    path('calories_quide/', CaloriesQuideViewSet.as_view(), ),
    path('chemical_composition_quide/', ChemicalCompositionQuideViewSet.as_view(), ),
    path('product_quide/', ProductQuideViewSet.as_view(), ),
]