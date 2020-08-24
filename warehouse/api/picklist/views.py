from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
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
    CreatePicklistSerializer,
    CreatePicklistResponseSerializer,
    AssignPicklistSerializer,
    AssignPicklistResponseSerializer,
    PicklistItemProcessingSerializer,
    PicklistProcessingMonitorSerializer
)
from django.db.models import Q
import requests
from io import BytesIO
from datetime import datetime
from base64 import b64encode
from reportlab.lib import units
from reportlab.graphics import renderPM
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing
import psycopg2
from drf_yasg.utils import swagger_auto_schema
import dropbox


access_token = 'd7ElXR2Sr-AAAAAAAAAAC2HC0qc45ss1TYhRYB4Jy6__NJU1jjGiffP7LlP_2rrf'
dbx = dropbox.Dropbox(access_token)


def get_barcode(value, width, barWidth = 0.05 * units.inch, fontSize = 30, humanReadable = True):

    barcode = createBarcodeDrawing('Code128', value = value, barWidth = barWidth, fontSize = fontSize, humanReadable = humanReadable)

    drawing_width = width
    barcode_scale = drawing_width / barcode.width
    drawing_height = barcode.height * barcode_scale

    drawing = Drawing(drawing_width, drawing_height)
    drawing.scale(barcode_scale, barcode_scale)
    drawing.add(barcode, name='barcode')
    return drawing


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class PicklistView(viewsets.ModelViewSet):
    queryset = Picklist.objects.all()
    serializer_class = PicklistSerializer
    pagination_class = CustomPageNumberPagination


class PicklistListView(viewsets.ModelViewSet):
    # queryset = Picklist.objects.all()
    serializer_class = PicklistSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        qs = Picklist.objects.all()

        return qs.order_by('-id')


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

    @swagger_auto_schema(operation_description="Create Picklist from following params: "
                                               "\n Portals - comma separated portal ids, "
                                               "\n wid: warehouse Id,\n quantity no. of orders in picklist",
                         request_body=CreatePicklistSerializer,
                         responses={201: CreatePicklistResponseSerializer, 400: "string"})
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
        serializer = PicklistSerializer(data=pickist_data)
        if serializer.is_valid():
            serializer.save()
            requests.get('https://sudzmhmdh1.execute-api.ap-south-1.amazonaws.com/default/generate_picklist')
            return Response({"message": "Picklist created successfully", "data": serializer.data}, status=201)
        else:
            return Response({"message": "Error while creating the picklist"}, status=400)


