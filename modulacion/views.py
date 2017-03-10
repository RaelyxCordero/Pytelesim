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

        print(req)

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

        # (val, unid)

        fm = string_frecuencia_separated(req['fm'].lower())
        fc = string_frecuencia_separated(req['fc'].lower())
        #                     fun_moduladora, fun_portadora, hz_fm, hz_fc, kl, fc, fm, vc, vm,
        FM = ModulacionFM(vmt, vct, fm[1], fc[1], float(req['kl']), float(fc[0]), float(fm[0]), float(vc), float(vm), noise=req['ruido'])
        datos = {}
        espectro = {}

        if if_saw(FM.fun_portadora):
            vc = FM.Vc_sierra
        else:
            vc = FM.Vc

        e = EspectroFrecuencia.EspectroFrecuencia(FM.m, vc, FM.fc, FM.fm)
        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = FM.get_portadora_str()
        datos['moduladora'] = FM.get_moduladora_str()
        datos['modulada'] = FM.get_modulada_str()
        datos['kl_modulada'] = FM.kl
        datos['m_modulada'] = FM.m
        datos['vc'] = vc
        datos['fm'] = FM.fm
        datos['fc'] = FM.fc

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

        fm = string_frecuencia_separated(req['fm'].lower())
        fc = string_frecuencia_separated(req['fc'].lower())

        PM = ModulacionPM(vmt, vct, fm[1], fc[1], float(req['kl']), fc[0], fm[0],
                          float(vc), float(vm), noise=req['ruido'])

        if if_saw(PM.fun_portadora):
            vc = PM.Vc_sierra
        else:
            vc = PM.Vc

        datos = {}
        espectro = {}
        e = EspectroFrecuencia.EspectroFrecuencia(PM.m, vc, PM.fc, PM.fm)

        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = PM.get_portadora_str()
        datos['moduladora'] = PM.get_moduladora_str()
        datos['modulada'] = PM.get_modulada_str()
        datos['k_modulada'] = PM.k
        datos['m_modulada'] = PM.m
        datos['vc'] = vc
        datos['fm'] = PM.fm
        datos['fc'] = PM.fc

        funcion = PM.fun_moduladora
        datos['signo'] = if_signo_en_funcion(funcion)

        return HttpResponse(JsonResponse(datos, safe=False))


class DemodFMView(View):
    def post(self, request):
        req = request.POST

        fm = string_frecuencia_separated(req['fm'].lower())
        fc = string_frecuencia_separated(req['fc'].lower())

        FM = DemodulacionFM(Vc=float(req['vc']), fc=fc[0], hzfc=fc[1], fun_portadora=req['vct'],
                            fun_moduladora=req['vmt'], hzfm=fm[1], fm=fm[0], kl=float(req['kl']), m=float(req['m']))

        if if_saw(FM.fun_portadora):
            vc = FM.Vc_sierra
        else:
            vc = FM.Vc

        datos = {}
        espectro = {}
        e = EspectroFrecuencia.EspectroFrecuencia(FM.m, vc, FM.fc, FM.fm)
        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = FM.get_portadora_str()
        datos['moduladora'] = FM.get_moduladora_str()
        datos['modulada'] = FM.get_modulada_str()
        datos['fm'] = req['fm']
        datos['fc'] = req['fc']
        datos['vm'] = FM.Vm
        datos['vct'] = FM.fun_portadora
        datos['vc'] = vc
        datos['fm_real'] = FM.fm
        datos['fc_real'] = FM.fc

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

        fm = string_frecuencia_separated(req['fm'].lower())
        fc = string_frecuencia_separated(req['fc'].lower())

        # Vc, fc, hzfc,  fun_portadora, fun_moduladora, hzfm, fm, k, m

        PM = DemodulacionPM(float(req['vc']), fc[0], fc[1], req['vct'], req['vmt'], fm[1], fm[0], float(req['kl']), m=float(req['m']))
        datos = {}
        espectro = {}
        e = EspectroFrecuencia.EspectroFrecuencia(PM.m, float(req['vc']), PM.fc, PM.fm)
        
        espectro['amplitudes'] = e.get_amplitudes_espectros()
        espectro['frecuencias'] = e.get_frecuencias_espectros()
        datos['espectro'] = espectro
        datos['portadora'] = PM.get_portadora_str()
        datos['moduladora'] = PM.get_moduladora_str()
        datos['modulada'] = PM.get_modulada_str()
        datos['fm'] = req['fm']
        datos['fc'] = req['fc']
        datos['vm'] = PM.Vm
        datos['fm_real'] = PM.fm
        datos['fc_real'] = PM.fc

        datos['signo'] = if_signo_en_funcion(PM.fun_moduladora)

        if 'cos' in PM.fun_moduladora:
            datos['vmt'] = 'cos'
        elif 'sin' in PM.fun_moduladora or 'sen' in PM.fun_moduladora:
            datos['vmt'] = 'sin'

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

        fm = string_frecuencia_separated(req['fm'].lower())
        fc = string_frecuencia_separated(req['fc'].lower())

        vc = ''
        vct = ''

        if not if_signo_en_funcion(req['vc']):
            vc = req['vc'].replace("-", "")
            vct = "-" + req['vct']
        else:
            vct = req['vct']
            vc = req['vc']

        PM = ModulacionPM(vmt, vct, fm[1], fc[1], float(req['kl']), fc[0],
                          fm[0], float(vc), float(vm))
        e = EspectroFrecuencia.EspectroFrecuencia(PM.m, float(vc), PM.fc, PM.fm)

        variacion_voltaje = CalculoDatos.variacion_voltaje_fase(float(req['kl']), float(vm))
        variacion_frecuencia = CalculoDatos.desviacion_frecuencia_fase(float(req['kl']), float(vm))

        calculo_datos = {}
        calculo_datos['desv_fase'] = CalculoDatos.desviacion_frecuencia_fase(float(req['kl']), float(vm))
        calculo_datos['desv_voltaje'] = variacion_voltaje
        calculo_datos['desv_frecuencia'] = variacion_frecuencia
        calculo_datos['desv_inst_fase'] = CalculoDatos.desviacion_instantanea_frecuencia_fase(float(req['kl']),
                                float(vm), PM.fm, float(req['t']), req['vmt'])
        #
        calculo_datos['fase_inst'] = CalculoDatos.fase_instantanea(fc[0], float(req['kl']), float(vm),
                                    PM.fm, float(req['t']), req['vmt'])
        #
        calculo_datos['k'] = CalculoDatos.sensibilidad_k(calculo_datos['desv_fase'], variacion_voltaje)




        calculo_datos['a_banda_bessel'] = CalculoDatos.ancho_banda_bessel(e.n, PM.fm)
        calculo_datos['a_banda_carson'] = CalculoDatos.ancho_banda_regla_carson(variacion_frecuencia,
                                                                                PM.fm)
        #
        return HttpResponse(JsonResponse(calculo_datos, safe=False))

