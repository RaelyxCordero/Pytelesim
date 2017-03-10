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
from .FM.utils import *
import sympy as sp #simbolic


from django import forms


# Create your views here.
class View(View):
    def get(self, request):
        return render(request, 'modulacion/index.html', {})

class ModFMView(View):
    def post(self, request):
        req = request.POST
        vmt = ''
        vm = ''

        if not if_signo_en_funcion(req['vm']):
            vm = req['vm'].replace("-", "")
            vmt = "-" + req['vmt']
        else:
            vmt = req['vmt']
            vm = req['vm']

        vct = ''
        vc = ''
        if not if_signo_en_funcion(req['vc']):
            vc = req['vc'].replace("-", "")
            vct = "-" + req['vct']
        else:
            vct = req['vct']
            vc = req['vc']

        FM = ModulacionFM(vmt, vct, 'Hz', 'Hz', float(req['kl']), float(req['fc']), float(req['fm']), float(vc), float(vm), noise=req['ruido'])
        datos = {}
        espectro = {}

        if if_saw(FM.fun_portadora):
            vc = FM.Vc_sierra
        else:
            vc = FM.Vc

        e = EspectroFrecuencia.EspectroFrecuencia(FM.m, vc, float(req['fc']), float(req['fm']))
        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = FM.get_portadora_str()
        datos['moduladora'] = FM.get_moduladora_str()
        datos['modulada'] = FM.get_modulada_str()
        datos['kl_modulada'] = FM.kl
        datos['m_modulada'] = FM.m
        datos['vc'] = vc

        funcion = integra_string_moduladora(FM.fun_moduladora)
        datos['signo'] = if_signo_en_funcion(funcion)

        if 'cos' in funcion:
            datos['vmt'] = 'cos'
        elif 'sin' in funcion or 'sen' in funcion:
            datos['vmt'] = 'sin'
        
        return HttpResponse(JsonResponse(datos, safe=False))


class ModPMView(View):
    def post(self, request):
        req = request.POST
        vmt = ''
        vm = ''

        if not if_signo_en_funcion(req['vm']):
            vm = req['vm'].replace("-", "")
            vmt = "-" + req['vmt']
        else:
            vmt = req['vmt']
            vm = req['vm']

        vct = ''
        vc = ''
        if not if_signo_en_funcion(req['vc']):
            vc = req['vc'].replace("-", "")
            vct = "-" + req['vct']
        else:
            vct = req['vct']
            vc = req['vc']

        PM = ModulacionPM(vmt, vct, 'Hz', 'Hz', float(req['kl']), float(req['fc']), float(req['fm']),
                          float(vc), float(vm), noise=req['ruido'])

        if if_saw(PM.fun_portadora):
            vc = PM.Vc_sierra
        else:
            vc = PM.Vc

        datos = {}
        espectro = {}
        e = EspectroFrecuencia.EspectroFrecuencia(PM.m, vc, float(req['fc']), float(req['fm']))

        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = PM.get_portadora_str()
        datos['moduladora'] = PM.get_moduladora_str()
        datos['modulada'] = PM.get_modulada_str()
        datos['k_modulada'] = PM.k
        datos['m_modulada'] = PM.m
        datos['vc'] = vc

        funcion = PM.fun_moduladora
        datos['signo'] = if_signo_en_funcion(funcion)

        return HttpResponse(JsonResponse(datos, safe=False))


class DemodFMView(View):
    def post(self, request):
        req = request.POST
        FM = DemodulacionFM(Vc=float(req['vc']), fc=float(req['fc']), hzfc='Hz', fun_portadora=req['vct'],
                            fun_moduladora=req['vmt'], hzfm='Hz', fm=float(req['fm']), kl=float(req['kl']), m=float(req['m']))

        if if_saw(FM.fun_portadora):
            vc = FM.Vc_sierra
        else:
            vc = FM.Vc

        datos = {}
        espectro = {}
        e = EspectroFrecuencia.EspectroFrecuencia(float(req['m']), vc, float(req['fc']), float(req['fm']))
        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = FM.get_portadora_str()
        datos['moduladora'] = FM.get_moduladora_str()
        datos['modulada'] = FM.get_modulada_str()
        datos['fm'] = FM.fm
        datos['fc'] = FM.fc
        datos['vm'] = FM.Vm
        datos['vct'] = FM.fun_portadora
        datos['vc'] = vc

        funcion = deriva_string_moduladora(FM.fun_moduladora)

        datos['signo'] = if_signo_en_funcion(funcion)

        if 'cos' in funcion:
            datos['vmt'] = 'cos'
        elif 'sin' in funcion or 'sen' in funcion:
            datos['vmt'] = 'sin'


        return HttpResponse(JsonResponse(datos, safe=False))


class DemodPMView(View):
    def post(self, request):
        # Vc, fc, hzfc,  fun_portadora, fun_moduladora, hzfm, fm, k, m
        req = request.POST
        print(req)
        PM = DemodulacionPM(float(req['vc']), float(req['fc']), 'Hz', req['vct'], req['vmt'], 'Hz', float(req['fm']), float(req['kl']), m=float(req['m']))
        datos = {}
        espectro = {}
        e = EspectroFrecuencia.EspectroFrecuencia(PM.m, float(req['vc']), float(req['fc']), float(req['fm']))
        
        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = PM.get_portadora_str()
        datos['moduladora'] = PM.get_moduladora_str()
        datos['modulada'] = PM.get_modulada_str()
        datos['fm'] = PM.fm
        datos['fc'] = PM.fc
        datos['vm'] = PM.Vm

        datos['signo'] = if_signo_en_funcion(PM.fun_moduladora)

        if 'cos' in PM.fun_moduladora:
            datos['vmt'] = 'cos'
        elif 'sin' in PM.fun_moduladora or 'sen' in PM.fun_moduladora:
            datos['vmt'] = 'sin'

        return HttpResponse(JsonResponse(datos, safe=False))