class ListPicklist(APIView):
    def post(self, request):

        headers = {
            "picklist_id": "Picklist Id",
            "total_orders": "Total Orders",
            "shipout_time": "Shipout Time",
            "status": "Status",
            "type": "Type",
            "assigned_to": "Assigned To",
            "packed_by": "Packed By",
            "packed_quantity": "Packed Quantity",
            "created_at": "Created At",
        }
        sortable = [
            "picklist_id",
            "total_orders",
            "shipout_time",
            "status",
            "type",
            "assigned_to",
            "packed_by",
            "packed_quantity",
            "created_at"
        ]
        columns = []
        date_filters = ["shipout_time", "created_at"]
        selected_headers = {}
        if 'columns' in request.data:
            columns = request.data['columns'].split(',')
            selected_headers = {i: columns[i] for i in range(0, len(columns))}
        selected_headers = []
        data = []
        if 'page' in request.query_params:
            page = request.query_params['page']
        else:
            page = 1
        if 'page_size' in request.query_params:
            page_size = request.query_params['page_size']
        else:
            page_size = 20
        picklists_data = dict(requests.get('http://localhost/warehouse/picklistlist/?page=' + str(page) + '&page_size='+ str(page_size)).json())

        picklists = picklists_data['results']

        conn_users = psycopg2.connect(database="users", user="postgres", password="buymore2",
                                      host="buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com", port="5432")
        cur_users = conn_users.cursor()
        for picklist in picklists:
            assignee_data = PicklistAssignee.objects.filter(picklist_id=picklist['id']).first()
            assignee_user = ''
            if assignee_data is not None:
                assignee = assignee_data.user_id
                if assignee is not None:
                    cur_users.execute('Select username from auth_user where id = ' + str(assignee))
                    user_assignee = cur_users.fetchone()
                    if user_assignee is not None:
                        assignee_user = user_assignee[0]
                else:
                    assignee_user = ''
            try:
                picklist_processing_monitor = PicklistProcessingMonitor.objects.get(picklist_id=picklist['id'])
                packed_quantity = picklist_processing_monitor.items_processed
                packed_by_user = picklist_processing_monitor.user_id
                if packed_by_user is not None:
                    cur_users.execute('Select username from auth_user where id = ' + str(packed_by_user))
                    user_packed = cur_users.fetchone()
                    if user_packed is not None:
                        packed_by = user_packed[0]
                    else:
                        packed_by = ''
                else:
                    packed_by = ''
            except PicklistProcessingMonitor.DoesNotExist:
                packed_quantity = 0
                packed_by = ''

            data.append({
                "id": picklist['id'],
                "picklist_id": picklist['picklist_id'],
                "total_orders": picklist['total_orders'],
                "shipout_time": picklist['shipout_time'],
                "status": picklist['status'],
                "type": picklist['type'],
                "assigned_to": assignee_user,
                "packed_by": packed_by,
                "packed_quantity": packed_quantity,
                "created_at": picklist['created_at']
            })
        conn_users.close()
        next_link = None
        prev_link = None
        if picklists_data['next'] is not None:
            next_link = '/list_picklist/?' + picklists_data['next'].split('?')[1]
        if picklists_data['previous'] is not None:
            prev_link = '/list_picklist/?' + picklists_data['previous'].split('?')[1]
        new_data = []
        if len(data):
            if len(columns) > 0:
                for obj in data:
                    new_item = {key: value for (key, value) in obj.items() if key in columns}
                    new_data.append(new_item)
            else:
                new_data = data

        # data = PicklistListSerializer(data, many=True)
        return Response({"count": picklists_data['count'], 'next': next_link, 'previous': prev_link, "headers": headers,
                         "sortable": sortable, 'selected_headers': selected_headers, "date_filters": date_filters,
                         "data": new_data})


class AssignPicklist(APIView):

    @swagger_auto_schema(
        operation_description="Assign Picklist to the User. \n  Params: \n id: Picklist Id,\n user_id: User Id of the Assignee",
        request_body=AssignPicklistSerializer, responses={201: AssignPicklistResponseSerializer, 400: "string"})
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
        serializer = PicklistAssigneeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Picklist Assigned Successfully", "data": serializer.data}, status=201)

        return Response("Error while assigning the picklist", status=400)


class PicklistItemCollectView(APIView):
    def post(self, request):
        conn_products = psycopg2.connect(database="products", user="postgres", password="buymore2",
                                         host="buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com", port="5432")

        cur_products = conn_products.cursor()
        picklist_item_id = request.data['id']
        picklist_item = PicklistItems.objects.get(id=picklist_item_id)
        picklist_id = picklist_item.picklist_id
        found = request.data['found']
        remarks = request.data['remarks']
        picklist_item.found = found
        picklist_item.remarks = remarks
        if not found:
            fnsku = request.data['fnsku']
            cur_products.execute("SELECT product_id from master_masterproduct where buymore_sku = '" + fnsku + "'")
            alt_product = cur_products.fetchone()
            if alt_product is not None:
                product_id = alt_product[0]
            else:
                return Response({
                    'status': False,
                    'message': 'Alternate Product does not exist'
                })
            picklist_item_alternate_data = {
                'picklist_item_id': picklist_item_id,
                'product_id': product_id
            }
            picklist_item_alternate = PicklistItemAlternate.objects.create(**picklist_item_alternate_data)
        picklist_item.status = 'Collected'
        picklist_item.save()
        picklist = Picklist.objects.get(id=picklist_id)
        total_orders = picklist.total_orders
        picklist_items_count = PicklistItems.objects.filter(picklist_id=picklist_id).filter(status='Collected').count()
        if total_orders == picklist_items_count:
            picklist.status = 'Completed'
        else:
            picklist.status = 'In Process'
        picklist.save()
        conn_products.close()
        return Response({'message': "Picklist item status updated"})


