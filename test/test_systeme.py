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
import pytest
from hjb.systeme import Systeme
import numpy as np


@pytest.fixture
def s1():
    return Systeme(a=1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=2)


def test_instanciation(s1):
    assert isinstance(s1, Systeme)


def test_parametres_valides(s1):
    assert s1._parametres_positifs()

    f2 = Systeme(a=-1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert not f2._parametres_positifs()


def test_bistabilitite(s1):
    assert not s1._regime_bistable()

    f2 = Systeme(a=1, b=2, c=2, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert f2._regime_bistable()


def test_verification(s1):
    assert not s1.verifications()

    f2 = Systeme(a=1, b=2, c=2, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    assert f2.verifications()


def test_coexistence():
    f2 = Systeme(a=1, b=2, c=2, d=1, bx=1, by=1, alpha=1, beta=1, M=2)
    x, y = f2.etat_coexistence()
    assert (x == 1 / 3) and (y == 1/3)


def test_repr():
    chaine = "Systeme(a=1, b=1, c=1, d=1, alpha=1, beta=1, M=2, bx=1, by=1)"
    f = eval(chaine)
    assert repr(f) == chaine


def test_flux(s1):
    assert np.allclose(s1.flux(np.array((1, 1)), 0), np.array([-1, -1]))
    assert np.allclose(s1.flux(np.array((1, 0)), 0), np.array([0, 0]))
    assert np.allclose(s1.flux(np.array((0, 1)), 0), np.array([0, 0]))
    assert np.allclose(s1.flux(np.array((1, 1)), 1), np.array([-2, -2]))
    assert np.allclose(s1.flux(np.array((1, 1)), 1), np.array([-2, -2]))

    assert np.allclose(s1.flux_libre(np.array((1, 1))), np.array([-1, -1]))
    assert np.allclose(s1.flux_bang(np.array((1, 1))), np.array([-3, -3]))


def test_flux_vectoriel(s1):
    points = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
    controle = np.array([0, 0, 0, 0])
    valeurs_reelles = np.array([[0, 0], [0, 0], [0, 0], [-1, -1]])
    valeurs_calculees = s1.flux(points, controle)
    assert np.allclose(valeurs_reelles, valeurs_calculees)
    valeurs_reelles = np.array([[0, 0], [0, 0], [0, 0], [-1, -1]])
    valeurs_calculees = s1.flux_libre(points)
    assert np.allclose(valeurs_calculees, valeurs_reelles)
    valeurs_reelles = np.array([[0, 0], [-2, 0], [0, -2], [-3, -3]])
    valeurs_calculees = s1.flux_bang(points)
    assert np.allclose(s1.flux_bang(points), valeurs_reelles)


def test_borne(s1):
    for _ in range(10):
        mu, nu, theta = np.random.rand(3)
        x, y, u = mu * s1.bx, nu * s1.by, theta * s1._M
        X = np.array([x, y])
        assert np.linalg.norm(s1.flux(X, u)) < s1.borne()
