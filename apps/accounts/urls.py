from django.urls import path, reverse_lazy, include
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView

from apps.accounts.views import MainView, UserRegisterView, DashboardView, UserDataView, UserProfileEditView

app_name = 'accounts_urls'

urlpatterns = [
    path('', MainView.as_view(), name='main_url'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_url'),
    path('user_data/', UserDataView.as_view(), name='user_data_url'),
    path('user_profile_edit/', UserProfileEditView.as_view(), name='user_profile_edit_url'),

    path('login/', LoginView.as_view(template_name="accounts/login_page.html", redirect_authenticated_user=True),
         name='login_url'),
    path('logout/', LogoutView.as_view(), name='logout_url'),

    path('password_change/', PasswordChangeView.as_view(template_name='accounts/password_change_form.html'),  name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),

    path('password_reset_start/', PasswordResetView.as_view(template_name='accounts/password_reset_form.html',
                                                            email_template_name='accounts/password_reset_email.html',
                                                            success_url=reverse_lazy(
                                                                'users_urls:reset_password_done')),
         name='reset_password_url'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done_form.html'),
         name='reset_password_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confim_form.html', success_url=reverse_lazy(
             'users_urls:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

    path('register/', UserRegisterView.as_view(), name='register_url'),

    path('api/v1/', include('apps.accounts.api.urls'),)

]