# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from modulacion import FM
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
from .calculo_datos_senales import CalculoDatos


from django import forms


# Create your views here.
class View(View):
    def get(self, request):
        return render(request, 'modulacion/index.html', {})

class ModFMView(View):
    def post(self, request):
        req = request.POST
        #return HttpResponse(req['vmt'])
        FM = ModulacionFM(req['vmt'], req['vct'], 'Hz', 'Hz', float(req['kl']), float(req['fc']), float(req['fm']), float(req['vc']), float(req['vm']), noise=req['ruido'])
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
        e = EspectroFrecuencia.EspectroFrecuencia(float(req['m']), float(req['vc']), float(req['fc']), float(req['fm']))
        print(e)
        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = FM.get_portadora_str()
        datos['moduladora'] = FM.get_moduladora_str()
        datos['modulada'] = str(FM.modulada)
        datos['fm'] = FM.fm
        datos['fc'] = FM.fc
        datos['vm'] = FM.Vm
        return HttpResponse(JsonResponse(datos, safe=False))

class ModPMView(View):
    def post(self, request):
        req = request.POST
        PM = ModulacionPM(req['vmt'], req['vct'], 'Hz', 'Hz', float(req['kl']), float(req['fc']), float(req['fm']), float(req['vc']), float(req['vm']), noise=req['ruido'])
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
        e = EspectroFrecuencia.EspectroFrecuencia(PM.m, float(req['vc']), float(req['fc']), float(req['fm']))
        
        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = PM.get_portadora_str()
        datos['moduladora'] = PM.get_moduladora_str()
        datos['modulada'] = str(PM.modulada)
        datos['fm'] = PM.fm
        datos['fc'] = PM.fc
        datos['vm'] = PM.Vm
        return HttpResponse(JsonResponse(datos, safe=False))

#   /*      FM                                          PM
# a. Desviación de frecuencia.(Kl,vm)
#                                                 b. Desviación de fase.(K,vm)
#                                                 c. Desviación instantánea de fase.(k, Vm, fm, t, fun_moduladora)
# d. Desviación Instantánea de frecuencia.
# (kl, Vm, fm, t, fun_moduladora)
#
# e. Frecuencia instantánea.
# fc, kl, Vm, fm, t, fun_moduladora               f. Fase instantánea.fc, kl, Vm, fm, t, fun_moduladora
#
# g. Sensibilidad de desviación Kl                g. Sensibilidad de desviación K (variacion_fase, variacion_voltaje)
# (variacion_frecuencia, variacion_voltaje)
#
# h. Determinar el ancho de banda.                h. Determinar el ancho de banda.
# por bessel (n, fm)                                  por bessel (n, fm)
# por regla carson (variacion_frecuencia, fm)         por regla carson (variacion_frecuencia, fm)
# m_mayor10(variacion_frecuencia)                     m_mayor10(variacion_frecuencia)
# m_menor10(fm)                                       m_menor10(fm)
# */

