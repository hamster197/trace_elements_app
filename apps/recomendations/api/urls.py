from django.urls import path

from apps.recomendations.api.views import *

app_name = 'api_recomendations_urls'

urlpatterns = [
    path('list/', RecomendationResulListView.as_view(), ),
    path('today/', RecomendationResultTodayDetailView.as_view(), ),
    path('<int:pk>/', RecomendationResultDetailView.as_view(), name='recomendation_detail_url'),
    path('nutrition/<int:pk>/', NutritionQuideSerializerView.as_view(), name='nutrition_detail_url'),
    path('discription/<int:pk>/', RecomendationDiscriptionView.as_view(), name='recomendation_discription_url'),


]