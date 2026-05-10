from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Item instances.
    """
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
