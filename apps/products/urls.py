from django.urls import path, include

app_name = 'product_urls'

urlpatterns = [
    path('api/v1/', include('apps.products.api.urls'),)
]