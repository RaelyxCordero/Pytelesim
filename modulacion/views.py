from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .FM.ModulacionFM import ModulacionFM


from scipy import *
import random
import django
import datetime
from .FM.ModulacionFM import ModulacionFM
#from .FM.DemodulacionFM import DemodulacionFM


from django import forms


# Create your views here.
class View(View):
    def get(self, request):
        return render(request, 'modulacion/index.html', {})

    def put(self, request):
        return request