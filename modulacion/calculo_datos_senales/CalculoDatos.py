# coding=utf-8
import sympy as sp  # simbolic
import numpy as np  # numeric

'''
a. Desviación de frecuencia.
b. Desviación de fase.
c. Desviación instantánea de fase.
d. Desviación Instantánea de frecuencia.
e. Frecuencia instantánea.
f. Fase instantánea.
g. Sensibilidad de desviación
h. Determinar el ancho de banda.
'''

# k, Vm, fm, t, fun_moduladora, fc, variacion_fase, variacion_voltaje, n, variacion_frecuencia
# Desviacion de Frecuencia / Desviacion de Fase
def desviacion_frecuencia_fase(const_desv, Vm):
    return const_desv * Vm


# Desviacion instantanea de fase / frecuencia
def desviacion_instantanea_frecuencia_fase(const_desv, Vm, fm, t, fun_moduladora):
    desviacion_instantanea = 0
    wm = 2 * np.pi * fm
    if fun_moduladora == 'cos':
        desviacion_instantanea = const_desv * Vm * np.cos(wm * t)

    elif fun_moduladora == 'sen' or fun_moduladora == 'sin':
        desviacion_instantanea = const_desv * Vm * np.sin(wm * t)

    return desviacion_instantanea


# Frecuencia Instantanea
def frecuencia_instantanea(fc, kl, Vm, fm, t, fun_moduladora):
    return fc + (desviacion_instantanea_frecuencia_fase(kl, Vm, fm, t, fun_moduladora) / 2 * np.pi)


# Fase Instantánea
def fase_instantanea(fc, k, Vm, fm, t, fun_moduladora):
    return 2 * np.pi * fc + desviacion_instantanea_frecuencia_fase(k, Vm, fm, t, fun_moduladora)


# Sensibilidad a la desviacion
def sensibilidad_k(variacion_fase, variacion_voltaje):
    return variacion_fase / variacion_voltaje


def sensibilidad_kl(variacion_frecuencia, variacion_voltaje):
    return variacion_frecuencia / variacion_voltaje


# Ancho de banda
def ancho_banda_bessel(n, fm):
    return 2 * n * fm


def ancho_banda_regla_carson(variacion_frecuencia, fm):
    return 2 * (variacion_frecuencia + fm)


def ancho_banda_m_mayor10(variacion_frecuencia):
    return 2 * variacion_frecuencia


def ancho_banda_m_menor10(fm):
    return 2 * fm