class CalculoParametrosPMView(View):
    # k, Vm, fm, t, fun_moduladora, fc, variacion_fase, variacion_voltaje, n, variacion_frecuencia PARA PM
    def post(self, request):
        req = request.POST
        calculo_datos = {}
        calculo_datos['desv_fase'] = CalculoDatos.desviacion_frecuencia_fase(float(req['kl']), float(req['vm']))
        calculo_datos['desv_inst_fase'] = CalculoDatos.desviacion_instantanea_frecuencia_fase(float(req['kl']),
                                float(req['vm']), float(req['fm']), float(req['t']), req['vmt'])
        # calculo_datos['desv_inst_fase'] = CalculoDatos.desviacion_instantanea_frecuencia_fase(float(req['k']),
        #                         float(req['vm']), float(req['fm']), float(req['t']), req['fun_moduladora'])
        #
        calculo_datos['fase_inst'] = CalculoDatos.fase_instantanea(float(req['fc']), float(req['kl']), float(req['vm']),
                                    float(req['fm']), float(req['t']), req['vmt'])
        # calculo_datos['fase_inst'] = CalculoDatos.fase_instantanea(float(req['fc']), float(req['k']), float(req['vm']),
        #                             float(req['fm']), float(req['t']), req['fun_moduladora'])
        #
        calculo_datos['k'] = CalculoDatos.sensibilidad_k(calculo_datos['desv_fase'], float(req['dv']))
        # calculo_datos['k'] = CalculoDatos.sensibilidad_k(float(req['variacion_fase']), float(req['variacion_voltaje']))
        
        PM = ModulacionPM(req['vmt'], req['vct'], 'Hz', 'Hz', float(req['kl']), float(req['fc']), float(req['fm']), float(req['vc']), float(req['vm']), noise=req['ruido'])
        e = EspectroFrecuencia.EspectroFrecuencia(PM.m, float(req['vc']), float(req['fc']), float(req['fm']))

        calculo_datos['a_banda_bessel'] = CalculoDatos.ancho_banda_bessel(e.n, float(req['fm']))
        # calculo_datos['a_banda_bessel'] = CalculoDatos.ancho_banda_bessel(float(req['n']), float(req['fm']))
        calculo_datos['a_banda_carson'] = CalculoDatos.ancho_banda_regla_carson(float(req['df']),
                                                                                float(req['fm']))
        # calculo_datos['a_banda_carson'] = CalculoDatos.ancho_banda_regla_carson(float(req['variacion_frecuencia']),
        #                                                                         float(req['fm']))
        #
        return HttpResponse(JsonResponse(calculo_datos, safe=False))

# //kl, vm, fm, t, fun_moduladora, fc, variacion_voltaje, n, variacion_frecuencia PARA FM
class CalculoParametrosFMView(View):
    def post(self, request):
        req = request.POST
        calculo_datos = {}
        calculo_datos['desv_frecuencia'] = CalculoDatos.desviacion_frecuencia_fase(float(req['kl']), float(req['vm']))
        calculo_datos['desv_inst_frecuencia'] = CalculoDatos.desviacion_instantanea_frecuencia_fase(float(req['kl']),
                                                                                              float(req['vm']),
                                                                                              float(req['fm']),
                                                                                              float(req['t']),
                                                                                              req['vmt'])
        # calculo_datos['desv_inst_frecuencia'] = CalculoDatos.desviacion_instantanea_frecuencia_fase(float(req['kl']),
        #                                                                                       float(req['vm']),
        #                                                                                       float(req['fm']),
        #                                                                                       float(req['t']),
        #                                                                                       req['fun_moduladora'])
        #
        calculo_datos['frecuencia_inst'] = CalculoDatos.frecuencia_instantanea(float(req['fc']),
                                                                    float(req['kl']), float(req['vm']),
                                                                   float(req['fm']), float(req['t']),
                                                                   req['vmt'])
        # calculo_datos['frecuencia_inst'] = CalculoDatos.frecuencia_instantanea(float(req['fc']),
        #                                                             float(req['kl']), float(req['vm']),
        #                                                            float(req['fm']), float(req['t']),
        #                                                            req['fun_moduladora'])
        #
        calculo_datos['kl'] = CalculoDatos.sensibilidad_kl(float(req['dw']), float(req['dv']))
        # calculo_datos['kl'] = CalculoDatos.sensibilidad_kl(float(req['variacion_frecuencia']), float(req['variacion_voltaje']))
        FM = ModulacionFM(req['vmt'], req['vct'], 'Hz', 'Hz', float(req['kl']), float(req['fc']), float(req['fm']), float(req['vc']), float(req['vm']))
        e = EspectroFrecuencia.EspectroFrecuencia(FM.m, float(req['vc']), float(req['fc']), float(req['fm']))

        calculo_datos['a_banda_bessel'] = CalculoDatos.ancho_banda_bessel(e.n, float(req['fm']))
        # calculo_datos['a_banda_bessel'] = CalculoDatos.ancho_banda_bessel(float(req['n']), float(req['fm']))
        calculo_datos['a_banda_carson'] = CalculoDatos.ancho_banda_regla_carson(calculo_datos['desv_frecuencia'],
                                                                                float(req['fm']))
        # calculo_datos['a_banda_carson'] = CalculoDatos.ancho_banda_regla_carson(float(req['variacion_frecuencia']),
        #                                                                         float(req['fm']))
        #
        return HttpResponse(JsonResponse(calculo_datos, safe=False))

