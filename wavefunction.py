# ===============================
# Title:  Hydrogen wavefunctions
# Author: Sebastian M
# Date:   24 Jan 2022
# Description: Hydrogen wavefunction modeling and probability-density plotting
# GitHub: https://github.com/cmd098
# ===============================

import math
import numpy as np
import scipy.special as sp


def radial_function(n, l, r, a0):
    laguerre = sp.genlaguerre(n - l - 1, 2 * l + 1)
    p = 2 * r / (n * a0)

    return np.sqrt(
        (2 / n * a0) ** 3 * math.factorial(n - l - 1)
        / (2 * n * (math.factorial(n + l)))
    ) * np.exp(-p / 2) * p ** l * laguerre(p)


def angular_function(l, m, theta, phi):
    legendre = sp.lpmv(m, l, np.cos(theta))

    return ((-1) ** m) * np.sqrt(
        (2 * l + 1) * math.factorial(l - np.abs(m))
        / (4 * np.pi * math.factorial(l + np.abs(m)))
    ) * legendre * np.real(np.exp(1.j * m * phi))
