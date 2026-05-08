from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.recomendations.api.serializers import RecomendationResultSerializer, RecomendationResultDetailSerializer, \
    RecomendationDiscriptionSerializer, NutritionQuideSerializer
from apps.recomendations.models import RecomendationResult, NutritionResult
from apps.recomendations.services import RecomendationListViewService, GetRecomendationViewService

class RecomendationResultListDetailView:
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        service = RecomendationListViewService(user=self.request.user, )

        return service.get_user_recomendations_list()

class RecomendationResulListView(RecomendationResultListDetailView, ListAPIView):
    """
           Recomendation Results list(for request user)
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = RecomendationResultSerializer

class RecomendationResultDetailView(RecomendationResulListView, RetrieveAPIView):
    """
           Recomendation Result Detail pk is id of RecomendationResult
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = RecomendationResultDetailSerializer

class RecomendationResultTodayDetailView(RetrieveAPIView):
    """
           Today Recomendation Result Detail pk is id of RecomendationResult
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = RecomendationResultDetailView.serializer_class
    permission_classes = (IsAuthenticated,)
    queryset = RecomendationResult.objects.all()
    service = None

    def get(self, request, *args, **kwargs):
        self.service = GetRecomendationViewService(user = self.request.user, pk = None)
        quize_result = self.service.get_today_user_quize_result()
        if not quize_result.exists():
            raise PermissionDenied({"Complete the today survey to receive a recommendation": "Now you don't have permission to access to this url",})

        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        recomendation, created =  self.service.get_or_create_recomendation_result()
        if created:
            self.service.get_today_nutrition_result()

        return recomendation


class RecomendationDiscriptionView(RetrieveAPIView):
    """
           Recomendation Result Detail Discription pk is id of RecomendationResult
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = RecomendationDiscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        service = GetRecomendationViewService(user = self.request.user, pk = self.kwargs['pk'])
        recomendation = service.get_recomendations().first()

        if not recomendation:
            raise PermissionDenied({"recommendation is absent": "Now you don't have permission to access to this url",})

        obj = service.get_recomendation_discription()
        return obj

class NutritionQuideSerializerView(ListAPIView):
    """
           Nutrition Quide Detail Discription for request user pk is id of RecomendationResult
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = NutritionQuideSerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        nutrion_pks = (NutritionResult.objects.filter(recomendation_result_id__pk=self.kwargs['pk'],
                                                     recomendation_result_id__user_id=self.request.user)
                       .values('elements_id__pk'))
        qst = self.serializer_class.Meta.model.objects.filter(pk__in=nutrion_pks)

        return qst
