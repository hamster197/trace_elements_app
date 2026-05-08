from django.urls import path, include, re_path
app_name = 'api_accounts_urls'

urlpatterns = [
    path('auth/', include('djoser.urls')),
    re_path(r"^auth/", include("djoser.urls.jwt")),
]