class PicklistCheckView(APIView):
    def get(self, request):
        picklist_id = request.query_params['picklist_id']
        try:
            picklist = Picklist.objects.get(picklist_id=picklist_id)

            id = picklist.id
            picklist_status = picklist.status
            total = PicklistItems.objects.filter(picklist_id=id).filter(~Q(status='Not Found')).count()
            picklist_processing_monitor = PicklistProcessingMonitor.objects.get(picklist_id=id)
            items_processed = picklist_processing_monitor.items_processed
            if items_processed is None:
                items_processed = 0
            if total == items_processed:
                return Response({"status": False, "message": "Picklist is already Processed"})

            if picklist_status == 'Completed':
                return Response({"status": True, "total": total, "items_processed": items_processed, "message": "Picklist found"})
            else:
                return Response({"status": False, "message": "Picklist is in process"})
        except Picklist.DoesNotExist as e:
            return Response({"status": False, "message": "Picklist does not exist"})


def get_order_by_fnsku(fnsku, picklist_id):
    conn_orders = psycopg2.connect(database="orders", user="postgres", password="buymore2",
                                   host="buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com", port="5432")
    cur_orders = conn_orders.cursor()
    cur_orders.execute("Select dd_id from api_neworder no inner join api_dispatchdetails dd on no.dd_id = dd.dd_id_id where no.buymore_sku='" + fnsku + "' and dd.picklist_id=" + str(picklist_id))
    order = cur_orders.fetchone()
    conn_orders.close()
    return order[0]


def get_order_data(order_id):
    conn_products = psycopg2.connect(database="products", user="postgres", password="buymore2",
                                     host="buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com", port="5432")

    cur_products = conn_products.cursor()
    conn_orders = psycopg2.connect(database="orders", user="postgres", password="buymore2",
                                   host="buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com", port="5432")
    cur_orders = conn_orders.cursor()
    cur_orders.execute("Select product_id, portal_sku, buymore_sku from api_neworder where dd_id=" + str(order_id))
    order = cur_orders.fetchone()
    product_id = order[0]
    sku = order[1]
    fnsku = order[2]
    cur_products.execute("Select product_name, product_length, product_breath, product_width, product_weight, image_url from master_masterproduct where product_id = " + str(product_id))
    product_data = cur_products.fetchone()
    conn_products.close()
    conn_orders.close()
    return {
        "product_image_url": product_data[5],
        "title": product_data[0],
        "sku": sku,
        "fnsku": fnsku,
        "length": product_data[1],
        "breadth": product_data[2],
        "height": product_data[3],
        "weight": product_data[4]
     }


class PicklistProcessingFnskuCheck(APIView):
    def get(self, request):
        picklist_id = request.query_params['picklist_id']
        picklist = Picklist.objects.get(picklist_id=picklist_id)
        id = picklist.id
        fnsku = request.query_params['fnsku']
        order_id = get_order_by_fnsku(fnsku, id)
        picklist_item = PicklistItems.objects.get(picklist_id=id, portal_new_order_id=order_id)
        if bool(picklist_item):
            picklist_item_id = picklist_item.id
            picklist_item_processing = PicklistItemProcessing.objects.filter(picklist_item_id=picklist_item_id).first()
            if picklist_item_processing is not None:
                return Response({"status": False, "message": "Item is already processed"})
            else:
                order_data = get_order_data(order_id)
                order_data['picklist_item_id'] = picklist_item_id
                return Response({'status': True, 'data': order_data})
        else:
            return Response({"status": False, "message": "Picklist item does not exist"})


