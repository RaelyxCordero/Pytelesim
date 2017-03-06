import numpy as np #numeric
import sympy as sp #simbolic
from . import utils

from .ModulacionPM import ModulacionPM

#execfile('DemodulacionFM.py')
#obj = DemodulacionFM(5, 10, 'KHz', 'cos', 'cos', 'KHz', m=50.13, fm=15, Vm=10)

class DemodulacionPM:

    def __init__(self, Vc, fc, hzfc,  fun_portadora, fun_moduladora, hzfm, fm, k=None,  Vm=None, m=None):

        self.moduladora = 0
        self.portadora = 0
        self.modulada = 0
        self.fun_portadora = fun_portadora
        self.fun_moduladora = fun_moduladora
        self.hzfc = hzfc
        self.hzfm = hzfm
        self.k = k
        self.fm_real = fm
        self.m = m
        self.Vc = Vc
        self.Vm = Vm
        self.fc_real = fc  # fc por parametro
        self.t = sp.Symbol('x')

        if k is not None and Vm is not None:
            self.m = self.Vm * self.k

        elif m is not None and Vm is not None:
            self.k = self.m / self.Vm

        elif m is not None and k is not None:
            self.Vm = self.m / self.k

        self.fm = utils.conv_unidades_frecuencia(self.fm_real, self.hzfm)
        self.fc = utils.conv_unidades_frecuencia(self.fc_real, self.hzfc)

        self.wm = 2 * np.pi * self.fm
        self.wc = 2 * np.pi * self.fc

        self._demodula_funcion_pm()

    def _demodula_funcion_pm(self):
        if self.fun_moduladora == 'cos':
            self.moduladora = self.Vm * sp.cos(self.wm*self.t)

        elif self.fun_moduladora == 'sen' or self.fun_moduladora == 'sin':
            self.moduladora = self.Vm * sp.sin(self.wm * self.t)

        if self.fun_portadora == 'cos':
            self.portadora = self.Vc * sp.cos(self.wc*self.t)

        elif self.fun_portadora == 'sen' or self.fun_moduladora == 'sin':
            self.portadora = self.Vc * sp.sin(self.wc * self.t)

        self.modulada = ModulacionPM(self.fun_moduladora, self.fun_portadora,
                                     self.hzfm, self.hzfc, self.k, self.fc, self.fm, self.Vc, self.Vm)

        return {'moduladora': self.moduladora, 'portadora': self.portadora}

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



