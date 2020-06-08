from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from .warehouse.views import (
    WarehouseDetailsViewSet,
    WarehouseListCodeGetAPI,
    WarehouseListAddressGetAPI,
    WarehouseListView,
    WarehouseQueryViewSet,
    WarehouseIdFilterView,
    WarehouseCodeFilterView,
    WarehouseAddressFilterView,
    WarehouseCityFilterView,
    WarehousePincodeFilterView,
    WarehouseStateFilterView,
    WarehouseGstFilterView
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = routers.DefaultRouter()
router.register(r'warehouse', WarehouseDetailsViewSet, basename='warehouse')
router.register(r'warehouses', WarehouseQueryViewSet, basename='warehouses')
schema_view = get_schema_view(openapi.Info(
    title="Warehouse API",
    default_version='v1',
    description="Test description",
), public=True, permission_classes=(permissions.AllowAny,))
urlpatterns = [
    path('', include(router.urls)),
    path("warehouse_code_filter/", WarehouseListCodeGetAPI.as_view(), name='warehouse_code'),
    path("warehouse_address_filter/", WarehouseListAddressGetAPI.as_view(), name='warehouse_address'),
    path("list_warehouse/", WarehouseListView.as_view(), name='list_warehouse'),
    path("warehouse_id/", WarehouseIdFilterView.as_view(), name='warehouse_id'),
    path("warehouse_code/", WarehouseCodeFilterView.as_view(), name='warehouse_code_filter'),
    path("warehouse_address/", WarehouseAddressFilterView.as_view(), name='warehouse_address_filter'),
    path("city/", WarehouseCityFilterView.as_view(), name='city'),
    path("pincode/", WarehousePincodeFilterView.as_view(), name='pincode'),
    path("state/", WarehouseStateFilterView.as_view(), name='state'),
    path("gst_number/", WarehouseGstFilterView.as_view(), name='gst_number'),
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
