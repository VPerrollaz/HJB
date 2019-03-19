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


@pytest.fixture
def vs(s):
    vs = Valeur(sys=s,
                xs=np.array([0, 1]),
                ys=np.array([0, 1]),
                ts=np.array([0, 0.5, 1])
                )
    return vs


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


def test_points(s, vs):
    assert np.all(vs.points == np.array([[0, 0], [0, 1], [1, 0], [1, 1]]))


def test_points_grand(s, v):
    assert v.points.shape == (100, 2)
    assert np.allclose(v.points[0], [0, 0])
    assert np.allclose(v.points[9], [0, 1])
    assert np.allclose(v.points[90], [1, 0])
    assert np.allclose(v.points[-1], [1, 1])


def test_etat_final(s, vs):
    vs.initialisation_terminale()
    manuel = np.array([[0.5, 0], [1, 0.5]])
    assert np.allclose(vs.valeurs[-1], manuel)


def test_etat_final_grand(s, v):
    v.initialisation_terminale()
    p = np.linspace(0, 1., 10)
    valeurs_reelles = (np.abs(p[:, np.newaxis])
                       + np.abs(p[np.newaxis, :] - 1.)) / 2
    assert np.allclose(v.valeurs[-1, ...], valeurs_reelles)


def test_nouveaux_points(s, vs):
    p_l, p_b = vs.nouveaux_points(dt=0.5)
    q_l = np.array([[0, 0], [0, 1], [1, 0], [0.5, 0.5]])
    q_b = np.array([[0, 0], [0, 0.5], [0.5, 0], [0, 0]])
    assert np.allclose(p_l, q_l)
    assert np.allclose(p_b, q_b)


def test_step(s, vs):
    manuel = np.array([[0, 0], [0, 0]])
    automatique = vs.step(vals=np.array([0, 0, 0, 0]).reshape(2, 2),
                          dt=0.5)
    assert np.all(manuel == automatique)

    manuel = np.array([[0., 0.5], [0.5, 0]])
    automatique = vs.step(vals=np.array([0, 1, 1, 2]).reshape(2, 2),
                          dt=0.5)
    assert np.allclose(manuel, automatique)


def test_resolution(s, vs):
    vs.resolution()
    manuel = np.array([[[0.5, 0], [0.625, 0.4375]],
                       [[0.5, 0], [0.75, 0.5]],
                       [[0.5, 0], [1, 0.5]]])
    for k in reversed(range(3)):
        assert np.allclose(vs.valeurs[k], manuel[k]), f"valeur de k {k}"
