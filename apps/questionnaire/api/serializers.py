from rest_framework import serializers

from apps.questionnaire.constants import QuestionEstimateChoises
from apps.questionnaire.models import Questionnaire, LoadIntensityQuide, TypeOfActivityQuide, QuizeResult, \
    QuizeResultElement, QuestionQuide


class TypeOfActivityQuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeOfActivityQuide
        fields = '__all__'

class LoadIntensityQuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoadIntensityQuide
        fields = '__all__'


class QuestionnaireListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Questionnaire
        fields = ['pk', 'creation_date', 'url',]

    def get_url(self, obj):
        request = self.context.get("request")
        if request:
            from rest_framework.reverse import reverse
            return reverse("questionnaire_urls:api_questionnaire_urls:questionnaire_detail_url", args=[obj.pk],
                           request=request)
        return None

class QuestionnaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questionnaire
        exclude = ['user_id', 'creation_date', ]


    def validate(self, attrs):
        list1 = attrs.get('favorite_foods_id')
        list2 = attrs.get('not_favorite_foods_id')
        common_elements = set(list1) & set(list2)
        if common_elements:
            raise serializers.ValidationError('Delete double in favorite and not favorite foods elemnts!', )

        return attrs


class QuizeResultListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = QuizeResult
        fields = ['creation_date', 'url',]

    def get_url(self, obj):
        request = self.context.get("request")
        if request:
            from rest_framework.reverse import reverse
            return reverse("questionnaire_urls:api_questionnaire_urls:quize_result_detail_url", args=[obj.pk],
                           request=request)
        return None


class QuizeResultElementSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizeResultElement
        fields = ['id', 'element_id', 'estimation', 'percent', 'get_max', 'get_status_element']

class QuizeResultDetailSerializer(serializers.ModelSerializer):
    quize_result_id = QuizeResultElementSerializer(many=True, read_only=True)

    class Meta:
        model = QuizeResult
        fields = ['creation_date', 'quize_result_id',]

class QuestionsListSerializer(serializers.ModelSerializer):
    quize_result_id = QuizeResultElementSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionQuide
        exclude =['elements_id',]


class QuestionQuiseSerializer(serializers.Serializer):

    def get_fields(self):
        for question in QuestionQuide.objects.all():
            self._declared_fields.update({str(question.pk): serializers.ChoiceField(label=question.pk, required=True, choices=QuestionEstimateChoises.choices),})

        return self._declared_fields



