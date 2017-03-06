import numpy as np #numeric
import sympy as sp #simbolic
from sympy import *

from . import utils
from .ModulacionFM import ModulacionFM


#execfile('DemodulacionFM.py')
#obj = DemodulacionFM(5, 10, 'KHz', 'cos', 'cos', 'KHz', m=50.13, fm=15, Vm=10)
class DemodulacionFM:
    def get_fm(self):
        return (self.kl * self.Vm)/ self.m

    def get_kl(self):
        return (self.m * self.fm_real) / self.Vm

    def get_Vm(self):
        return (self.m * self.fm_real) / self.kl

    def get_m(self):
        return (self.kl * self.Vm) / self.fm_real

    def __init__(self, Vc, fc, hzfc,  fun_portadora, fun_moduladora, hzfm, kl=None, fm=None, Vm=None, m=None):

        self.moduladora = 0
        self.portadora = 0
        self.modulada = 0
        self.fun_portadora = fun_portadora
        self.fun_moduladora = fun_moduladora
        self.hzfc = hzfc
        self.hzfm = hzfm
        self.kl = kl
        self.fm_real = fm
        self.m = m
        self.Vc = Vc
        self.Vm = Vm
        self.fc_real = fc  # fc por parametro
        self.t = Symbol('x')

        if kl is not None and Vm is not None and m is not None:
            self.fm_real = self.get_fm() # fm por parametros

        elif m is not None and fm is not None and Vm is not None:
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
        if self.fun_moduladora == 'cos':
            self.portadora = self.Vc * sp.cos(self.wc*self.t)

        elif self.fun_moduladora == 'sen' or self.fun_moduladora == 'sin':
            self.portadora = self.Vc * sp.sin(self.wc * self.t)

        self.modulada = ModulacionFM(self.fun_moduladora, self.fun_portadora, self.hzfm,
                                     self.hzfc, self.kl, self.fc, self.fm, self.Vc, self.Vm)

        return {'moduladora': self.moduladora, 'portadora': self.portadora}

    def deriva_moduladora(self):
        funcion = 0
        if self.fun_moduladora == 'cos':
            funcion = sp.cos(self.wm*self.t)

        elif self.fun_moduladora == 'sen' or self.fun_moduladora == 'sin':
            funcion = sp.sin(self.wm * self.t)

        return sp.diff(funcion, self.t)

    def get_portadora_str(self):
        return str(self.portadora)
        # return utils.get_string_portadora(self.fc_real, self.hzfc, self.Vc, self.fun_portadora)

    def get_moduladora_str(self):
        return str(self.moduladora)
        # return utils.get_string_moduladora(self.fm_real, self.hzfm, self.Vm, self.fun_moduladora)

    def get_modulada_str(self):
        return str(self.modulada)
        # return utils.get_string_modulada(self.fm_real, self.hzfm, self.fun_moduladora,
        #                                  self.fc_real, self.hzfc, self.Vc, self.fun_portadora, self.m)



