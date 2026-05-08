from django.urls import path, include

from apps.questionnaire.views import TodayQuestionnaireView, UserQuestionnaireDetailView, \
    QuestionnaireView, QuestionnairesListView, QuestionnaireDetailView

app_name = 'questionnaire_urls'

urlpatterns = [
    path('<int:pk>/', UserQuestionnaireDetailView.as_view(), name='questionnaire_detail_url'),
    path('today/', TodayQuestionnaireView.as_view(), name='questionnaire_today_url'),
    # path('create/', CreateQuestionnaireView.as_view(), name='questionnaire_create_url'),
    path('questions/', QuestionnaireView.as_view(), name='questions_url'),
    path('questionnaires_list/', QuestionnairesListView.as_view(), name='questionnaires_list_url'),
    path('questionnaires_detail/<int:pk>/', QuestionnaireDetailView.as_view(), name='questionnaires_detail_url'),

    path('api/v1/', include('apps.questionnaire.api.urls',), )
]