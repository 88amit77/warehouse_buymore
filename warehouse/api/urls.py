from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from .warehouse.views import WarehouseDetailsViewSet
from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter()
router.register(r'warehouse', WarehouseDetailsViewSet, basename='warehouse')
schema_view = get_swagger_view(title='Micromerce API')
urlpatterns = [
    path('', include(router.urls)),
    path("docs/", schema_view),
]
print(router.urls)
