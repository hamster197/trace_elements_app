from django.urls import path
from apps.questionnaire.api.views import *

app_name = 'api_questionnaire_urls'

urlpatterns = [
    path('load_intensity_quide/', LoadIntensityQuideView.as_view(), ),
    path('type_of_activity_quide/', TypeOfActivityQuideView.as_view(), ),

    path('questionnaire_all/', QuestionnaireView.as_view(), ),
    path('questionnaire_detail/<int:pk>/', QuestionnaireDetailView.as_view(), name='questionnaire_detail_url'),
    path('questionnaire_today/', QuestionnaireUpdateView.as_view(), ),
    path('questionnaire_create/', QuestionnaireCreateView.as_view(), ),

    path('questions_list/', QuestionsListView.as_view(), ),
    path('questions_result_list/', QuestionsQuiseView.as_view(), ),
    path('quize_result_list/', QuizeResultListView.as_view(), ),
    path('quize_result_detail/<int:pk>/', QuizeResultDetailView.as_view(), name='quize_result_detail_url'),
    path('quize_top_result_detail/<int:pk>/', QuizeTopResultDetailView.as_view(), name='quize_top_result_detail_url'),
]