# EN LOS CALCULOS RECIBIR TODO COMO VALOR ABSOLUTO

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
    def post(self, request):
        req = request.POST
        vm = ''
        vmt = ''

        if not if_signo_en_funcion(req['vm']):
            vm = req['vm'].replace("-", "")
            vmt = "-" + req['vmt']
        else:
            vm = req['vm']
            vmt = req['vmt']



        variacion_voltaje = CalculoDatos.variacion_voltaje_fase(float(req['kl']), float(vm))
        variacion_frecuencia = CalculoDatos.desviacion_frecuencia_fase(float(req['kl']), float(vm))

        calculo_datos = {}
        calculo_datos['desv_fase'] = CalculoDatos.desviacion_frecuencia_fase(float(req['kl']), float(vm))
        calculo_datos['desv_voltaje'] = variacion_voltaje
        calculo_datos['desv_frecuencia'] = variacion_frecuencia
        calculo_datos['desv_inst_fase'] = CalculoDatos.desviacion_instantanea_frecuencia_fase(float(req['kl']),
                                float(vm), float(req['fm']), float(req['t']), req['vmt'])
        #
        calculo_datos['fase_inst'] = CalculoDatos.fase_instantanea(float(req['fc']), float(req['kl']), float(vm),
                                    float(req['fm']), float(req['t']), req['vmt'])
        #
        calculo_datos['k'] = CalculoDatos.sensibilidad_k(calculo_datos['desv_fase'], variacion_voltaje)


        vc = ''
        vct = ''

        if not if_signo_en_funcion(req['vc']):
            vc = req['vc'].replace("-", "")
            vct = "-" + req['vct']
        else:
            vct = req['vct']
            vc = req['vc']

        PM = ModulacionPM(vmt, vct, 'Hz', 'Hz', float(req['kl']), float(req['fc']),
                          float(req['fm']), float(vc), float(vm))
        e = EspectroFrecuencia.EspectroFrecuencia(PM.m, float(vc), float(req['fc']), float(req['fm']))

        calculo_datos['a_banda_bessel'] = CalculoDatos.ancho_banda_bessel(e.n, float(req['fm']))
        calculo_datos['a_banda_carson'] = CalculoDatos.ancho_banda_regla_carson(variacion_frecuencia,
                                                                                float(req['fm']))
        #
        return HttpResponse(JsonResponse(calculo_datos, safe=False))

class CalculoParametrosFMView(View):
    def post(self, request):
        req = request.POST

        vm = ''
        vmt = ''

        if not if_signo_en_funcion(req['vm']):
            vm = req['vm'].replace("-", "")
            vmt = "-" + req['vmt']
        else:
            vm = req['vm']
            vmt = req['vmt']

        variacion_voltaje = CalculoDatos.variacion_voltaje_frecuencia(float(req['kl']), float(vm))
        variacion_angular = CalculoDatos.variacion_angular(float(req['kl']), float(vm))

        calculo_datos = {}
        calculo_datos['desv_frecuencia'] = CalculoDatos.desviacion_frecuencia_fase(float(req['kl']), float(vm))
        calculo_datos['desv_voltaje'] = variacion_voltaje
        calculo_datos['desv_angular'] = variacion_angular
        calculo_datos['desv_inst_frecuencia'] = CalculoDatos.desviacion_instantanea_frecuencia_fase(float(req['kl']),
                                                                                              float(vm),
                                                                                              float(req['fm']),
                                                                                              float(req['t']),
                                                                                              req['vmt'])

        calculo_datos['frecuencia_inst'] = CalculoDatos.frecuencia_instantanea(float(req['fc']),
                                                                    float(req['kl']), float(req['vm']),
                                                                   float(req['fm']), float(req['t']),
                                                                   req['vmt'])

        calculo_datos['kl'] = CalculoDatos.sensibilidad_kl(variacion_angular, variacion_voltaje)

        vc = ''
        vct = ''

        if not if_signo_en_funcion(req['vc']):
            vc = req['vc'].replace("-", "")
            vct = "-" + req['vct']
        else:
            vct = req['vct']
            vc = req['vc']

        FM = ModulacionFM(vmt, vct, 'Hz', 'Hz', float(req['kl']), float(req['fc']),
                          float(req['fm']), float(vc), float(vm))
        e = EspectroFrecuencia.EspectroFrecuencia(FM.m, float(vc), float(req['fc']), float(req['fm']))

        calculo_datos['a_banda_bessel'] = CalculoDatos.ancho_banda_bessel(e.n, float(req['fm']))
        calculo_datos['a_banda_carson'] = CalculoDatos.ancho_banda_regla_carson(calculo_datos['desv_frecuencia'],
                                                                                float(req['fm']))
        return HttpResponse(JsonResponse(calculo_datos, safe=False))

