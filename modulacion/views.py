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
from .FM.DemodulacionFM import DemodulacionFM
from .PM.ModulacionPM import ModulacionPM
from .PM.DemodulacionPM import DemodulacionPM
from .espectros_de_frecuencia import EspectroFrecuencia


from django import forms


# Create your views here.
class View(View):
    def get(self, request):
        return render(request, 'modulacion/index.html', {})

class ModFMView(View):
    def post(self, request):
        req = request.POST
        #return HttpResponse(req['vmt'])
        FM = ModulacionFM(req['vmt'], req['vct'], 'Hz', 'Hz', float(req['kl']), float(req['fc']), float(req['fm']), float(req['vc']), float(req['vm']))
        #fun_moduladora, fun_portadora, hz_fm, hz_fc, kl, fc, fm, vc, vm)
        
        datos = {}
        espectro = {}
        e = EspectroFrecuencia.EspectroFrecuencia(FM.m, float(req['vc']), float(req['fc']), float(req['fm']))
        print("M:"+str(e.m))
        print(e.Vc)
        print(e.fc)
        print(e.fm)
        print(e.n)
        print(e.get_indices_bessel())
        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = FM.get_portadora_str()
        datos['moduladora'] = FM.get_moduladora_str()
        datos['modulada'] = FM.get_modulada_str()
        
        return HttpResponse(JsonResponse(datos, safe=False))

class DemodFMView(View):
    def post(self, request):
        req = request.POST
        FM = DemodulacionFM(float(req['vc']), float(req['fc']), 'Hz', req['vct'], req['vmt'], 'Hz', float(req['kl']), float(req['fm']), m=float(req['m']))
        #(self, Vc, fc, hzfc,  fun_portadora, fun_moduladora, hzfm, kl=None, fm=None, Vm=None, m=None):
        
        datos = {}
        espectro = {}
        e = EspectroFrecuencia.EspectroFrecuencia(FM.m, float(req['vc']), float(req['fc']), float(req['fm']))
        print(e)
        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = FM.get_portadora_str()
        datos['moduladora'] = FM.get_moduladora_str()
        datos['modulada'] = str(FM.modulada)
        return HttpResponse(JsonResponse(datos, safe=False))

class ModPMView(View):
    def post(self, request):
        req = request.POST
        PM = ModulacionPM(req['vmt'], req['vct'], 'Hz', 'Hz', float(req['kl']), float(req['fc']), float(req['fm']), float(req['vc']), float(req['vm']))
        #(self, fun_moduladora, fun_portadora, hz_fm, hz_fc, k, fc, fm, vc, vm)
        datos = {}
        espectro = {}
        e = EspectroFrecuencia.EspectroFrecuencia(PM.m, float(req['vc']), float(req['fc']), float(req['fm']))
        
        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = PM.get_portadora_str()
        datos['moduladora'] = PM.get_moduladora_str()
        datos['modulada'] = PM.get_modulada_str()
        return HttpResponse(JsonResponse(datos, safe=False))

class DemodPMView(View):
    def post(self, request):
        req = request.POST
        PM = DemodulacionPM(float(req['vc']), float(req['fc']), 'Hz', req['vct'], req['vmt'], 'Hz', float(req['fm']), float(req['kl']), m=float(req['m']))
        #self, Vc, fc, hzfc,  fun_portadora, fun_moduladora, hzfm, fm, k=None,  Vm=None, m=None
        datos = {}
        espectro = {}
        e = EspectroFrecuencia.EspectroFrecuencia(FM.m, float(req['vc']), float(req['fc']), float(req['fm']))
        
        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = PM.get_portadora_str()
        datos['moduladora'] = PM.get_moduladora_str()
        datos['modulada'] = str(PM.modulada)
        return HttpResponse(JsonResponse(datos, safe=False))
        
        