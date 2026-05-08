from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from apps.accounts.forms import MyUserCreationForm, MyUserUpdateForm
from django.contrib import messages

from apps.accounts.services import DashboardViewService, UserDataViewService
from config import settings


# Create your views here.
class MainView(TemplateView):
    template_name = 'accounts/main.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts_urls:dashboard_url', )

        return super().dispatch(request, *args, **kwargs)

class UserRegisterView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'accounts/register_page.html'
    success_url = reverse_lazy('accounts_urls:login_url')

    def form_valid(self, form):
        messages.success(self.request, 'Успешная регистрация! Авторизуйтесь на сайте!')

        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        service = DashboardViewService(user=self.request.user,)
        context['questionnaire_today'] = service.get_all_user_questionnaire()
        context['quize_result'] = service.get_today_user_quize_result()

        return context

class UserDataView(LoginRequiredMixin, ListView):
    template_name = 'accounts/user_data.html'
    context_object_name = 'instances'
    paginate_by = settings.MY_PAGINATION
    service = None

    def get_queryset(self):
        self.service = UserDataViewService(user=self.request.user,)
        return self.service.get_all_user_questionnaire()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questionnaire_today'] = self.service.get_today_user_questionnaire()

        return context

class UserProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/user_profile_edit.html'
    form_class = MyUserUpdateForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, 'Your instance was updated successfully!')
        url = reverse_lazy('accounts_urls:user_profile_edit_url', )
        return url
