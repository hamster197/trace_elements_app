
from apps.accounts.utils import get_all_user_questionnaire
from apps.questionnaire.models import Questionnaire, QuizeResultElement, QuizeResult
from datetime import date

class TodayQuestionnaireViewService:
    model = Questionnaire

    def __init__(self, user):
        self.user = user

    def get_or_create_today_user_questionnaire(self):
        old_questionnaire = get_all_user_questionnaire(self.user).first()
        if old_questionnaire:
            defaults_values={'height': old_questionnaire.height, 'weight': old_questionnaire.weight ,
                             'load_intensity_id':old_questionnaire.load_intensity_id,
                             'goal_choises': old_questionnaire.goal_choises,
                             }

        obj, created = self.model.objects.get_or_create(
            user_id=self.user, creation_date=date.today(),
            defaults=defaults_values,
        )

        if created:
            obj.type_of_activity_id.set(old_questionnaire.type_of_activity_id.all())
            obj.favorite_foods_id.set(old_questionnaire.favorite_foods_id.all())
            obj.not_favorite_foods_id.set(old_questionnaire.not_favorite_foods_id.all())

        return obj

class QuestionnaireViewService():

    def __init__(self, user, element_dict):
        self.user = user
        self.element_dict = element_dict


    def save_today_user_quize_elemnts_result(self):
        from apps.questionnaire.models import QuizeResult, QuestionQuide
        quize, created = QuizeResult.objects.get_or_create(user_id=self.user, creation_date=date.today())

        element_result = []
        for key in self.element_dict:
            total = QuestionQuide.objects.filter(elements_id=key).count() * 4
            element_dict_id = int(self.element_dict[key])
            element_result.append(QuizeResultElement(quize_id=quize, element_id=key, estimation=element_dict_id,
                                                     percent= (element_dict_id / total) * 100 ))

        QuizeResultElement.objects.bulk_create(element_result)

        pass

class QuestionnaireListDetailViewService():

    def __init__(self, user, obj):
        self.user = user
        self.obj = obj

    def get_user_quize_result(self):
        return QuizeResult.objects.filter(user_id=self.user)

    def get_today_user_quize_top_elements_result(self, ):
        return self.obj.quize_result_id.all().order_by('quize_id', '-percent')[:2]
