import numpy as np #numeric
import sympy as sp #simbolic
from sympy import *

import utils
import ModulacionFM


#execfile('DemodulacionFM.py')
#obj = DemodulacionFM(Vc=5, fc=10, hzfc='KHz', fun_portadora='cos', fun_moduladora='cos', hzfm='KHz', m=50.13, fm=15, Vm=10)
class DemodulacionFM:

    def get_kl(self):
        return (self.m * self.fm_real) / self.Vm

    def get_Vm(self):
        return (self.m * self.fm_real) / self.kl

    def get_m(self):
        return (self.kl * self.Vm) / self.fm_real

    def __init__(self, Vc, fc, hzfc, fun_portadora, fun_moduladora, hzfm, fm, kl=None, Vm=None, m=None):

        self.moduladora = 0
        self.portadora = 0
        self.modulada = 0
        self.fun_portadora = fun_portadora
        self.fun_moduladora = fun_moduladora
        self.hzfc = hzfc
        self.hzfm = hzfm
        self.kl = kl
        self.fm_real = fm # fm por parametros
        self.m = m
        self.Vc = Vc
        self.Vm = Vm
        self.fc_real = fc  # fc por parametro
        self.t = Symbol('x')

        if m is not None and fm is not None and Vm is not None:
            self.kl = self.get_kl()

        elif m is not None and fm is not None and kl is not None:
            self.Vm = self.get_Vm()

        elif kl is not None and Vm is not None and fm is not None:
            self.m = self.get_m()

        self.fm = utils.conv_unidades_frecuencia(self.fm_real, self.hzfm)
        self.fc = utils.conv_unidades_frecuencia(self.fc_real, self.hzfc)

        self.wm = 2 * np.pi * self.fm
        self.wc = 2 * np.pi * self.fc

        self._demodula_funcion_fm()

    def _demodula_funcion_fm(self):
        self.moduladora = self.Vm * self.deriva_moduladora()

        sign = utils.signo_en_funcion(self.fun_portadora)
        funcion = utils.funcion_en_string(self.fun_portadora, self.wc, self.t)

        self.portadora = self.Vc * (sign * funcion)

        fun_moduladora = ''

        if self.fun_moduladora == 'sin' or self.fun_moduladora == 'sen':
            fun_moduladora = 'cos'
        elif self.fun_moduladora == '-sin' or self.fun_moduladora == '-sen':
            fun_moduladora = '-cos'
        elif self.fun_moduladora == 'cos':
            fun_moduladora = '-sen'
        elif self.fun_moduladora == '-cos':
            fun_moduladora = 'sen'

        self.modulada = ModulacionFM.ModulacionFM(fun_moduladora, self.fun_portadora, self.hzfm,
                                     self.hzfc, self.kl, self.fc, self.fm, self.Vc, self.Vm).modulada

        return {'moduladora': self.moduladora, 'portadora': self.portadora}

    def deriva_moduladora(self):
        funcion = utils.funcion_en_string(self.fun_moduladora, self.wm, self.t)
        signo = utils.signo_en_funcion(self.fun_moduladora)

        return sp.diff(signo * funcion, self.t)


    def get_portadora_str(self):
        return str(self.portadora)

    def get_moduladora_str(self):
        return str(self.moduladora)

    def get_modulada_str(self):
        return str(self.modulada)



