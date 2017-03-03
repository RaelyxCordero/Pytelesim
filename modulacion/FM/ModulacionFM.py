import sympy as sp #simbolic
import numpy as np #numeric
import utils
from sympy import *

# AGREGAR RUIDO
#Validar Hz y no hz

class ModulacionFM:


    def __init__(self, fun_moduladora, fun_portadora, hz_fm, hz_fc, kl, fc, fm, vc, vm):
        self.fun_moduladora = fun_moduladora
        self.fun_portadora = fun_portadora
        self.kl = kl
        self.fc_real = fc  # fc traido por parametro
        self.fm_real = fm  # fm traido por parametro
        self.hzfc = hz_fc
        self.hzfm = hz_fm
        self.Vc = vc
        self.Vm = vm
        self.t = Symbol('t')
        self.moduladora = 0
        self.portadora = 0
        self.fm = 0
        self.fc = 0
        self.wc = 0
        self.wm = 0

    def modula_funcion_fm(self):
        modulada = 0

        self.fm = utils.conv_unidades_frecuencia(self.fm_real, self.hzfm)
        self.fc = utils.conv_unidades_frecuencia(self.fc_real, self.hzfc)

        self.wm = 2*np.pi*self.fm
        self.wc = 2*np.pi*self.fc

        if self.fun_moduladora == 'cos':
            self.moduladora = self.Vm*sp.cos(self.wm*self.t)

        elif self.fun_moduladora == 'sen' or self.fun_moduladora == 'sin':
            self.moduladora = self.Vm*sp.sin(self.wm*self.t)

        integral = self.integra_kl_vmt(self.kl, self.moduladora)

        if self.fun_portadora == 'cos':
            self.portadora = self.Vc*sp.cos(self.wc*self.t)
            modulada = self.Vc*sp.cos((self.wc*self.t) + integral)

        elif self.fun_portadora == 'sen' or self.fun_moduladora == 'sin':
            self.portadora = self.Vc*sp.sin(self.wc*self.t)
            modulada = self.Vc*sp.sin(self.wc*self.t + integral)

        return modulada

    def integra_kl_vmt(self, kl, moduladora):
        funcion = kl * moduladora
        return sp.integrate(funcion, self.t)

    def get_m(self):
        return (self.kl * self.Vm) / self.wm

    def get_moduladora(self):
        if self.moduladora is None:
            return 'no hay moduladora'
        else:
            return self.moduladora

    def get_portadora(self):
        if self.portadora is None:
            return 'no hay portadora'
        else:
            return self.portadora

    def get_portadora_str(self):
        return utils.get_string_portadora(self.fc_real, self.hzfc, self.Vc, self.fun_portadora)

    def get_moduladora_str(self):
        return utils.get_string_portadora(self.fm_real, self.hzfm, self.Vm, self.fun_moduladora)

    def get_modulada_str(self):
        return utils.get_string_modulada(self.fm_real, self.hzfm, self.fun_moduladora,
                                         self.fc_real, self.hzfc, self.Vc, self.fun_portadora, self.get_m())


