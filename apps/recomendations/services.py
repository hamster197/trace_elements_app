from apps.questionnaire.models import QuizeResult
from apps.recomendations.models import RecomendationResult, NutritionQuide, NutritionResult, RecomendationDiscription
from datetime import date

class RecomendationListViewService():

    def __init__(self, user,):
        self.user = user

    def get_user_recomendations_list(self):
        return RecomendationResult.objects.filter(user_id=self.user,)

class GetRecomendationViewService():

    def __init__(self, user, pk):
        self.user = user
        self.pk = pk

    def get_recomendations(self, ):
        return RecomendationResult.objects.filter(user_id=self.user, pk=self.pk)

    def get_or_create_recomendation_result(self, ):
        recomendation, created = RecomendationResult.objects.get_or_create(user_id=self.user,  creation_date=date.today(),)

        return recomendation, created

    def get_today_user_quize_result(self):
        return QuizeResult.objects.filter(user_id=self.user, creation_date=date.today())

    def get_today_nutrition_result(self, ):
        age = date.today().year - self.user.date_of_birth.year \
              - ((date.today().month, date.today().day) < (self.user.date_of_birth.month, self.user.date_of_birth.day))

        if self.user.male:
            nutrion_quide = NutritionQuide.objects.filter(man=True, age_min__lte=age, age_max__gte=age)
        else:
            nutrion_quide = NutritionQuide.objects.filter(man=False, age_min__lte=age, age_max__gte=age)

        analise_result = QuizeResult.objects.get(user_id=self.user, creation_date=date.today())

        recomendation = self.get_or_create_recomendation_result()
        element_result = []
        for element in analise_result.quize_result_id.all():
            quide_rez = nutrion_quide.filter(elements_id=element.element_id)
            if quide_rez:
                if quide_rez.first().estimate <=element.estimation:
                    element_result.append(NutritionResult(recomendation_result_id=recomendation, elements_id=quide_rez.first()))

        NutritionResult.objects.bulk_create(element_result)

        pass

    def get_recomendation_discription(self,):
        recomendation_result, created = self.get_or_create_recomendation_result()
        imt = recomendation_result.imt
        recomendation_discription = RecomendationDiscription.objects.filter(imt_min__lte=imt, imt_max__gte=imt)
        if recomendation_discription.exists():
            discription = recomendation_discription.first()
        else:
            discription = recomendation_discription.none()

        return discription
