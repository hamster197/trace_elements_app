from rest_framework import serializers

from apps.recomendations.models import RecomendationResult, RecomendationDiscription, NutritionComposition, NutritionQuide


class RecomendationResultSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = RecomendationResult
        fields = ['pk', 'creation_date', 'url',]

    def get_url(self, obj):
        request = self.context.get("request")
        if request:
            from rest_framework.reverse import reverse
            return reverse("recomendations_urls:api_recomendations_urls:recomendation_detail_url", args=[obj.pk],
                           request=request)
        return None

class NutritionQuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = NutritionQuide
        fields = ['pk', 'estimate', 'value', 'discription', 'man',]


class RecomendationResultDetailSerializer(serializers.ModelSerializer):
    discription_url = serializers.SerializerMethodField()
    nutrition_url = serializers.SerializerMethodField()

    class Meta:
        model = RecomendationResult
        fields = ['pk', 'creation_date', 'imt', 'bmr', 'KKAL', 'load_intensity', 'discription_url', 'nutrition_url',]

    def get_discription_url(self, obj):
        request = self.context.get("request")
        if request:
            from rest_framework.reverse import reverse
            return reverse("recomendations_urls:api_recomendations_urls:recomendation_discription_url",
                           args=[obj.pk], request=request)
        return None

    def get_nutrition_url(self, obj):
        request = self.context.get("request")
        if request:
            from rest_framework.reverse import reverse
            return reverse("recomendations_urls:api_recomendations_urls:nutrition_detail_url",
                           args=[obj.pk], request=request)
        return None


class NutritionCompositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = NutritionComposition
        fields = ['pk', 'title', 'dimension',]

class RecomendationDiscriptionSerializer(serializers.ModelSerializer):
    nutrition_composition_recomendation_id = NutritionCompositionSerializer(many=True, read_only=True)

    class Meta:
        model = RecomendationDiscription
        fields = ['pk', 'title', 'discription',  'nutrition_composition_recomendation_id', ]
