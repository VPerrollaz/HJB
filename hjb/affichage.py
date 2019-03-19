#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 perrollaz <perrollaz@vincent-MacBookPro>
#
# Distributed under terms of the MIT license.

"""
Fonctionnalités pour faciliter l'affichage des solutions de HJB.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def affichage_image(v):
    """Renvoit une figure affichant la première et la dernière valeur.

    :param v: objet valeur
    :type v: Valeur
    """
    fig, (ax_h, ax_b) = plt.subplots(nrows=2)
    im_h = ax_h.imshow(v.valeurs[-1],
                       extent=[0, v.sys.bx, 0, v.sys.by],
                       origin="lower")
    ax_h.set_title(f"t={v.ts[-1]}")
    fig.colorbar(im_h, ax=ax_h)
    im_b = ax_b.imshow(v.valeurs[0],
                       extent=[0, v.sys.bx, 0, v.sys.by],
                       origin="lower")
    ax_b.set_title("t=0")
    fig.colorbar(im_b, ax=ax_b)
    return fig


def affichage_3d(v):
    """Renvoit une figure avec les deux graphes des valeurs extremes.

    :param v: objet valeur
    :type v: Valeur
    """
    fig = plt.figure()
    ax = Axes3D(fig)
    X, Y = np.meshgrid(v.xs, v.ys)
    ax.plot_wireframe(X.T, Y.T, v.valeurs[-1],
                      color="blue", label=f"t={v.ts[-1]}")
    ax.plot_wireframe(X.T, Y.T, v.valeurs[0],
                      color="red", label=f"t=0")
    ax.legend()
    return fig


def main():
    s = Systeme(a=1, b=2, c=2, d=1, alpha=1, beta=1, M=1, bx=1, by=1)
    v = Valeur.from_dl(sys=s, dl=0.05, T=10)
    v.resolution()
    affichage_3d(v)
    plt.show()


if __name__ == "__main__":
    from systeme import Systeme
    from cartographie import Valeur

    main()
