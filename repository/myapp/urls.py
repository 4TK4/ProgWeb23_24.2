from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from . import views
from . import myController

urlpatterns = [
    path('', myController.index2, name='index'),
     path("paramsToJson", myController.paramsToJson, name="paramsToJson")
]