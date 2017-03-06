"""Pytelesim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from modulacion.views import View
from modulacion.views import ModFMView
from modulacion.views import DemodFMView
from modulacion.views import ModPMView
from modulacion.views import DemodPMView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', View.as_view()),
    url(r'^modulate-fm/$', ModFMView.as_view()),
    url(r'^demodulate-fm/$',DemodFMView.as_view()),
    url(r'^modulate-pm/$', ModPMView.as_view()),
    url(r'^demodulate-pm/$',DemodPMView.as_view())
]
