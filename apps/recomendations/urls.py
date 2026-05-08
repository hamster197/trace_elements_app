from django.urls import path, include

from apps.recomendations.views import GetRecomendationView, RecomendationListView

app_name = 'recomendations_urls'

urlpatterns = [
    path('get_recomendation/list/', RecomendationListView.as_view(), name='list_recomendation_url'),
    path('get_recomendation/today/', GetRecomendationView.as_view(action='today', ), name='get_recomendation_url'),
    path('get_recomendation/<int:pk>/', GetRecomendationView.as_view(), name='detail_recomendation_url'),

    path('api/v1/', include('apps.recomendations.api.urls',), )
]