class CalculoParametrosFMView(View):
    def post(self, request):
        req = request.POST

        fm = string_frecuencia_separated(req['fm'].lower())
        fc = string_frecuencia_separated(req['fc'].lower())

        vm = ''
        vmt = ''

        if not if_signo_en_funcion(req['vm']):
            vm = req['vm'].replace("-", "")
            vmt = "-" + req['vmt']
        else:
            vm = req['vm']
            vmt = req['vmt']

        vc = ''
        vct = ''

        if not if_signo_en_funcion(req['vc']):
            vc = req['vc'].replace("-", "")
            vct = "-" + req['vct']
        else:
            vct = req['vct']
            vc = req['vc']

        FM = ModulacionFM(vmt, vct, fm[1], fc[1], float(req['kl']), fc[0], fm[0], float(vc), float(vm))
        e = EspectroFrecuencia.EspectroFrecuencia(FM.m, float(vc), FM.fc, FM.fm)

        variacion_voltaje = CalculoDatos.variacion_voltaje_frecuencia(float(req['kl']), float(vm))
        variacion_angular = CalculoDatos.variacion_angular(float(req['kl']), float(vm))

        calculo_datos = {}
        calculo_datos['desv_frecuencia'] = CalculoDatos.desviacion_frecuencia_fase(float(req['kl']), float(vm))
        calculo_datos['desv_voltaje'] = variacion_voltaje
        calculo_datos['desv_angular'] = variacion_angular
        calculo_datos['desv_inst_frecuencia'] = CalculoDatos.desviacion_instantanea_frecuencia_fase(float(req['kl']),
                                                                                              float(vm),
                                                                                              FM.fm,
                                                                                              float(req['t']),
                                                                                              req['vmt'])

        calculo_datos['frecuencia_inst'] = CalculoDatos.frecuencia_instantanea(FM.fc,
                                                                    float(req['kl']), float(req['vm']),
                                                                   FM.fm, float(req['t']),
                                                                   req['vmt'])

        calculo_datos['kl'] = CalculoDatos.sensibilidad_kl(variacion_angular, variacion_voltaje)





        calculo_datos['a_banda_bessel'] = CalculoDatos.ancho_banda_bessel(e.n, FM.fm)
        calculo_datos['a_banda_carson'] = CalculoDatos.ancho_banda_regla_carson(calculo_datos['desv_frecuencia'],
                                                                                FM.fm)
        return HttpResponse(JsonResponse(calculo_datos, safe=False))

