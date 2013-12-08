#!/usr/bin/env python
# coding: utf-8

from infect.infect import Infect


class TestInfect(object):
    def test_instantiation(self):
        infect = Infect()
        assert infect is not None
