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
    WarehouseSelectView
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
    GeneratePicklist
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = routers.DefaultRouter()
router.register(r'warehouse', WarehouseDetailsViewSet, basename='warehouse')
router.register(r'warehouses', WarehouseQueryViewSet, basename='warehouses')

router.register(r'picklist', PicklistView)
router.register(r'picklist_items', PicklistItemsView)
router.register(r'picklist_item_alternative', PicklistItemAlternateView)
router.register(r'picklist_item_assignee', PicklistAssigneeView)
router.register(r'picklist_item_processing', PicklistItemProcessingView)
router.register(r'picklist_processing_monitor', PicklistProcessingMonitorView)

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
    path("warehouse_select/", WarehouseSelectView.as_view(), name='warehouse_select'),
    path("city/", WarehouseCityFilterView.as_view(), name='city'),
    path("pincode/", WarehousePincodeFilterView.as_view(), name='pincode'),
    path("state/", WarehouseStateFilterView.as_view(), name='state'),
    path("gst_number/", WarehouseGstFilterView.as_view(), name='gst_number'),
    path('create_picklist/', CreatePicklist.as_view(), name='create_picklist'),
    path('list_picklist/', ListPicklist.as_view(), name='list_picklist'),
    path('assign_picklist/', AssignPicklist.as_view(), name='assign_picklist'),
    path('picklistitem_collect/', PicklistItemCollectView.as_view(), name='picklistitem_collect'),
    path('picklist_check/', PicklistCheckView.as_view(), name='picklist_check'),
    path('picklist_processing/', PicklistProcessingFnskuCheck.as_view(), name='picklist_processing'),
    path('size_correctness/', SizeCorrectness.as_view(), name='size_correctness'),
    path('label_correctness/', LabelCorrectness.as_view(), name='size_correctness'),
    path('dimension_correctness/', DimensionCorrectness.as_view(), name='size_correctness'),
    path('image_correctness/', ImageCorrectness.as_view(), name='image_correctness'),
    path('product_condition/', ProductCondition.as_view(), name='product_condition'),
    path('status/', Status.as_view(), name='status'),
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

