# ===============================
# Title:  Hydrogen wavefunctions
# Author: Sebastian M
# Date:   24 Jan 2022
# Description: Hydrogen wavefunction modeling and probability-density plotting
# GitHub: https://github.com/cmd098
# ===============================

import argparse
import math
import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt

# Command line arguments
parser = argparse.ArgumentParser(
    description='Hydrogen wavefunction probability-density by definition '
                'of quantum numbers n, l, m and bohr radius'
)


def add_argument(flag, description): parser.add_argument(
    flag, help=description, metavar='', type=int, required=True
)


add_argument('-n', '(n) principal quantum number (constraint: 1 <= n)')
add_argument('-l', '(l) azimuthal quantum number (constraint: 0 <= l <= n-1)')
add_argument('-m', '(m) magnetic quantum number (constraint: -l <= m <= l)')
add_argument('-a0', '(a0) bohr radius (constraint: 1 <= a0)')
parser.add_argument(
    '-cm', metavar='', choices=['1', '2', '3', '4'], default='1',
    help='(color map) optional color scheme |input choices: 1, 2, 3, 4'
)

args = parser.parse_args()


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


# probability-density plot
def plot_wavefunction(n, l, m, a0):
    x_points = np.linspace(-480, 480, 680)
    y_points = x_points
    x, y = np.meshgrid(x_points, y_points)

    # Ψ(r,θ,φ) = R(r)Y(θ,φ)
    psi = radial_function(
        n, l, np.sqrt((x ** 2 + y ** 2)), a0
    ) * angular_function(
        l, m, np.arctan(x / (y + 1e-10)), 0
    )

    # |Ψ|^2 probability density
    prob_density = np.abs(psi) ** 2

    plt.figure(figsize=(8, 6))
    plt.title('Hydrogen wavefunction probability density', fontsize=15, pad=20)
    plt.text(25, 50, f'{n, l, m}', fontsize=14, color='white')
    plt.text(780, 25, '+', fontsize=18)
    plt.text(780, 690, '−', fontsize=18)
    plt.text(
        790, 560, 'Electron probability distribution',
        rotation='vertical', fontsize=14
    )

    prob_density = np.sqrt(prob_density)
    cmap = {'1': 'inferno', '2': 'gist_heat', '3': 'afmhot', '4': 'gist_gray'}
    plt.imshow(prob_density, cmap=cmap[args.cm])
    cbar = plt.colorbar()
    cbar.set_ticks([])
    plt.savefig(f'wavefunction{n,l,m}.png')
    plt.show()


plot_wavefunction(args.n, args.l, args.m, args.a0)
