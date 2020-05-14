from rest_framework import serializers
from .models import WarehouseDetails
import requests


class WarehouseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseDetails
        fields = '__all__'
