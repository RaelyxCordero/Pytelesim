from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .FM.ModulacionFM import ModulacionFM


from scipy import *
import random
import django
from django.http import *
import datetime
from .FM.ModulacionFM import ModulacionFM
#from .FM.DemodulacionFM import DemodulacionFM


from django import forms


# Create your views here.
class View(View):
    def get(self, request):
        return render(request, 'modulacion/index.html', {})

    def post(self, request):
        req = request.POST
        #return HttpResponse(req['vmt'])
        FM = ModulacionFM(req['vmt'], req['vct'], 'Hz', 'Hz', float(req['kl']), float(req['fc']), float(req['fm']), float(req['vc']), float(req['vm']))
        #fun_moduladora, fun_portadora, hz_fm, hz_fc, kl, fc, fm, vc, vm)
        datos = {}
        datos['portadora'] = FM.get_portadora_str()
        datos['moduladora'] = FM.get_moduladora_str()
        datos['modulada'] = FM.get_modulada_str()
        return HttpResponse(JsonResponse(datos, safe=False))