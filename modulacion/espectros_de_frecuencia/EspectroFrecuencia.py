from scipy import special                   # Importamos scipy.special
import scipy as sp

m_bandas =(0, 0.25, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15)
n_j_bandas =(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)

coeficientes_bessel = {
    0:
    0.25:
    0.5:
    1:
    1.5:
    2:
    2.5:
    3:
    4:
    5:
    6:
    7:
    8:
    9, 10, 12, 15
}

class EspectroFrecuencia:
    def __init__(self, m, Vc, fc, fm):
        self.m = m
        self.Vc =Vc
        self.fc =fc
        self.fm =fm

    def _get_j_by_m(self):
        i = 0
        while i <= n_j_bandas[17]:
            if i == n_j_bandas[17]:
                return n_j_bandas[17]
            else:
                if self.m >= m_bandas[i] and self.m < m_bandas[i + 1]:
                    mitad = (m_bandas[i] + m_bandas[i + 1]) / 2
                    if self.m < mitad:
                        return n_j_bandas[i]
                    elif self.m >= mitad:
                        return n_j_bandas[i + 1]
                else:
                    i = i + 1

    def get_indices_bessel(self):
        x = sp.arange(0, 50, .1)

        # Calculamos los coeficientes de orden cero.
        j0 = special.j0(x)

        # Calculamos los coeficientes de orden uno.
        j1 = special.j1(x)
        j1 = special.j2