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


def test_grille(setup):
    s, v = setup
    Nx = np.floor(s.bx / v.dl) + 1
    xs = np.arange(0, s.bx, s.bx / Nx)
    assert np.allclose(v.xs, xs)
    Ny = np.floor(s.by / v.dl) + 1
    ys = np.arange(0, s.by, s.by / Ny)
    assert np.allclose(v.ys, ys)
