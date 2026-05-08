from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from apps.recomendations.services import RecomendationListViewService, GetRecomendationViewService


# Create your views here.

class RecomendationListView(LoginRequiredMixin, ListView):
    template_name = 'recomendation/recomendation_list_page.html'
    context_object_name = 'instances'

    def get_queryset(self):
        service = RecomendationListViewService(user=self.request.user, )
        return service.get_user_recomendations_list()


class GetRecomendationView(LoginRequiredMixin, TemplateView):
    template_name = 'recomendation/recomendation_get_page.html'
    recomendations = None
    service = None
    action = ""

    def get(self, request, *args, **kwargs):
        if 'pk' in self.kwargs:
            self.service = GetRecomendationViewService(user = self.request.user, pk = kwargs['pk'])
            self.recomendations = self.service.get_recomendations()
            if not self.recomendations.exists():
                return redirect('accounts_urls:dashboard_url')

        else:
            self.service = GetRecomendationViewService(user = self.request.user, pk = None)

            if self.action == 'today':
                if not self.service.get_today_user_quize_result().exists():
                    messages.error(self.request, 'Complete the today survey to receive a recommendation!')
                    return redirect('questionnaire_urls:questions_url')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            recomendation = self.recomendations.first()
        else:
            recomendation, created = self.service.get_or_create_recomendation_result()

            if created:
                self.service.get_today_nutrition_result()

        context['recomendation'] = recomendation
        context['recomendation_text'] = self.service.get_recomendation_discription()

        return context

