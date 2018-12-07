#!/usr/bin/env python
"""Algoritmo de line sweep"""

from geocomp.common.segment import Segment
from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.config import *
from . import square
import math
import time

def sq(x):
	return x*x

oo = float("inf")

ans = oo
a = None
hia = None
b = None
hib = None
id = None


def closest_pair(v, w, l, r):
	ans = _closest_pair(v, w, l, r)
	return ans.dist

def make(dist, a, hia, b, hib, id):
	return {"dist": dist, "a": a, "hia": hia, "b": b, "hib": hib, "id": id}
	

def _closest_pair(v, w, l, r):
	ans = -1.
	a = b = None
	hia = hib = None
	id = None

	if l + 1 >= r: 
		return make(oo, None, None, None, None, None)
	
	m = int((l + r)/2)
	x = v[m].x
	
	#Vertical line dividing
	vid = control.plot_vert_line(x)
	control.sleep()

	lans = _closest_pair(v, w, l, m)

	control.plot_delete(vid)
	vid = control.plot_vert_line(x, COLOR_ALT2)
	control.sleep()

	rans = _closest_pair(v, w, m, r)

	control.plot_delete(vid)
	vid = control.plot_vert_line(x, COLOR_ALT3)
	control.sleep()

	
	bst = ot = None

	if(lans['dist'] < rans['dist']):
		bst = lans
		ot = rans
	else:
		bst = rans
		ot = lans

	res = bst['dist']
	a = bst['a']
	hia = bst['hia']
	b = bst['b']
	hib = bst['hib']
	id = bst['id']

	if(ot['a'] != None):
		ot['a'].unhilight(ot['hia'])
	if(ot['b'] != None):
		ot['b'].unhilight(ot['hib'])
	if(ot['id'] != None):
		control.plot_delete(ot['id'])
	control.sleep()

	vlid = vrid = None
	lx = rx = None
	if(res != float("inf")):
		lx = x - res
		vlid = control.plot_vert_line(lx, COLOR_ALT5)
		rx = x + res
		vrid = control.plot_vert_line(rx, COLOR_ALT5)
		control.sleep()

	# Merge
	i = l
	j = m
	aux = l

	pa = pb = None
	while i < m and j < r :
		if v[i].y < v[j].y:
			w[aux] = v[i]
			i = i+1
		else:
			w[aux] = v[j]
			j = j+1
		aux = aux+1

	while i < m:
		w[aux] = v[i]
		aux = aux+1
		i = i + 1

	while j < r:
		w[aux] = v[j]
		aux = aux+1
		j = j+1

	s = l
	for i in range(l, r):
		v[i] = w[i]
		if sq(v[i].x - x) < sq(res):
			hv = v[i].hilight('red')
			control.sleep()
			square_id = None
			if(res != float("inf")):
				square_id = square.plot_square(lx, v[i].y-res, rx, v[i].y)
				control.sleep()
			for j in range(s-1, l-1, -1):
				if sq(w[i].y - w[j].y) >= res*res:
					break;
				dis = math.sqrt(dist2(w[i], w[j]))

				if res > dis:
					res = dis
					control.freeze_update()
					if a != None: a.unhilight(hia)
					if b != None: b.unhilight(hib)
					if id != None: control.plot_delete(id)

					a = w[i]
					b = w[j]

					hia = a.hilight()
					hib = b.hilight()
					id = a.lineto(b)

					control.thaw_update()
					control.update()
			v[i].unhilight(hv)
			w[s] = v[i]
			s = s+1
			if square_id != None:
				square.erase_square(square_id)

	control.plot_delete(vid)
	if(vlid != None):
		control.plot_delete(vlid)
	if(vrid != None):
		control.plot_delete(vrid)
	control.sleep()

	return make(res, a, hia, b, hib, id)
					

def Divide (l):
	"Algoritmo que usa divide and conquer para encontrar o par de pontos mais proximo"
	global ans, a, b

	if len (l) < 2: 
		return None

	l.sort(key=lambda o: o.x)
	
	L = []
	for i in range(len(l)):
		L.append(0)

	ans = _closest_pair(l, L, 0, len(l))
	dis = ans['dist']
	a = ans['a']
	b = ans['b']

	ret = Segment (a, b)
	ret.extra_info = 'distancia: %.2f'%(dis)
	return ret
	
