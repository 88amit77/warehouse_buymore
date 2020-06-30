from django.shortcuts import render
from .serializers import WarehouseDetailsSerializer, WarehouseListSerializer
from rest_framework import viewsets
from .models import WarehouseDetails
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
import requests
import dropbox
# Create your views here.
from datetime import timedelta, datetime

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class WarehouseDetailsViewSet(viewsets.ModelViewSet):
    queryset = WarehouseDetails.objects.all()
    serializer_class = WarehouseDetailsSerializer


class WarehouseQueryViewSet(viewsets.ModelViewSet):
    serializer_class = WarehouseDetailsSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        qs = WarehouseDetails.objects.all()
        if 'keyword' in self.request.data:
            qf = Q(id__contains=self.request.data['keyword']) | \
                 Q(warehouse_code__contains=self.request.data['keyword']) | \
                 Q(warehouse_address__contains=self.request.data['keyword']) | \
                 Q(city__contains=self.request.data['keyword']) | \
                 Q(state__contains=self.request.data['keyword']) | \
                 Q(gst_number__contains=self.request.data['keyword']) | \
                 Q(pincode__contains=self.request.data['keyword']) | \
                 Q(created_at__contains=self.request.data['keyword']) | \
                 Q(updated_at__contains=self.request.data['keyword'])
            qs = qs.filter(qf)
        if 'warehouse_id' in self.request.data:
            warehouse_id = self.request.data['warehouse_id'].split(',')
            qs = qs.filter(id__in=warehouse_id)
        if 'warehouse_code' in self.request.data:
            warehouse_code = self.request.data['warehouse_code'].split(',')
            qs = qs.filter(warehouse_code__in=warehouse_code)
        if 'warehouse_address' in self.request.data:
            warehouse_address = self.request.data['warehouse_address'].split(',')
            qs = qs.filter(warehouse_address__in=warehouse_address)
        if 'city' in self.request.data:
            city = self.request.data['city'].split(',')
            qs = qs.filter(city__in=city)
        if 'pincode' in self.request.data:
            pincode = self.request.data['pincode'].split(',')
            qs = qs.filter(pincode__in=pincode)
        if 'state' in self.request.data:
            state = self.request.data['state'].split(',')
            qs = qs.filter(state__in=state)
        if 'gst_number' in self.request.data:
            gst_number = self.request.data['gst_number'].split(',')
            qs = qs.filter(gst_number__in=gst_number)
        if 'created_at' in self.request.data:
            created_at = self.request.data['created_at'].split('/')
            qs = qs.filter(created_at__range=created_at)
        if 'updated_at' in self.request.data:
            updated_at = self.request.data['updated_at'].split('/')
            qs = qs.filter(updated_at__range=updated_at)
        if 'sort_by' in self.request.data:
            sort_key = self.request.data['sort_by']
            if sort_key == 'warehouse_id':
                sort_key = 'id'
            sort_by = ''
            if 'sort_order' in self.request.data and self.request.data['sort_order'] == 'desc':
                sort_by = '-'
            sort_by += sort_key
            qs = qs.order_by(sort_by)
        return qs


class WarehouseListCodeGetAPI(APIView):
    def get(self, request):
        qs = WarehouseDetails.objects.all()
        data = {}
        for item in qs:
            data[item.id] = item.warehouse_code
        return Response(data)


class WarehouseListAddressGetAPI(APIView):
    def get(self, request):
        qs = WarehouseDetails.objects.all()
        data = {}
        for item in qs:
            data[item.id] = item.warehouse_address
        return Response(data)


class WarehouseListView(APIView):
    def post(self, request):
        columns = []
        selected_headers = {}
        filters = {}
        sorting = {}
        header = {
            'warehouse_id': 'Warehouse Id',
            'warehouse_code': 'Warehouse Code',
            'warehouse_address': 'Warehouse Address',
            'city': 'City',
            'pincode': 'Pincode',
            'state': 'State',
            'gst_number': 'GSTIN Number',
            'created_at': 'Created At',
            'updated_at': 'Updated At'
        }
        sticky_headers = [
            'warehouse_id',
            'warehouse_code',
            'warehouse_address'
        ]

        sortable = [
            'warehouse_id',
            'warehouse_code',
            'warehouse_address',
            'city',
            'pincode',
            'state',
            'gst_number',
            'created_at',
            'updated_at'
        ]
        date_filters = [
            'created_at',
            'updated_at'
        ]
        if 'columns' in request.data:
            columns = request.data['columns'].split(',')
            selected_headers = {i: columns[i] for i in range(0, len(columns))}
        if 'page' in request.query_params:
            page = request.query_params['page']
        else:
            page = 1
        if 'page_size' in request.query_params:
            page_size = request.query_params['page_size']
        else:
            page_size = 20
        warehouses = requests.get('http://localhost:8001/warehouses/?page=' + str(page) + '&page_size=' + str(page_size),
                               data=request.data).json()
        data = []
        warehouses_data = warehouses['results']

        for i in range(len(warehouses_data)):
            item = warehouses_data[i]
            print(item)
            warehouse_item = {
                'warehouse_id': item['id'],
                'warehouse_code': item['warehouse_code'],
                'warehouse_address': item['warehouse_address'],
                'city': item['city'],
                'pincode': item['pincode'],
                'state': item['state'],
                'gst_number': item['gst_number'],
                'created_at': item['created_at'],
                'updated_at': item['updated_at']
            }
            data.append(warehouse_item)
        new_data = []
        if len(data):
            serializer = WarehouseListSerializer(data, many=True)
            if len(columns) > 0:
                for obj in serializer.data:
                    columns.append('warehouse_id')
                    columns.append('warehouse_code')
                    columns.append('warehouse_address')
                    new_item = {key: value for (key, value) in obj.items() if key in columns}
                    new_data.append(new_item)
            else:
                new_data = serializer.data
            next_link = None
            prev_link = None
            if warehouses['next'] is not None:
                next_link = '/list_warehouse/?' + warehouses['next'].split('?')[1]
            if warehouses['previous'] is not None:
                prev_link = '/list_warehouse/?' + warehouses['previous'].split('?')[1]
            return Response({'count': warehouses['count'], 'next': next_link, 'previous': prev_link, 'header': header,
                             'selected_headers': selected_headers, 'data': new_data, 'filters': filters,
                             'date_filters': date_filters, 'sticky_headers': sticky_headers, 'sorting': sorting,
                             'sortable': sortable, 'message': 'Warehouses fetched successfully'})
        else:
            data = []
            return Response({'count': 0, 'next': None, 'previous': None, 'header': header, 'data': data,
                             'selected_headers': selected_headers, 'filters': filters, 'date_filters': date_filters,
                             'sticky_headers': sticky_headers, 'sorting': sorting, 'sortable': sortable,
                             'message': 'No warehouse found'})


