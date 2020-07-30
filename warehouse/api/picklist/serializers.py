from rest_framework import serializers
from .models import (
    Picklist,
    PicklistItemAlternate,
    PicklistItems,
    PicklistAssignee,
    PicklistProcessingMonitor,
    PicklistItemProcessing
)


class PicklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picklist
        fields = '__all__'


class PicklistItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PicklistItems
        fields = '__all__'


class PicklistAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PicklistAssignee
        fields = '__all__'


class PicklistItemAlternateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PicklistItemAlternate
        fields = '__all__'


class PicklistItemProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PicklistItemProcessing
        fields = '__all__'


class PicklistProcessingMonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PicklistProcessingMonitor
        fields = '__all__'


class PicklistListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    picklist_id = serializers.CharField(max_length=50)
    total_orders = serializers.IntegerField()
    shipout_time = serializers.DateTimeField(allow_null=True)
    status = serializers.CharField(max_length=25)
    type = serializers.CharField(max_length=10)
    assigned_to = serializers.CharField(max_length=200)
    packed_by = serializers.CharField(max_length=200)
    packed_quantity = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class CreatePicklistSerializer(serializers.Serializer):
    portals = serializers.CharField()
    wid = serializers.IntegerField()
    quantity = serializers.IntegerField()


class CreatePicklistResponseSerializer(serializers.Serializer):
    message = serializers.CharField
    data = PicklistSerializer()


class AssignPicklistSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()


class AssignPicklistResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = PicklistAssigneeSerializer()


class BarcodeRequestSerializer(serializers.Serializer):
    barcode = serializers.CharField()


class TempLinkRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
