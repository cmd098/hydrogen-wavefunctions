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


# Rnl(r) normalized radial function
def radial_function(n, l, r, a0):
    laguerre = sp.genlaguerre(n - l - 1, 2 * l + 1)
    p = 2 * r / (n * a0)

    return np.sqrt(
        (2 / n * a0) ** 3 * math.factorial(n - l - 1)
        / (2 * n * (math.factorial(n + l)))
    ) * np.exp(-p / 2) * p ** l * laguerre(p)


# Ylm(θ,φ) normalized angular function (spherical harmonic function)
def angular_function(l, m, theta, phi):
    legendre = sp.lpmv(m, l, np.cos(theta))

    return ((-1) ** m) * np.sqrt(
        (2 * l + 1) * math.factorial(l - np.abs(m))
        / (4 * np.pi * math.factorial(l + np.abs(m)))
    ) * legendre * np.real(np.exp(1.j * m * phi))


n = 2
l = 0
m = 0
a0 = 10

x_points = np.linspace(-480, 480, 680)
y_points = x_points
x, y = np.meshgrid(x_points, y_points)

psi = radial_function(
    n, l, np.sqrt((x ** 2 + y ** 2)), a0
) * angular_function(
    l, m, np.arctan(x / (y + 1e-10)), 0
)

# |Ψ|^2 probability density
prob_density = np.abs(psi) ** 2
