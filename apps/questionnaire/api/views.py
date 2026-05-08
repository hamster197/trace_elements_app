from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.accounts.utils import get_all_user_questionnaire
from apps.questionnaire.api.serializers import *
from apps.questionnaire.services import TodayQuestionnaireViewService, QuestionnaireViewService, \
    QuestionnaireListDetailViewService


class LoadIntensityQuideView(ListAPIView):
    """
           LoadIntensityQuide lists
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = LoadIntensityQuideSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (IsAuthenticated,)

class TypeOfActivityQuideView(ListAPIView):
    """
           TypeOfActivityQuide lists
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = TypeOfActivityQuideSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (IsAuthenticated,)

class QuestionnaireView(ListAPIView):
    """
           All User Questionnaires lists(for request user)
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = QuestionnaireListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_all_user_questionnaire(self.request.user)

class QuestionnaireDetailView(RetrieveAPIView):
    """
            User Questionnaire Detail(for request user)
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = QuestionnaireSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_all_user_questionnaire(self.request.user)



class QuestionnaireUpdateView(RetrieveUpdateDestroyAPIView):
    """
           Create User Questionnaire (for request user if user have any old Questionnaire)
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = QuestionnaireSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'put', ]

    def get(self, request, *args, **kwargs):
        if get_all_user_questionnaire(self.request.user).count() == 0:
            raise PermissionDenied({"use another url for create questionnaire": "Now you don't have permission to access to this url",})

        return self.retrieve(request, *args, **kwargs)


    def get_object(self):
        service = TodayQuestionnaireViewService(user=self.request.user,)
        return  service.get_or_create_today_user_questionnaire()

class QuestionnaireCreateView(ListCreateAPIView):
    """
           Create User Questionnaire (for request user if user have no  any old Questionnaire)
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = QuestionnaireSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return get_all_user_questionnaire(self.request.user)

    def get(self, request, *args, **kwargs):
        if get_all_user_questionnaire(self.request.user).count() != 0:
            raise PermissionDenied({"use another url for update questionnaire": "Now you don't have permission to access to this url",})

        return self.list(request, *args, **kwargs)

class QuizeResultListDetailView:
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        service = QuestionnaireListDetailViewService(user=self.request.user, obj=None)
        return service.get_user_quize_result()

class QuizeResultListView(QuizeResultListDetailView, ListAPIView):
    """
           QuizeResult list
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = QuizeResultListSerializer


class QuizeResultDetailView(QuizeResultListDetailView, RetrieveAPIView):
    """
           QuizeResult Detail pk is id of QuizeResult
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = QuizeResultDetailSerializer

class QuizeTopResultDetailView(ListAPIView):
    """
           Top Quize Result Detail pk is id of QuizeResult
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = QuizeResultElementSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        service = QuestionnaireListDetailViewService(user=self.request.user, obj=QuizeResult.objects.get(pk=self.kwargs['pk']))

        return service.get_today_user_quize_top_elements_result()


class QuestionsListView(ListAPIView):#
    """
           Questions List
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = QuestionsListSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (IsAuthenticated,)


class QuestionsQuiseView(APIView):
    """
       add discription
       permission_classes = (IsAuthenticated,)
    """
    serializer_class = QuestionQuiseSerializer
    permission_classes = (IsAuthenticated,)


    def get_permissions(self):
        QuizeResultElement.get_today_user_quize_answers()
        if QuizeResultElement.get_today_user_quize_answers().count() != 0:
            raise PermissionDenied(detail='Today questionnaire is complite! Try again tomorrow', code=None)

        return [permission() for permission in self.permission_classes]

    def post(self, request, **kwargs):
        serializer = QuestionQuiseSerializer(data=request.data)

        if serializer.is_valid():
            element_dict = dict()
            for qst in QuestionQuide.objects.all():
                for element in qst.elements_id.all():
                    if element in element_dict:
                        element_dict[element] = int(element_dict[element]) + int(request.data[str(qst.pk)])
                    else:
                        element_dict[element] = request.data[str(qst.pk)]

            service = QuestionnaireViewService(user=self.request.user, element_dict=element_dict, )
            service.save_today_user_quize_elemnts_result()

        return Response(serializer.data)

