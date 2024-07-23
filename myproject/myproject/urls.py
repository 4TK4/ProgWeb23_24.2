"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
#from django.conf.urls import include in teoria non serve
from myapp import views

urlpatterns = [
    #è buona norma inserire un "/" in coda all'url
    
    path('admin/', admin.site.urls), #configurazione per l'url dell'amministrazione di Django
    
    path("", views.home, name="index"),

    path("contrattoTelefonico/", views.contrattoTelefonico, name="contrattoTelefonico"),

    path("sim/", views.sim, name="sim"),

    path("telefonata/", views.telefonata, name="telefonata"),
    
    path('modifica_contratto/', views.modifica_contratto, name='modifica_contratto'),
    
    path('inserisci_contratto/', views.inserisci_contratto, name='inserisci_contratto'),
    path('inserimento_successo/', views.inserimento_successo, name='inserimento_successo'),
    
    path('elimina_contratto/<int:numero>/', views.elimina_contratto, name='elimina_contratto'),

]
