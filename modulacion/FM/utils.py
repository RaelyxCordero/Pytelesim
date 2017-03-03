import sympy as sp #simbolic
import numpy as np #numeric

def get_string_moduladora(fm_real, hzfm, Vm, fun_moduladora):
    wm = 2 * np.pi * fm_real
    hz = switch_hz_string(hzfm)
    return str(Vm) + fun_moduladora + '(' + str(wm) + hz + 't)'

def get_string_portadora(fc_real, hzfc, Vc, fun_portadora):
    wc = 2 * np.pi * fc_real
    hz = switch_hz_string(hzfc)
    return str(Vc) + fun_portadora + '(' + str(wc) + hz + 't)'

def get_string_modulada(fm_real, hzfm, fun_moduladora, fc_real, hzfc, Vc, fun_portadora, m):
    wc = 2 * np.pi * fc_real
    wm = 2 * np.pi * fm_real
    hzc = switch_hz_string(hzfc)
    hzm = switch_hz_string(hzfm)

    return str(Vc) + fun_portadora + '('+ str(wc) + hzc + 't + ' \
           + str(m) + fun_moduladora + '(' + str(wm) + hzm + 't))'

def conv_unidades_frecuencia(numero, unidad):
    if unidad == "Hz":
        return numero * 1
    if unidad == "KHz":
        return numero * 1000
    if unidad == "MHz":
        return numero * 1000000
    if unidad == "GHz":
        return numero * 1000000000
    if unidad == "THz":
        return numero * 1000000000000

def switch_hz_string(unidad):
    if unidad == "Hz":
        return ''
    if unidad == "KHz":
        return 'k'
    if unidad == "MHz":
        return 'x10^6'
    if unidad == "GHz":
        return 'x10^9'
    if unidad == "THz":
        return 'x10^12'

