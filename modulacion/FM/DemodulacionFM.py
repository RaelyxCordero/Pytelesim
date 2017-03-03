import numpy as np
import sympy as sp
from sympy  import *
from numpy import sin, cos, pi
from utils import conv_unidades_frecuencia, switch_hz_string

class DemodulacionFM:
    def __init__(self, Vc, fc, fun_portadora, fun_moduladora,
                 kl=None, fm=None, Vm=None, m=None, t=np.arange(0, 0.01, 10**(-5.7) ) ):

        self.moduladora = None
        self.portadora = None
        self.fun_portadora = fun_portadora
        self.fun_moduladora = fun_moduladora
        self.kl = kl
        self.fc_real = fc  # fc sin convertir con hz
        self.fm_real = fm  # fm sin convertir con hz
        self.Vc = Vc
        self.Vm = Vm
        self.m = m
        self.t = t

        self.fm = conv_unidades_frecuencia(self.fm, self.hz_fm)
        self.fc = conv_unidades_frecuencia(self.fc_real, self.hz_fc)

        self.wm = 2 * pi * self.fm
        self.wc = 2 * pi * self.fc

    def demodula_funcion_fm(self):
        # if
        return None

    def get_wm(self):
        return (self.kl * self.Vm)/ self.m

    def get_kl(self):
        return (self.m * self.wm) / self.Vm

    def get_Vm(self):
        return (self.m * self.wm) / self.kl

    def get_m(self):
        return (self.kl * self.Vm) / self.wm