class WarehouseIdFilterView(APIView):
    def get(self, request):
        """
        Warehouse Id filter
        """
        qs = WarehouseDetails.objects.distinct('id').all()
        if 'warehouse_id' in request.query_params:
            qs = qs.filter(id__contains=request.query_params['warehouse_id'])
        data1 = [{data.id: data.id} for data in qs]
        return Response(data1)


class WarehouseCodeFilterView(APIView):
    def get(self, request):
        """
        Warehouse code filter
        """
        qs = WarehouseDetails.objects.distinct('warehouse_code').all()
        if 'warehouse_code' in request.query_params:
            qs = qs.filter(warehouse_code__contains=request.query_params['warehouse_code'])
        data1 = [{data.warehouse_code: data.warehouse_code} for data in qs]
        return Response(data1)


class WarehouseAddressFilterView(APIView):
    def get(self, request):
        """
        Warehouse address filter
        """
        qs = WarehouseDetails.objects.distinct('warehouse_address').all()
        if 'warehouse_address' in request.query_params:
            qs = qs.filter(warehouse_address__contains=request.query_params['warehouse_address'])
        data1 = [{data.warehouse_address: data.warehouse_address} for data in qs]
        return Response(data1)


class WarehouseCityFilterView(APIView):
    def get(self, request):
        """
        Warehouse city filter
        """
        qs = WarehouseDetails.objects.distinct('city').all()
        if 'city' in request.query_params:
            qs = qs.filter(city__contains=request.query_params['city'])
        data1 = [{data.city: data.city} for data in qs]
        return Response(data1)


class WarehousePincodeFilterView(APIView):
    def get(self, request):
        """
        Warehouse pincode filter
        """
        qs = WarehouseDetails.objects.distinct('pincode').all()
        if 'pincode' in request.query_params:
            qs = qs.filter(pincode__contains=request.query_params['pincode'])
        data1 = [{data.pincode: data.pincode} for data in qs]
        return Response(data1)


class WarehouseStateFilterView(APIView):
    def get(self, request):
        """
        Warehouse state filter
        """
        qs = WarehouseDetails.objects.distinct('state').all()
        if 'state' in request.query_params:
            qs = qs.filter(state__contains=request.query_params['state'])
        data1 = [{data.state: data.state} for data in qs]
        return Response(data1)


class WarehouseGstFilterView(APIView):
    def get(self, request):
        """
        Warehouse gst number filter
        """
        qs = WarehouseDetails.objects.distinct('gst_number').all()
        if 'gst_number' in request.query_params:
            qs = qs.filter(gst_number__contains=request.query_params['gst_number'])
        data1 = [{data.gst_number: data.gst_number} for data in qs]
        return Response(data1)


class WarehouseSelectView(APIView):
    def get(self, request):
        warehouses = WarehouseDetails.objects.filter(which_warehouse="Buymore Warehouse")
        result = [{warehouse.id: warehouse.warehouse_address} for warehouse in warehouses]
        return Response(result)


class GetDropboxFile(APIView):
    def get(self, request):
        id = request.data['id']
        export_data = dict(requests.get('http://13.232.166.20/create_export/'+ str(id) +'/').json())

        folder_url = export_data['exfile_url']
        folder_url_created = export_data['exfile_url_time']
        folder_time = datetime. strptime(folder_url_created.split('.')[0], '%Y-%m-%dT%H:%M:%S')
        print(folder_url_created)
        if folder_url_created is not None:
            time_delta = (datetime.now() - folder_time)
            total_time = time_delta.total_seconds() / 3600
            if total_time < 1:
                return Response({'link': folder_url})
        folder_path = export_data['exfile_path']
        access_token = 'd7ElXR2Sr-AAAAAAAAAAC2HC0qc45ss1TYhRYB4Jy6__NJU1jjGiffP7LlP_2rrf'
        dbx = dropbox.Dropbox(access_token)
        link = dbx.files_get_temporary_link(folder_path ).link
        request_data = {
            'exfile_isdownloaded': True,
            'exfile_url': link,
            'exfile_url_time': datetime.now()
        }
        requests.patch('http://13.232.166.20/create_export/'+ str(id) +'/', data=request_data).json()
        return Response({'link': link})
