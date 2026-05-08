from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.products.api.serializers import *


class CaloriesQuideViewSet(ListAPIView):
    """
           CaloriesQuide lists
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = CaloriesQuideSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (IsAuthenticated,)

class ChemicalCompositionQuideViewSet(ListAPIView):
    """
           ChemicalCompositionQuide lists
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = ChemicalCompositionQuideSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (IsAuthenticated,)

class ProductQuideViewSet(ListAPIView):
    """
           ProductQuide lists
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = ProductQuideSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (IsAuthenticated,)