class SizeCorrectness(APIView):
    def get(self, request):
        return Response({
            "True": "Yes",
            "False": "No"
        })


class TitleCorrectness(APIView):
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


class BarcodeGenerator(APIView):
    @swagger_auto_schema(operation_description="Get barcode image code for the generated picklist id")
    def get(self, request):
        code = request.data['barcode']
        barcode = get_barcode(value=code, width=600)
        databar = b64encode(renderPM.drawToString(barcode, fmt='JPEG'))
        return Response({'barfile': databar})


class DownloadPicklist(APIView):
    def get(self, request):
        picklist_id = request.query_params['picklist_id']
        file_path = '/buymore2/picklist/' + picklist_id + '.pdf'
        link = dbx.files_get_temporary_link(file_path).link
        return {
            'link': link
        }


class ExternalPicklistProcess(APIView):
    def post(self, request):
        picklist_id = request.data['id']
        user_id = request.data['user_id']
        items_processed = request.data['quantity']
        try:
            picklist_processing_monitor = PicklistProcessingMonitor.objects.get(picklist_id=picklist_id)
            picklist_processing_monitor.start_at = datetime.now()
            picklist_processing_monitor.user_id = user_id
            picklist_processing_monitor.items_processed = items_processed
            picklist_processing_monitor.end_at = datetime.now()
            picklist_processing_monitor.status = True
            picklist_processing_monitor.save()
            picklist = Picklist.objects.get(id=picklist_id)
            picklist.status = 'Completed'
            picklist.save()
            return Response({'status': True, 'message': 'Picklist processed successfully'})
        except PicklistProcessingMonitor.DoesNotExist as e:
            return Response({'status': False})


class ExternalPicklistCreate(APIView):
    def post(self, request):
        post = request.data
        if post['type'] == 'Smart':
            portals = [2]
        else:
            portals = [1]
        picklist_data = {
            'picklist_id': post['picklist_id'],
            'quantity': post['quantity'],
            'total_orders': post['quantity'],
            'status': 'In Process',
            'type': post['type'],
            'warehouse_id': post['warehouse_id'],
            'portals': portals
        }
        picklist_serializer = PicklistSerializer(data=picklist_data)
        if picklist_serializer.is_valid():
            picklist = picklist_serializer.save()
            if picklist is not None:
                assignee_data = {
                    'picklist_id': picklist.id,
                    'user_id': post['assigned_to'],
                    'created_at': datetime.now(),
                    'completed_at': datetime.now()
                }
                assignee_serializer = PicklistAssigneeSerializer(data=assignee_data)
                if assignee_serializer.is_valid():
                    assignee = assignee_serializer.save()
                else:
                    return Response({
                        'status': False,
                        'message': 'Assignee creation failed'
                    })
                process_data = {
                    'user_id': post['user_id'],
                    'picklist_id': picklist.id,
                    'picklist_file': post['picklist_file'],
                    'start_at': datetime.now(),
                    'status': 0
                }
                process_serializer = PicklistProcessingMonitorSerializer(data=process_data)
                if process_serializer.is_valid():
                    process = process_serializer.save()
                    if process is not None:
                        return Response({
                            'status': True,
                            'message': 'Picklist created successfully'
                        })
                    else:
                        return Response({
                            'status': False,
                            'message': 'Picklist file upload failed'
                        })
                else:
                    return Response({
                        'status': False,
                        'message': 'Picklist file upload failed'
                    })
            else:
                return Response({
                    'status': False,
                    'message': 'Picklist creation failed'
                })
        else:
            return Response({
                'status': False,
                'message': 'Picklist creation failed verification',
                'error': picklist_serializer.errors
            })


