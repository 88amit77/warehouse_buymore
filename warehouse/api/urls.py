from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from .warehouse.views import (
    WarehouseDetailsViewSet,
    WarehouseListCodeGetAPI,
    WarehouseListAddressGetAPI
)
from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter()
router.register(r'warehouse', WarehouseDetailsViewSet, basename='warehouse')
schema_view = get_swagger_view(title='Micromerce API')
urlpatterns = [
    path('', include(router.urls)),
    path("warehouse_code/", WarehouseListCodeGetAPI.as_view(), name='warehouse_code'),
    path("warehouse_address/", WarehouseListAddressGetAPI.as_view(), name='warehouse_address'),
    path("docs/", schema_view),
]
