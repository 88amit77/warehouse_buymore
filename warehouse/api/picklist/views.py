from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .render import Render
from .models import (
    Picklist,
    PicklistItemAlternate,
    PicklistItems,
    PicklistAssignee,
    PicklistItemProcessing,
    PicklistProcessingMonitor
)
from .serializers import (
    PicklistSerializer,
    PicklistItemAlternateSerializer,
    PicklistItemsSerializer,
    PicklistAssigneeSerializer,
    PicklistListSerializer,
    PicklistItemProcessingSerializer,
    PicklistProcessingMonitorSerializer
)
from django.db.models import Q
import requests
from io import BytesIO
from datetime import datetime
# Create your views here.


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class PicklistView(viewsets.ModelViewSet):
    queryset = Picklist.objects.all()
    serializer_class = PicklistSerializer


class PicklistItemsView(viewsets.ModelViewSet):
    queryset = PicklistItems.objects.all()
    serializer_class = PicklistItemsSerializer


class PicklistItemAlternateView(viewsets.ModelViewSet):
    queryset = PicklistItemAlternate.objects.all()
    serializer_class = PicklistItemAlternateSerializer


class PicklistAssigneeView(viewsets.ModelViewSet):
    queryset = PicklistAssignee.objects.all()
    serializer_class = PicklistAssigneeSerializer


class PicklistItemProcessingView(viewsets.ModelViewSet):
    queryset = PicklistItemProcessing.objects.all()
    serializer_class = PicklistItemProcessingSerializer


class PicklistProcessingMonitorView(viewsets.ModelViewSet):
    queryset = PicklistProcessingMonitor.objects.all()
    serializer_class = PicklistProcessingMonitorSerializer


class CreatePicklist(APIView):
    def post(self, request):
        portals = request.data['portals'].split(',')
        quantity = request.data['quantity']
        warehouseId = request.data['wid']
        pickist_data = {
            'picklist_id': 'P' + str(int(datetime.timestamp(datetime.now()))),
            'total_orders': 0,
            'status': 'Created',
            'type': 'MFN',
            'portals': portals,
            'quantity': quantity,
            'warehouse_id': warehouseId
        }
        picklist = Picklist.objects.create(**pickist_data)
        return Response({"message": "Picklist created successfully"}, status=201)


class ListPicklist(APIView):
    def post(self, request):
        picklists = Picklist.objects.all()
        data = []
        for picklist in picklists:
            data.append({
                "id": picklist.id,
                "picklist_id": picklist.picklist_id,
                "total_orders": picklist.total_orders,
                "shipout_time": picklist.shipout_time,
                "status": picklist.status,
                "type": picklist.type,
                "assigned_to": "",
                "packed_by": "",
                "packed_quantity": 0,
                "created_at": picklist.created_at
            })
        # data = PicklistListSerializer(data, many=True)
        return Response(data)


class AssignPicklist(APIView):
    def post(self, request):
        picklist_id = request.data['id']
        picklist = Picklist.objects.get(id=picklist_id)
        picklist.status = 'Assigned'
        picklist.save()
        user_id = request.data['user_id']
        data = {
            'user_id': user_id,
            'picklist_id': picklist_id
        }
        picklist_assignee = PicklistAssignee.objects.create(**data)
        return Response({"message": "Picklist assigned successfully", data: picklist_assignee}, status=201)


class PicklistItemCollectView(APIView):
    def post(self, request):
        picklist_item_id = request.data['id']
        picklist_item = PicklistItems.objects.get(id=picklist_item_id)
        picklist_id = picklist_item['picklist_id']
        found = request.data['found']
        remarks = request.data['remarks']
        picklist_item.found = found
        picklist_item.remarks = remarks
        if not found:
            fnsku = request.data['fnsku']
            product_id = 1
            picklist_item_alternate_data = {
                'picklist_item_id': picklist_item_id,
                'product_id': product_id
            }
            picklist_item_alternate = PicklistItemAlternate.objects.create(**picklist_item_alternate_data)
        picklist_item.save()
        picklist = Picklist.object.get(id=picklist_id)
        total_orders = picklist.total_orders
        picklist_items_count = PicklistItems.objects.filter(picklist_id=picklist_id).filter(status='Collected').count()
        if total_orders == picklist_items_count:
            picklist.status = 'Completed'
        else:
            picklist.status = 'In Process'
        picklist.save()
        return Response({'message': "Picklist item status updated"})


class PicklistCheckView(APIView):
    def get(self, request):
        picklist_id = request.data['picklist_id']
        picklist = Picklist.object.get(picklist_id=picklist_id)
        if bool(picklist):
            id = picklist.id
            picklist_status = picklist.status
            total = PicklistItems.objects.filter(picklist_id=id).filter(~Q(status='Not Found')).count()
            picklist_processing_monitor = PicklistProcessingMonitor.objects.get(picklist_id=id)
            items_processed = picklist_processing_monitor.items_processed
            if total == items_processed:
                return Response({"status": False, "message": "Picklist is already Processed"})

            if picklist_status == 'Completed':
                return Response({"status": True, "message": "Picklist found"})
            else:
                return Response({"status": False, "message": "Picklist is in process"})
        else:
            return Response({"status": False, "message": "Picklist does not exist"})


def get_product_by_fnsku(fnsku):
    return 1


def get_order_data(order_id):
    return 1


class PicklistProcessingFnskuCheck(APIView):
    def get(self, request):
        picklist_id = request.data['picklist_id']
        picklist = Picklist.objects.get(picklist_id=picklist_id)
        id = picklist.id
        order_id = picklist.portal_new_order_id
        fnsku = request.data['fnsku']
        product_id = get_product_by_fnsku(fnsku)
        picklist_item = PicklistItems.objects.get(picklist_id=id).flter(product_id=product_id)
        if bool(picklist_item):
            picklist_item_id = picklist_item.id
            picklist_item_processing = PicklistItemProcessing.objects.get(picklist_item_id=picklist_item_id)
            if bool(picklist_item_processing):
                return Response({"status": False, "message": "Item is already processed"})
            else:
                # order_data = get_order_data(order_id)
                # product_data = get_product_data(product_id)
                return Response({
                    "product_image": "",
                    "title": "title",
                    "sku": "",
                    "fnsku": "",
                    "length": "",
                    "breadth": "",
                    "height": "",
                 })
        else:
            return Response({"status": False, "message": "Picklist item does not exist"})


class SizeCorrectness(APIView):
    def get(self, request):
        return Response({
            "True": "Yes",
            "False": "No"
        })


class LabelCorrectness(APIView):
    def get(self, request):
        return Response({
            "True": "Yes",
            "False": "No"
        })


class ImageCorrectness(APIView):
    def get(self, request):
        return Response({
            "True": "Yes",
            "False": "No"
        })


class DimensionCorrectness(APIView):
    def get(self, request):
        return Response({
            "True": "Yes",
            "False": "No"
        })


class ProductCondition(APIView):
    def get(self, request):
        return Response({
            "True": "Good",
            "False": "Bad"
        })


class Status(APIView):
    def get(self, request):
        return Response({
            "True": "Pass",
            "False": "Fail"
        })
