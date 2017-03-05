
m_bandas =(0, 0.25, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15)
n_j_bandas =(0, 1, 2, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 16, 16)

coeficientes_bessel = {
    '0': (1),
    '0.25': (0.98, 0.12),
    '0.5': (0.94, 0.24, 0.03),
    '1': (0.77, 0.44, 0.11, 0.02),
    '1.5': (0.51, 0.56, 0.23, 0.06, 0.01),
    '2': (0.22, 0.58, 0.35, 0.13, 0.03),
    '2.5': (-0.05, 0.5, 0.45, 0.22, 0.07, 0.02),
    '3': (-0.26, 0.34, 0.49, 0.31, 0.13, 0.04, 0.01),
    '4': (-0.40, -0.07, 0.36, 0.43, 0.28, 0.13, 0.05, 0.02),
    '5': (-0.18, -0.33, 0.05, 0.36, 0.39, 0.26, 0.13, 0.05, 0.02),
    '6': (0.15, -0.28, -0.24, 0.11, 0.36, 0.36, 0.25, 0.13, 0.06, 0.02),
    '7': (0.30, 0, -0.30, -0.17, 0.16, 0.35, 0.34, 0.23, 0.13, 0.06, 0.02),
    '8': (0.17, 0.23, -0.11, -0.29, -0.10, 0.19, 0.34, 0.32, 0.22, 0.13, 0.06, 0.03),
    '9': (-0.09, 0.24, 0.14, -0.18, -0.27, -0.06, 0.20, 0.33, 0.30, 0.21, 0.12, 0.06, 0.03, 0.01),
    '10': (-0.25, 0.04, 0.25, 0.06, -0.22, -0.23, -0.01, 0.22, 0.31, 0.29, 0.20, 0.12, 0.06, 0.03, 0.01),
    '12': (0.05, -0.22, -0.08, 0.20, 0.18, -0.07, -0.24, -0.17, 0.05, 0.23, 0.30, 0.27, 0.20, 0.12, 0.07, 0.03, 0.01),
    '15': (-0.01, 0.21, 0.04, -0.19, -0.12, 0.17, 0.21, 0.03, -0.17, -0.22, -0.09, 0.10, 0.24, 0.28, 0.25, 0.18, 0.12)
}

class EspectroFrecuencia:
    def __init__(self, m, Vc, fc, fm):
        self.m = m
        self.Vc = Vc
        self.fc = fc
        self.fm = fm
        self.n = self._get_j_by_m()


    def _get_j_by_m(self):
        i = 0
        while i <= n_j_bandas[16]:
            if i == n_j_bandas[16]:
                return n_j_bandas[16]
            else:
                if self.m >= m_bandas[i] and self.m < m_bandas[i + 1]:
                    mitad = (m_bandas[i] + m_bandas[i + 1]) / 2
                    if self.m <= mitad:
                        return n_j_bandas[i]
                    elif self.m > mitad:
                        return n_j_bandas[i + 1]
                else:
                    i = i + 1

    def get_indices_bessel(self):
        return coeficientes_bessel[str(self.n)]

    def get_amplitudes_espectros(self):
        items = self.get_indices_bessel()
        i = 0
        amplitudes = (items[i] * self.Vc, )
        i = i + 1
        while i < len(items):
            amplitudes = amplitudes + (items[i] * self.Vc,)
            i = i + 1
        return amplitudes

    # devuelve un diccionario con llaves j0, j1, etc
    # con la llave 'j0' devuelve la frecuencia portadora
    # con la llave 'j1' devuelve una tupla con la frecuencia lateral inferior y superior respectivamente para j1
    # y asi sucesivamente

    def get_frecuencias_espectros(self):
        frecuencias_pares = {}
        frecuencias_pares['j0'] = self.fc
        i = 1
        fli = self.fc - self.fm
        fls = self.fc + self.fm
        while i <= self.n:
            frecuencias_pares['j'+str(i)] = (fli, fls)
            fli = fli - self.fm
            fls = fls + self.fm
            i = i + 1
        return frecuencias_pares


