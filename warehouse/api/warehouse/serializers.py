from rest_framework import serializers
from .models import WarehouseDetails
import requests


class WarehouseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseDetails
        fields = '__all__'


class WarehouseListSerializer(serializers.Serializer):
    warehouse_id = serializers.IntegerField()
    warehouse_code = serializers.CharField(max_length=50)
    warehouse_address = serializers.CharField(max_length=50)
    city = serializers.CharField(max_length=100)
    pincode = serializers.CharField(max_length=10)
    state = serializers.CharField(max_length=100)
    gst_number = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