class PicklistDetailView(APIView):
    def get(self, request):
        conn_products = psycopg2.connect(database="products", user="postgres", password="buymore2",
                                         host="buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com", port="5432")

        cur_products = conn_products.cursor()
        conn_orders = psycopg2.connect(database="orders", user="postgres", password="buymore2",
                                       host="buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com", port="5432")
        cur_orders = conn_orders.cursor()
        id = request.query_params['id']
        picklist = Picklist.objects.get(id=id)
        assigned_to_user = ''
        if picklist.status in ['Assigned', 'Completed']:
            assignee = PicklistAssignee.objects.get(picklist_id=id)
            if assignee is not None:
                assigned_to = assignee.user_id
                conn_users = psycopg2.connect(database="users", user="postgres", password="buymore2",
                                               host="buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com", port="5432")
                cur_users = conn_users.cursor()
                cur_users.execute('Select username from auth_user where id = ' + str(assigned_to))
                user_assignee = cur_users.fetchone()
                if user_assignee is not None:
                    assigned_to_user = user_assignee[0]
                conn_users.close()
        picklist_data = {
          'id': picklist.id,
          'picklist_id': picklist.picklist_id,
          'total_orders': picklist.total_orders,
          'shipout_time': picklist.shipout_time,
          'assigned_to': assigned_to_user,
          'status': picklist.status,
          'created_at': picklist.created_at
        }
        picklist_items_data = PicklistItems.objects.filter(picklist_id=id)
        picklist_items = []
        for item_data in picklist_items_data:
            order_query = "Select \"bin_Id\", n.product_id, n.buymore_sku, n.portal_sku, n.portal_id, n.qty " \
                          "from api_neworder n " \
                          "inner join api_dispatchdetails d on n.dd_id =d.dd_id_id " \
                          "where n.dd_id=" + str(item_data.portal_new_order_id)
            print(order_query)
            cur_orders.execute(order_query)
            order = cur_orders.fetchone()
            if order is not None:
                master_product_query = "SELECT mp.product_name, fp.flipkart_listing_id " \
                                       "from master_masterproduct mp " \
                                       "left join flipkart_flipkartproducts fp on mp.product_id = fp.product_id " \
                                       "where mp.product_id = " + str(order[1])
                cur_products.execute(master_product_query)
                master_product = cur_products.fetchone()
                try:
                    picklist_alternate_product = PicklistItemAlternate.objects.get(picklist_item_id=item_data.id)
                    if item_data.found == 'Not Found' and picklist_alternate_product is not None:
                        cur_products.execute('select product_name from master_masterproduct where product_id = ' + str(
                            picklist_alternate_product.product_id))
                        alt_product = cur_products.fetchone()
                        if alt_product is not None:
                            alternate_product_title = alt_product[0]
                except PicklistItemAlternate.DoesNotExist:
                    alternate_product_title = ''

                total_completed = 0
                total_cancelled = 0
                if item_data.status == 'Collected':
                    total_completed = order[5]

                if master_product is not None:
                    picklist_items.append({
                        'picklist_item_id': item_data.id,
                        'bin': order[0],
                        'sku': order[3],
                        'fnsku': order[2],
                        'listing_id': master_product[1],
                        'portal': order[4],
                        'title': master_product[0],
                        'total_items': order[5],
                        'remarks': item_data.remarks,
                        'alternate_product_title': alternate_product_title,
                        'total_completed': total_completed,
                        'total_cancelled': total_cancelled
                    })
        conn_products.close()
        conn_orders.close()
        return Response({
            'picklist_data': picklist_data,
            'picklist_items': picklist_items
        })


class OrderCount(APIView):
    def post(self, request):
        conn_orders = psycopg2.connect(database="orders", user="postgres", password="buymore2",
                                       host="buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com", port="5432")

        cur_orders = conn_orders.cursor()

        portals = request.data['portals']
        warehouse = request.data['wid']


        query = 'Select count(*) as count from api_neworder  inner join api_dispatchdetails ' \
                    'on api_neworder.dd_id = api_dispatchdetails.dipatch_details_id  ' \
                    'where api_dispatchdetails.is_mark_placed=TRUE and api_dispatchdetails.packing_status=FALSE and ' \
                    'api_dispatchdetails.is_dispatch=FALSE and ' \
                    'api_neworder.portal_id IN (' + str(portals) + ') and api_neworder.warehouse_id = ' + str(warehouse)

        cur_orders.execute(query)
        quantity = cur_orders.fetchone()
        if quantity is not None:
            quantity_order = quantity[0]
        else:
            quantity_order = 0
        conn_orders.close()
        return Response({"quantity": quantity})


