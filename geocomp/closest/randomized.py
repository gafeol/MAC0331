#!/usr/bin/env python
"""Algoritmo randomizado"""

from geocomp.common.segment import Segment
from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.config import *
from random import shuffle
import math


cntdist = 0

def getdist2(a, b):
	global cntdist
	cntdist += 1
	return dist2(a, b)

def plot_grid(l, eps):
	mnx = mny = float('inf')
	mxx = mxy = -float('inf')
	for p in l:
		mnx = min(mnx, p.x)
		mny = min(mny, p.y)
		mxy = max(mxy, p.y)
		mxx = max(mxx, p.x)
	mnx -= 5*eps
	mnx = math.floor(mnx/(eps/2.))*(eps/2.)
	mny -= 5*eps
	mny = math.floor(mny/(eps/2.))*(eps/2.)
	mxx += 5*eps
	mxx = math.floor(mxx/(eps/2.))*(eps/2.)
	mxy += 5*eps
	mxy = math.floor(mxy/(eps/2.))*(eps/2.)

	# Limitar o numero de retas no grid 
	maxline = 200
	stp = max(max(mxx - mnx, mxy - mny)/maxline, eps/2.)

	x = mnx
	grid_lines = []
	while(x < mxx):
		id = control.plot_vert_line(x)
		grid_lines.append(id)
		x += stp
	y = mny
	while(y < mxy):
		id = control.plot_horiz_line(y)
		grid_lines.append(id)
		y += stp
	
	control.sleep()
	return grid_lines

def clear_grid(grid_points, grid_lines):
	for ln in grid_lines:
		control.plot_delete(ln)
	for p, id in grid_points.items():
		p.unhilight(id)

a = None
b = None
ate = -1

def check(l, epsSq):
	global a, b, ate
	eps = math.sqrt(epsSq)

	grid_lines = plot_grid(l, eps)
	grid_points = {}

	grid = {}
	it = 0
	for it in range(len(l)):
		p = l[it]
		i = math.floor(p.x/(eps/2.))
		j = math.floor(p.y/(eps/2.))

		vid = None
		if(it >= ate):
			vid = p.hilight(COLOR_ALT3)
			grid_points[p] = vid
			control.sleep()
			for di in range(-2, 3):
				for dj in range(-2, 3):
					ii = i + di
					jj = j + dj
					if ii in grid and jj in grid[ii]:
						distSq = getdist2(p, grid[ii][jj])
						# Fazer alteracao de grid no final
						if(distSq < epsSq):
							a = grid[ii][jj]
							b = p
							clear_grid(grid_points, grid_lines)
							return distSq

		if not i in grid:
			grid[i] = {}
		grid[i][j] = p

		ate = max(ate, it)
		if(vid != None):
			p.unhilight(vid)
			del grid_points[p]
		hid = p.hilight(COLOR_ALT1)
		grid_points[p] = hid;
		control.sleep()

	clear_grid(grid_points, grid_lines)
	return -1;


def Randomized (l):
	global a, b, cntdist, ate
	cntdist = 0
	ate = -1
	"Algoritmo randomizado para encontrar o par de pontos mais proximo"
	if len (l) < 2: return None

	shuffle(l)

	a = l[0]
	b = l[1]
	epsSq = getdist2(a, b)
	while(epsSq > 0):
		epsSq = check(l, epsSq)
	
	a.lineto(b)
	ret = Segment (a, b)
	ret.extra_info = 'distancia: %.2f, chamadas de dist2: %d'%(math.sqrt (getdist2 (a, b)), cntdist)
	return ret

