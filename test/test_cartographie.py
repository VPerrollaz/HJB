#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
from hjb.cartographie import Valeur
from hjb.systeme import Systeme
import pytest
import numpy as np


@pytest.fixture
def setup():
    s = Systeme(a=1, b=1, c=1, d=1, bx=1, by=1, alpha=1, beta=1, M=1)
    v = Valeur(sys=s, T=10, dl=0.1)
    return s, v


def test_instanciation(setup):
    s, v = setup
    assert isinstance(v, Valeur)


def test_discretisation_spatiale(setup):
    s, v = setup
    assert (v.dx <= v.dl) and (v.dy <= v.dl)


def test_cfl(setup):
    s, v = setup
    assert np.sqrt(2) * v.dt * s.borne() <= v.dl


def test_etat_final(setup):
    s, v = setup
    v.initialisation_terminale()
    p = np.linspace(0, 1., 10)
    valeurs_reelles = ((p[:, None]) ** 2 + (p[None, :] - 1.) ** 2) / 2
    assert np.allclose(v.valeurs[-1, ...], valeurs_reelles)
