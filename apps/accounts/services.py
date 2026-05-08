from apps.accounts.utils import get_all_user_questionnaire
from apps.questionnaire.models import QuizeResult
from datetime import date

class DashboardViewService:

    def __init__(self, user):
        self.user = user

    def get_all_user_questionnaire(self,):
        return get_all_user_questionnaire(self.user)

    def get_today_user_quize_result(self, ):
        return QuizeResult.objects.filter(user_id=self.user, creation_date=date.today())

class UserDataViewService:

    def __init__(self, user):
        self.user = user

    def get_all_user_questionnaire(self):
        return get_all_user_questionnaire(self.user)

    def get_today_user_questionnaire(self):
        return self.get_all_user_questionnaire().filter(creation_date=date.today())