#!/usr/bin/env python

from . import control
from geocomp import config


class Segment:
    "Um segmento de reta"
    def __init__ (self, pto_from=None, pto_to=None):
        "Para criar, passe os dois pontos extremos"
        self.p1 = pto_from
        self.p2 = pto_to
        if self.__cmp(self.p1, self.p2) < 0:
            self.upper = self.p1
            self.lower = self.p2
        else:
            self.upper = self.p2
            self.lower = self.p1

    def __repr__ (self):
        "retorna uma string da forma [ ( x0 y0 );( x1 y1 ) ]"
        return '[ ' + repr(self.p1) + '; ' + repr(self.p2) + ' ]'

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        if self.p1 == other.p1 and self.p2 == other.p2:
            return True
        if self.p1 == other.p2 and self.p2 == other.p1:
            return True
        return False

    def endpoints(self):
        return self.p1, self.p2

    def hilight (self, color_line=config.COLOR_HI_SEGMENT,
            color_point=config.COLOR_HI_SEGMENT_POINT):
        "desenha o segmento de reta com destaque na tela"
        self.lid = self.p1.lineto (self.p2, color_line)
        self.pid0 = self.p1.hilight (color_point)
        self.pid1 = self.p2.hilight (color_point)
        return self.lid

    def plot (self, cor=config.COLOR_SEGMENT):
        "desenha o segmento de reta na tela"
        self.lid = self.p1.lineto (self.p2, cor)
        return self.lid

    def hide (self, id=None):
        "apaga o segmento de reta da tela"
        if id == None: id = self.lid
        control.plot_delete (id)

    def adj(self, p):
        if p == self.p1:
            return self.p2
        return self.p1

    def __hash__(self):
        return hash(self.p1) ^ hash(self.p2)

    def __contains__(self, p):
        return p == self.p1 or p == self.p2

    def __cmp(self, a, b):
        if a[1] > b[1]:
            return -1
        if b[1] > a[1]:
            return 1
        if a[0] < b[0]:
            return -1
        if b[0] < a[0]:
            return 1
        return 0
