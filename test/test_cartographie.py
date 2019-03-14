#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
from hjb.cartographie import Valeur
from hjb.systeme import Systeme
import pytest
import numpy as np


@pytest.fixture
def s():
    s = Systeme(a=1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=1)
    return s


@pytest.fixture
def v(s):
    v = Valeur.from_dl(sys=s, T=1, dl=0.1)
    return v


def test_instanciation(s):
    v = Valeur(sys=s,
               xs=np.linspace(0, 1, 2),
               ys=np.linspace(0, 1, 2),
               ts=np.linspace(0, 1, 2)
               )
    assert isinstance(v, Valeur)


def test_extremites(s):
    v = Valeur(sys=s,
               xs=np.linspace(0, 1, 2),
               ys=np.linspace(0, 1, 2),
               ts=np.linspace(0, 1, 2)
               )
    assert v.verification_extremites()

    v = Valeur(sys=s,
               xs=np.linspace(0, 2, 2),
               ys=np.linspace(0, 1, 2),
               ts=np.linspace(0, 1, 2)
               )
    assert not v.verification_extremites()


def test_constructeur(s):
    v = Valeur.from_dl(sys=s, T=10, dl=0.1)
    assert isinstance(v, Valeur)
    assert v.verification_cfl()
    assert v.verification_extremites()


def test_cfl(s):
    v = Valeur(sys=s,
               xs=np.linspace(0, 1, 2),
               ys=np.linspace(0, 1, 2),
               ts=np.linspace(0, 1, 20)
               )
    assert v.verification_cfl()

    v = Valeur(sys=s,
               xs=np.linspace(0, 1, 2),
               ys=np.linspace(0, 1, 2),
               ts=np.linspace(0, 1, 2)
               )
    assert not v.verification_cfl()


def test_points(s):
    v = Valeur(sys=s,
               xs=np.array([0, 1]),
               ys=np.array([0, 1]),
               ts=np.array([0, 1])
               )
    assert np.all(v.points == np.array([[0, 0], [1, 0], [0, 1], [1, 1]]))


def test_points_grand(s, v):
    assert v.points.shape == (100, 2)
    assert np.allclose(v.points[0], [0, 0])
    assert np.allclose(v.points[9], [1, 0])
    assert np.allclose(v.points[90], [0, 1])
    assert np.allclose(v.points[-1], [1, 1])


def test_etat_final(s, v):
    v.initialisation_terminale()
    p = np.linspace(0, 1., 10)
    valeurs_reelles = ((p[:, np.newaxis]) ** 2
                       + (p[np.newaxis, :] - 1.) ** 2) / 2
    assert np.allclose(v.valeurs[-1, ...], valeurs_reelles)


def test_step(s):
    v = Valeur(sys=s,
               xs=np.array([0, 1]),
               ys=np.array([0, 1]),
               ts=np.array([0, 1])
               )
    manuel = np.array([0, 0, 0, 0])
    automatique = v.step(vals=np.array([0, 0, 0, 0]).reshape(2, 2),
                         dt=0.5)
    assert np.all(manuel == automatique)

    manuel = np.array([0, 0.5, 0.5, 0])
    automatique = v.step(vals=np.array([0, 1, 1, 2]).reshape(2, 2),
                         dt=0.5)
    assert np.allclose(manuel, automatique)
