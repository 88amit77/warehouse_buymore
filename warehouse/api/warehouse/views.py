from django.shortcuts import render
from .serializers import WarehouseDetailsSerializer
from rest_framework import viewsets
from .models import WarehouseDetails
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.


class WarehouseDetailsViewSet(viewsets.ModelViewSet):
    queryset = WarehouseDetails.objects.all()
    serializer_class = WarehouseDetailsSerializer


class WarehouseListCodeGetAPI(APIView):
    def get(self, request):
        qs = WarehouseDetails.objects.all()
        data = [{item.id: item.warehouse_code} for item in qs]
        return Response(data)


class WarehouseListAddressGetAPI(APIView):
    def get(self, request):
        qs = WarehouseDetails.objects.all()
        data = [{item.id: item.warehouse_address} for item in qs]
        return Response(data)
