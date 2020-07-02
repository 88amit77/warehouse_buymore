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
    WarehouseGstFilterView,
    WarehouseSelectView,
    GetDropboxFile
)
from .picklist.views import (
    PicklistView,
    PicklistItemsView,
    PicklistItemAlternateView,
    PicklistAssigneeView,
    CreatePicklist,
    AssignPicklist,
    ListPicklist,
    PicklistProcessingMonitorView,
    PicklistItemProcessingView,
    PicklistItemCollectView,
    PicklistCheckView,
    PicklistProcessingFnskuCheck,
    SizeCorrectness,
    LabelCorrectness,
    ImageCorrectness,
    DimensionCorrectness,
    Status,
    ProductCondition,
    BarcodeGenerator
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

router = routers.DefaultRouter()
router.register(r'warehouse/warehouse', WarehouseDetailsViewSet, basename='warehouse')
router.register(r'warehouse/warehouses', WarehouseQueryViewSet, basename='warehouses')

router.register(r'warehouse/picklist', PicklistView)
router.register(r'warehouse/picklist_items', PicklistItemsView)
router.register(r'warehouse/picklist_item_alternative', PicklistItemAlternateView)
router.register(r'warehouse/picklist_item_assignee', PicklistAssigneeView)
router.register(r'warehouse/picklist_item_processing', PicklistItemProcessingView)
router.register(r'warehouse/picklist_processing_monitor', PicklistProcessingMonitorView)

schema_view = get_schema_view(openapi.Info(
    title="Warehouse API",
    default_version='v1',
    description="Test description",
), public=True, permission_classes=(permissions.AllowAny,))
urlpatterns = [
    path('', include(router.urls)),
    path("warehouse/warehouse_code_filter/", WarehouseListCodeGetAPI.as_view(), name='warehouse_code'),
    path("warehouse/warehouse_address_filter/", WarehouseListAddressGetAPI.as_view(), name='warehouse_address'),
    path("warehouse/list_warehouse/", WarehouseListView.as_view(), name='list_warehouse'),
    path("warehouse/warehouse_id/", WarehouseIdFilterView.as_view(), name='warehouse_id'),
    path("warehouse/warehouse_code/", WarehouseCodeFilterView.as_view(), name='warehouse_code_filter'),
    path("warehouse/warehouse_address/", WarehouseAddressFilterView.as_view(), name='warehouse_address_filter'),
    path("warehouse/warehouse_select/", WarehouseSelectView.as_view(), name='warehouse_select'),
    path("warehouse/city/", WarehouseCityFilterView.as_view(), name='city'),
    path("warehouse/pincode/", WarehousePincodeFilterView.as_view(), name='pincode'),
    path("warehouse/state/", WarehouseStateFilterView.as_view(), name='state'),
    path("warehouse/gst_number/", WarehouseGstFilterView.as_view(), name='gst_number'),
    path('warehouse/create_picklist/', CreatePicklist.as_view(), name='create_picklist'),
    path('warehouse/list_picklist/', ListPicklist.as_view(), name='list_picklist'),
    path('warehouse/assign_picklist/', AssignPicklist.as_view(), name='assign_picklist'),
    path('warehouse/picklistitem_collect/', PicklistItemCollectView.as_view(), name='picklistitem_collect'),
    path('warehouse/picklist_check/', PicklistCheckView.as_view(), name='picklist_check'),
    path('warehouse/picklist_processing/', PicklistProcessingFnskuCheck.as_view(), name='picklist_processing'),
    path('warehouse/size_correctness/', SizeCorrectness.as_view(), name='size_correctness'),
    path('warehouse/label_correctness/', LabelCorrectness.as_view(), name='size_correctness'),
    path('warehouse/dimension_correctness/', DimensionCorrectness.as_view(), name='size_correctness'),
    path('warehouse/image_correctness/', ImageCorrectness.as_view(), name='image_correctness'),
    path('warehouse/product_condition/', ProductCondition.as_view(), name='product_condition'),
    path('warehouse/get_barcode/', BarcodeGenerator.as_view(), name='get_barcode'),
    path('warehouse/get_temp_link/', GetDropboxFile.as_view(), name='get_temp_link'),
    path('warehouse/status/', Status.as_view(), name='status'),
    path("warehouse/docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
urlpatterns += staticfiles_urlpatterns()
