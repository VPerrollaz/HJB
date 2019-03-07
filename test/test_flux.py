#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 perrollaz <perrollaz@vincent-MacBookPro>
#
# Distributed under terms of the MIT license.

"""
Tests de flux.
"""

from hjb.flux import Flux
import numpy as np


def test_instanciation():
    f = Flux(a=1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert isinstance(f, Flux)


def test_parametres_valides():
    f1 = Flux(a=1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert f1._parametres_positifs()

    f2 = Flux(a=-1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert not f2._parametres_positifs()


def test_bistabilitite():
    f1 = Flux(a=1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert not f1._regime_bistable()

    f2 = Flux(a=1, b=2, c=2, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert f2._regime_bistable()


def test_verification():
    f1 = Flux(a=1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert not f1.verifications()

    f2 = Flux(a=1, b=2, c=2, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert f2.verifications()


def test_coexistence():
    f2 = Flux(a=1, b=2, c=2, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    x, y = f2.etat_coexistence()
    assert (x == 1 / 3) and (y == 1/3)


def test_evaluation():
    f = Flux(a=1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert np.allclose(f(np.array((1, 1)), 0), np.array([-1, -1]))
    assert np.allclose(f(np.array((1, 0)), 0), np.array([0, 0]))
    assert np.allclose(f(np.array((0, 1)), 0), np.array([0, 0]))
    assert np.allclose(f(np.array((1, 1)), 1), np.array([-2, -2]))


def test_repr():
    chaine = "Flux(a=1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=2)"
    f = eval(chaine)
    assert repr(f) == chaine