class PicklistItemProcess(APIView):
    def post(self, request):
        conn_orders = psycopg2.connect(database="orders", user="postgres", password="buymore2",
                                       host="buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com", port="5432")
        cur_orders = conn_orders.cursor()
        data = request.data
        user_id = data['user_id']

        item_processing_serializer = PicklistItemProcessingSerializer(data=data)
        if item_processing_serializer.is_valid():
            item_processing_serializer.save()
            picklist_item = PicklistItems.objects.get(id=data['picklist_item_id'])
            picklist_id = picklist_item.picklist_id
            picklist_processing_monitor = PicklistProcessingMonitor.objects.get(picklist_id=picklist_id)
            total = PicklistItems.objects.filter(picklist_id=picklist_id).filter(~Q(status='Not Found')).count()
            if picklist_processing_monitor is not None:
                if picklist_processing_monitor.start_at is None:
                    picklist_processing_monitor.start_at = datetime.now()
                    picklist_processing_monitor.user_id = user_id
                    picklist_processing_monitor.items_processed = 1
                    picklist_processing_monitor.status = False
                else:
                    picklist_processing_monitor.items_processed += 1
                if total == picklist_processing_monitor.items_processed:
                    picklist_processing_monitor.end_at = datetime.now()
                    picklist_processing_monitor.status = True
                picklist_processing_monitor.save()

            if data['status']:
                picklist_item = PicklistItems.objects.get(id=data['picklist_item_id'])
                order_id = picklist_item.portal_new_order_id
                cur_orders.execute('select order_id, order_item_id from api_neworder where dd_id = ' + str(order_id))
                order = cur_orders.fetchone()
                if order is not None:
                    file_path = '/buymore2/orders/invoices/' + str(order[0]) + '#' + str(order[1]) + '.pdf'
                    invoice_file = dbx.files_get_temporary_link(file_path).link
                    resp = {'status': True, 'invoice': True, 'invoice_file': invoice_file}
                else:
                    resp = {'status': False, 'invoice': False, 'message': 'Invoice not found'}
            else:
                resp = {'status': True, 'invoice': False, 'invoice_file': ''}

        else:
            resp = {'status': False, 'errors': item_processing_serializer.errors}
        conn_orders.close()
        return Response(resp)


class BulkFoundPicklistItem(APIView):
    def post(self, request):
        ids = request.data['ids']
        picklist_id = request.data['picklist_id']
        remarks = request.data['remarks']
        item_ids = ids.split(',')
        try:
            PicklistItems.objects.filter(id__in=item_ids).update(found='Found', remarks=remarks, status = 'Collected')
            picklist = Picklist.objects.get(id=picklist_id)
            total_orders = picklist.total_orders
            picklist_items_count = PicklistItems.objects.filter(picklist_id=picklist_id).filter(status='Collected').count()
            if total_orders == picklist_items_count:
                picklist.status = 'Completed'
            else:
                picklist.status = 'In Process'
            picklist.save()

            return Response({'status': True, 'message': 'Records updated successfully'})
        except:
            return Response({'status': False, 'message': 'Picklist Items could not be updated'})


# class GetActivePortalAccounts(APIView):
#     def get(self, request):
#         conn_orders = psycopg2.connect(database="orders", user="postgres", password="buymore2",
#                                          host="buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com", port="5432")
#
#         cur_orders = conn_orders.cursor()
#         new_orders = cur_orders.execute('Select portal_id, portal_account_id from api_neworder no inner join api_dispatchdetails dd on no.dd_id = dd.dd_id_id where dd.is_mark_placed = True and dd.picklist_id = 0')
