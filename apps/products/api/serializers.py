from rest_framework import serializers

from apps.products.models import *

class CaloriesQuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaloriesQuide
        fields = '__all__'

class ChemicalCompositionQuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChemicalCompositionQuide
        fields = '__all__'

class ProductQuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductQuide
        fields = '__all__'