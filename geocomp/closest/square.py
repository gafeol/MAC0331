#!/usr/bin/env python

"""Algoritmo de line sweep"""

from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.config import *

def plot_square(x, y, xx, yy):
	if(x == None or y == None or xx == None or yy == None):
		return None
	id = []
	id.append(control.plot_segment(x, y, x, yy, 'orange'))
	id.append(control.plot_segment(x, yy, xx, yy, 'orange'))
	id.append(control.plot_segment(xx, yy, xx, y, 'orange'))
	id.append(control.plot_segment(xx, y, x, y, 'orange'))
	return id

def erase_square(id):
	if(id == None):
		return 
	for ln in id:
		control.plot_delete(ln)

