#!/usr/bin/env python
"""Algoritmo randomizado"""

from geocomp.common.segment import Segment
from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.config import *
from random import shuffle
import math

def redraw_points(l):
	global ate, painted_points

	for tp in painted_points:
		tp[0].unhilight(tp[1])
	painted_points.clear()
	for i in range(0, ate+1):
		painted_points.append([l[i], l[i].hilight('cyan')])
	for i in range(ate, len(l)):
		painted_points.append([l[i], l[i].hilight('white')])

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
	
	redraw_points(l)

	control.sleep()
	return grid_lines

def clear_grid(grid_lines):
	for ln in grid_lines:
		control.plot_delete(ln)

a = None
b = None
ate = -1

def check(l, epsSq):
	global a, b, ate, painted_points
	eps = math.sqrt(epsSq)

	grid_lines = plot_grid(l, eps)

	grid = {}
	it = 0
	ret = -1
	
	for it in range(len(l)):
		p = l[it]
		i = math.floor(p.x/(eps/2.))
		j = math.floor(p.y/(eps/2.))

		vid = None
		if(it > ate):
			ate = it
			vid = p.hilight('magenta')
			control.sleep()
			for di in range(-2, 3):
				for dj in range(-2, 3):
					ii = i + di
					jj = j + dj
					if ii in grid and jj in grid[ii]:
						distSq = dist2(p, grid[ii][jj])
						# Fazer alteracao de grid no final
						if(distSq < epsSq):
							a = grid[ii][jj]
							b = p
							ret = distSq

			control.plot_delete(vid)
			hid = p.hilight('cyan')
			painted_points.append([p, hid])

			if(ret != -1):
				clear_grid(grid_lines)
				return ret

		if not i in grid:
			grid[i] = {}
		grid[i][j] = p

	clear_grid(grid_lines)
	return ret;


def Randomized (l):
	global a, b, ate, painted_points
	painted_points = []
	cntdist = 0
	ate = -1
	"Algoritmo randomizado para encontrar o par de pontos mais proximo"
	if len (l) < 2: return None

	shuffle(l)

	a = l[0]
	b = l[1]
	epsSq = dist2(a, b)
	while(epsSq > 0):
		epsSq = check(l, epsSq)
	
	for tp in painted_points:
		tp[0].unhilight(tp[1])

	a.hilight('green')
	b.hilight('green')
	a.lineto(b)
	ret = Segment (a, b)
	ret.extra_info = 'distancia: %.2f'%(math.sqrt (dist2 (a, b)))
	return ret

