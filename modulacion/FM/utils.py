import sympy as sp #simbolic
import numpy as np #numeric

def saw(amp, f, t):
    return (2*amp/np.pi) * sp.atan(sp.cot(np.pi*f*t))

def triangle(amp, f, t):
    return (2*amp/np.pi) * sp.asin(sp.sin(2*np.pi*f*t))

def triangle_integrate(amp, f, t):
    u = sp.sin(2*np.pi*f*t)
    amplitud = ((2 * amp * u )/(np.pi * sp.cos(2*np.pi*f*t)) )
    raiz = 1 - (u**2)
    return ( amplitud * sp.asin(u) ) + sp.sqrt( raiz)

def saw_no_amp(f, t):
    return sp.atan(sp.cot(np.pi*f*t))

def triangle_no_amp(f, t):
    return sp.asin(sp.sin(2*np.pi*f*t))

def signo_en_funcion(string):
    sign = 1
    if '-' in string:
        sign = -1
    return sign

def if_signo_en_funcion(string):
    sign = True
    if '-' in string:
        sign = False
    return sign

def deriva_string_moduladora(string):
    if string == 'sin' or string == 'sen':
        return  'cos'
    elif string == '-sin' or string == '-sen':
        return '-cos'
    elif string == 'cos':
        return '-sin'
    elif string == '-cos':
        return 'sin'

def integra_string_moduladora(string):
    if string == 'sin' or string == 'sen':
        return  '-cos'
    elif string == '-sin' or string == '-sen':
        return 'cos'
    elif string == 'cos':
        return 'sin'
    elif string == '-cos':
        return '-sin'

def if_saw(funcion):
    if 'saw' in funcion or 'tri' in funcion:
        return True
    else:
        return False

def funcion_en_string(string, wm, t):
    if 'sen' in string or 'sin' in string:
        return sp.sin(wm * t)

    elif 'cos' in string:
        return sp.cos(wm * t)

    elif 'tri' in string:
        return triangle_no_amp((wm/2*np.pi), t)

    elif 'saw' in string:
        return saw_no_amp((wm/2*np.pi), t)



def deriva_vmt(modulada):
    return sp.diff(modulada, sp.Symbol('x'))

def integra_vmt(moduladora):
    return sp.integrate(moduladora, sp.Symbol('x'))

def conv_unidades_frecuencia(numero, unidad):
    if unidad == "Hz":
        return numero * 1
    elif unidad == "KHz":
        return numero * 1000
    elif unidad == "MHz":
        return numero * 1000000
    elif unidad == "GHz":
        return numero * 1000000000
    elif unidad == "THz":
        return numero * 1000000000000

def string_frecuencia_separated(string):
    val = 0
    unid = ""

    if "hz" in string:
        if "khz" in string:
            val = float(string.replace("khz", ""))
            unid = "KHz"
        elif "mhz" in string:
            val = float(string.replace("mhz", ""))
            unid = "MHz"
        elif "ghz" in string:
            val = float(string.replace("ghz", ""))
            unid = "GHz"
        elif "thz" in string:
            val = float(string.replace("thz", ""))
            unid = "THz"
        else:
            val = float(string.replace("hz", ""))
            unid = "Hz"

    return (val, unid)


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

