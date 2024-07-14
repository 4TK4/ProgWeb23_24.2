"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import myController
urlpatterns= [
    path("", myController.home,  #fa il binding dell'URL a cui appendiamo la stringa vuota e il controller home
    name="index"),

    path("contrattoTelefonico", myController.contrattoTelefonico, name="contrattoTelefonico"),

    path("sim", myController.sim, name="sim"),

     path("telefonata", myController.telefonata, name="telefonata")
]
