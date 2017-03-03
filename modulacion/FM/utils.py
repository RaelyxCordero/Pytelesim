


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

