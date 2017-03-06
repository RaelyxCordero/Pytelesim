import numpy as np  # numeric
import sympy as sp  # simbolic

from . import utils

# execfile('ModulacionFM.py')
# obj = ModulacionFM(fun_moduladora='-sen', fun_portadora='cos', hz_fm='Hz', hz_fc='Hz', kl=50, fc=3000, fm=50, vc=20, vm=10, noise=False)

class ModulacionFM:
    def __init__(self, fun_moduladora, fun_portadora, hz_fm, hz_fc, kl, fc, fm, vc, vm, noise=False):
        self.fun_moduladora = fun_moduladora
        self.fun_portadora = fun_portadora
        self.kl = kl
        self.fc_real = fc  # fc traido por parametro
        self.fm_real = fm  # fm traido por parametro
        self.hzfc = hz_fc
        self.hzfm = hz_fm
        self.Vc = vc
        self.Vm = vm
        self.t = sp.Symbol('x')
        self.moduladora = 0
        self.portadora = 0
        self.modulada = 0
        self.fm = 0
        self.fc = 0
        self.wc = 0
        self.wm = 0
        self.m = 0

        if noise is True:
            self.noise = np.random.normal(0, 1, 100)
        else:
            self.noise = 0

        self.fm = utils.conv_unidades_frecuencia(self.fm_real, self.hzfm)
        self.fc = utils.conv_unidades_frecuencia(self.fc_real, self.hzfc)

        self.wm = 2 * np.pi * self.fm
        self.wc = 2 * np.pi * self.fc
        self.m = (self.kl * self.Vm) / self.wm

        self._modula_funcion_fm()

    def _modula_funcion_fm(self):
        signo_moduladora = utils.signo_en_funcion(self.fun_moduladora)

        funcion_moduladora = utils.funcion_en_string(self.fun_moduladora, self.wm, self.t)

        self.moduladora = self.Vm * (signo_moduladora * funcion_moduladora)
        integral = self._integra_kl_vmt(self.kl, self.moduladora)

        signo_portadora = utils.signo_en_funcion(self.fun_portadora)
        funcion_portadora = utils.funcion_en_string(self.fun_portadora, self.wc, self.t)

        self.portadora = self.Vc * (signo_portadora * funcion_portadora)

        if 'cos' in self.fun_portadora:
            self.modulada = self.Vc * (signo_portadora * sp.cos((self.wc * self.t) + integral)) + self.noise

        elif 'sen' in self.fun_portadora or 'sin' in self.fun_portadora:
            self.modulada = self.Vc * (signo_portadora * sp.sin(self.wc * self.t + integral)) + self.noise

        return self.modulada

    def _integra_kl_vmt(self, kl, moduladora):
        funcion = kl * moduladora
        return sp.integrate(funcion, self.t)

    def get_portadora_str(self):
        return str(self.portadora)

    def get_moduladora_str(self):
        return str(self.moduladora)

    def get_modulada_str(self):
        return str(self.modulada)
