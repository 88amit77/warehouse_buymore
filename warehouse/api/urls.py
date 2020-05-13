from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
	path('', include(router.urls)),
	path("docs/", schema_view),
]
