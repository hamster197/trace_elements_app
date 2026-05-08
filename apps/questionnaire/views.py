from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, UpdateView
from django.contrib import messages

from apps.accounts.utils import get_all_user_questionnaire
from apps.questionnaire.forms import QuestionnaireForm, QuestionForm, QuestionsFormset
from apps.questionnaire.models import QuizeResultElement
from apps.questionnaire.services import TodayQuestionnaireViewService, QuestionnaireViewService, \
    QuestionnaireListDetailViewService
from config import settings


# Create your views here.
class UserQuestionnaireDetailView(LoginRequiredMixin, DetailView):
    template_name = 'questionnaire/questionnaire_detail.html'
    context_object_name = 'instance'

    def get_queryset(self):
        return get_all_user_questionnaire(self.request.user)


class QuestionnaireView(LoginRequiredMixin,):
    template_name = 'questionnaire/questionnaire_today.html'
    form_class = QuestionnaireForm

    def get_success_url(self):
        messages.success(self.request, 'Your instance was updated successfully!')
        url = reverse_lazy('questionnaire_urls:questionnaire_today_url', )
        return url

class TodayQuestionnaireView(QuestionnaireView, UpdateView):

    def get_object(self, queryset = None):
        service = TodayQuestionnaireViewService(user=self.request.user,)
        return service.get_or_create_today_user_questionnaire()

class QuestionnaireView(LoginRequiredMixin, TemplateView):
    template_name = 'questionnaire/questions_answers_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = QuestionsFormset(queryset=QuestionForm.Meta.model.objects.all(),)

        return context

    def render_to_response(self, context, **response_kwargs):
        answers = QuizeResultElement.get_today_user_quize_answers()
        if answers.count() != 0:
            return redirect('questionnaire_urls:questionnaires_list_url')

        response_kwargs.setdefault("content_type", self.content_type)

        return self.response_class(request=self.request, template=self.get_template_names(),context=context,
            using=self.template_engine,  **response_kwargs, )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        formset = QuestionsFormset(request.POST)
        element_dict = dict()
        for form in formset:
            if form.is_valid():
                for element in form.instance.elements_id.all():
                    if element in element_dict:
                        element_dict[element] = int(element_dict[element]) + int(form.cleaned_data['answer_field'])
                    else:
                        element_dict[element] = form.cleaned_data['answer_field']

        service = QuestionnaireViewService(user=self.request.user, element_dict=element_dict, )
        service.save_today_user_quize_elemnts_result()

        return self.render_to_response(context)

class QuestionnairesListDetail(LoginRequiredMixin):

    def get_queryset(self):
        service = QuestionnaireListDetailViewService(user=self.request.user, obj=None)

        return service.get_user_quize_result()

class QuestionnairesListView(QuestionnairesListDetail, ListView):
    template_name = 'questionnaire/questions_list_page.html'
    context_object_name = 'instances'
    paginate_by = settings.MY_PAGINATION



class QuestionnaireDetailView(QuestionnairesListDetail, DetailView):
    template_name = 'questionnaire/question_result_page.html'
    context_object_name = 'instance'


#
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        service = QuestionnaireListDetailViewService(user=self.request.user, obj=self.object)
        context['top'] = service.get_today_user_quize_top_elements_result()

        return context




