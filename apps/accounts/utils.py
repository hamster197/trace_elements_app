from apps.questionnaire.models import Questionnaire


def get_all_user_questionnaire(user, ):

    return (Questionnaire.objects.filter(user_id=user,).select_related('load_intensity_id',)
            .prefetch_related('type_of_activity_id', 'favorite_foods_id', 'not_favorite_foods_id',))