from django.shortcuts import render
from .serializers import WarehouseDetailsSerializer
from rest_framework import viewsets
from .models import WarehouseDetails
# Create your views here.


class WarehouseDetailsViewSet(viewsets.ViewSet):
    queryset = WarehouseDetails.objects.all()
    serializer_class = WarehouseDetailsSerializer
