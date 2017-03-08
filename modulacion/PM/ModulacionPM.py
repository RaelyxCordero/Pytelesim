import sympy as sp  # simbolic
import numpy as np  # numeric
from . import utils

# AGREGAR RUIDO
# Validar Hz y no hz

#execfile('ModulacionPM.py')
#obj = ModulacionPM(fun_moduladora='sin', fun_portadora='cos', hz_fm='KHz', hz_fc='KHz', k=50, fc=30, fm=1, vc=6, vm=2, noise=False)

class ModulacionPM:
    def __init__(self, fun_moduladora, fun_portadora, hz_fm, hz_fc, k, fc, fm, vc, vm, noise=False):
        self.fun_moduladora = fun_moduladora
        self.fun_portadora = fun_portadora
        self.k = k
        self.fc_real = fc  # fc traido por parametro
        self.fm_real = fm  # fm traido por parametro
        self.hzfc = hz_fc
        self.hzfm = hz_fm
        self.Vc = vc
        self.Vc_sierra = (2 * self.Vc)/np.pi
        self.Vm = vm
        self.Vm_sierra = (2 * self.Vm)/np.pi
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
            self.noise = np.random.normal(0,1,100)
        else:
            self.noise = 0

        self.fm = utils.conv_unidades_frecuencia(self.fm_real, self.hzfm)
        self.fc = utils.conv_unidades_frecuencia(self.fc_real, self.hzfc)

        self.wm = 2 * np.pi * self.fm
        self.wc = 2 * np.pi * self.fc

        if 'saw' in self.fun_moduladora:
            self.m = (self.k * self.Vm_sierra)

        elif 'tri' in self.fun_moduladora:
            self.m = (self.k * self.Vm_sierra)
        else:
            self.m = self.k * self.Vm

        self._modula_funcion_pm()

    def _modula_funcion_pm(self):

        signo_moduladora = utils.signo_en_funcion(self.fun_moduladora)
        funcion_moduladora = utils.funcion_en_string(self.fun_moduladora, self.wm, self.t)

        if 'saw' in self.fun_moduladora:
            self.moduladora = (-1) * self.Vm_sierra * (signo_moduladora * funcion_moduladora)

        elif 'tri' in self.fun_moduladora:
            self.moduladora = self.Vm_sierra * (signo_moduladora * funcion_moduladora)
        else:
            self.moduladora = self.Vm * (signo_moduladora * funcion_moduladora)

        funcion_mod = self.k * self.moduladora

        signo_portadora = utils.signo_en_funcion(self.fun_portadora)
        funcion_portadora = utils.funcion_en_string(self.fun_portadora, self.wc, self.t)

        if 'saw' in self.fun_portadora:
            self.portadora = (-1) * self.Vm_sierra * (signo_portadora * funcion_portadora)

        elif 'tri' in self.fun_portadora:
            self.portadora = self.Vm_sierra * (signo_portadora * funcion_portadora)
        else:
            self.portadora = self.Vc * (signo_portadora * funcion_portadora)



        if 'cos' in self.fun_portadora:
            self.modulada = self.Vc * (signo_portadora * sp.cos((self.wc * self.t) + funcion_mod)) + self.noise

        elif 'sen' in self.fun_portadora or 'sin' in self.fun_portadora:
            self.modulada = self.Vc * (signo_portadora * sp.sin(self.wc * self.t + funcion_mod)) + self.noise

        elif 'saw' in self.fun_portadora:
            self.modulada = (-1) * (self.Vc_sierra) * (signo_portadora * sp.atan(sp.cot((self.wc/2) * self.t + funcion_mod))) \
                            + self.noise

        elif 'tri' in self.fun_portadora:
            self.modulada = (self.Vc_sierra) * (signo_portadora * sp.asin(sp.sin(self.wc * self.t + funcion_mod))) \
                            + self.noise



        return self.modulada

    def get_portadora_str(self):
        return str(self.portadora)

    def get_moduladora_str(self):
        return str(self.moduladora)

    def get_modulada_str(self):
        return str(self.modulada)

