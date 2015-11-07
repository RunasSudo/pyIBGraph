# -*- coding: utf-8 -*-
#    pyIBGraph - IB Physics (2016 syllabus) style graphs
#    Copyright (C) 2015  Yingtong Li (RunasSudo)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

DATA_FILE = "data.csv"
OUTPUT_NAME = "graph.pdf"

X_Q = r"P^{-1}"
X_U = r"kPa^{-1}"
Y_Q = r"V"
Y_U = r"cm^3"

EQ_POS = "upper left"
LEG_POS = "lower right"

SWING_MODE = "cap"
SWING_CENTRE = "midrange"

ERRORBAR_CAP_SIZE = 3
MINMAX_TRIES = 3

# ========== END CONFIGURATION PARAMETERS ==========

X_U = X_U.replace(r" ", r"\ ")
Y_U = Y_U.replace(r" ", r"\ ")

import matplotlib as mpl
import numpy as np

def LOBF(xvar, yvar, xmin, xmax):
	par = np.polyfit(xvar, yvar, 1, full=True)
	m = par[0][0]
	c = par[0][1]
	xl = [xmin, xmax]
	yl = [m*xx + c for xx in xl]

	variance = np.var(yvar)
	residuals = np.var([(m*xx + c - yy)  for xx,yy in zip(xvar,yvar)])
	Rsqr = 1-residuals/variance

	return m, c, xl, yl, Rsqr

def prettyNum(num):
	pretty = "{:.5g}".format(num)
	if "e" in pretty:
		pretty = pretty.replace("e", r"\times 10^{") + "}"
	return pretty

def signedPretty(num):
	pretty = prettyNum(num)
	if "-" in pretty:
		return pretty
	else:
		return "+" + pretty

import matplotlib.backend_bases
from matplotlib.backends.backend_pgf import FigureCanvasPgf
matplotlib.backend_bases.register_backend("pdf", FigureCanvasPgf)

pgf_with_lualatex = {
	"pgf.texsystem": "lualatex",
	"font.family": "serif",
	"text.usetex": True,
	"pgf.rcfonts": False,
	"pgf.preamble": [
		r"\usepackage{amsmath,amssymb}",
		#r"\usepackage[usenames,dvipsnames,svgnames,table]{xcolor}",
		#r"\usepackage[T1]{fontenc}",
		#r"\usepackage[utf8]{inputenc}",
		r"\usepackage[math-style=ISO, bold-style=ISO]{unicode-math}",
		r"\setmainfont[RawFeature=-tlig]{TeX Gyre Termes}",
		r"\setsansfont[RawFeature=-tlig]{TeX Gyre Heros}",
		r"\setmonofont[RawFeature=-tlig]{TeX Gyre Cursor}",
		r"\setmathfont[RawFeature=-tlig]{TeX Gyre Termes Math}",
	]
}
mpl.rcParams.update(pgf_with_lualatex)

import matplotlib.pyplot as plt

import csv
def getColumn(column):
	results = np.genfromtxt(DATA_FILE, delimiter=",", dtype = float)
	return [result[column] for result in results]
xvar = getColumn(0)
xunc = getColumn(1)
yvar = getColumn(2)
yunc = getColumn(3)

fig, ax = plt.subplots()

# Idiot method
for trial in range(0, MINMAX_TRIES):
	print("Processing trial {0}".format(trial))
	ax.clear()

	ax.grid(True)
	ax.autoscale_view(True, True, True)
	plt.xlabel("$" + X_Q + ("\\ /\\ \\mathrm{" + X_U + "}" if X_U != "" else "") + "$")
	plt.ylabel("$" + Y_Q + ("\\ /\\ \\mathrm{" + Y_U + "}" if Y_U != "" else "") + "$")

	# Plot the data points
	ax.scatter(xvar, yvar, color="#005c94", label="data")
	ax.errorbar(xvar, yvar, color="black", xerr=xunc, yerr=yunc, linestyle="None", capsize=ERRORBAR_CAP_SIZE)

	# Line of best fit
	m0, c0, xl0, yl0, Rsqr = LOBF(xvar, yvar, 0, max(xvar))

	# Maximum/minimum line
	xmed = False
	if SWING_CENTRE == "midrange":
		xmed = (min(xvar) + max(xvar)) / 2
	if SWING_CENTRE == "mean":
		xmed = np.mean(xvar)
	if SWING_CENTRE == "median":
		xmed = np.median(xvar)
	
	ymed = m0*xmed + c0
	
	mmax, cmax, xlmax, ylmax, _ = False, False, False, False, False
	mmin, cmin, xlmin, ylmin, _ = False, False, False, False, False
	
	if SWING_MODE != "ends":
		xabove, xbelow = False, False
		xabove = [ i for i,v in enumerate(xvar) if v>=xmed ][0] # First index of xvar above mean (to exclude)
		xbelow = [ i for i,v in enumerate(xvar) if v<=xmed ][-1]
		
		xmmax, ymmax = False, False
		xmmin, ymmin = False, False
		
		def tryPoint(x, y):
			global xmmax, ymmax, mmax, xmmin, ymmin, mmin
			m = (max(y, ymed) - min(y, ymed)) / (max(x, xmed) - min(x, xmed))
			if mmax == False or m > mmax:
				xmmax, ymmax, mmax = x, y, m
			if mmin == False or m < mmin:
				xmmin, ymmin, mmin = x, y, m
		
		for i in range(len(xvar)):
			if i != xabove and i != xbelow:
				# Do matplotlib magic
				capsize_in = ERRORBAR_CAP_SIZE / 72 * 2
				capsize_px = fig.dpi_scale_trans.transform([capsize_in, capsize_in])
				capsize_u = ax.transData.inverted().transform([capsize_px, capsize_px]) - ax.transData.inverted().transform([0, 0])
				capsize_ux = capsize_u[0][0]
				capsize_uy = capsize_u[0][1]
				
				if SWING_MODE == "cap":
					tryPoint(xvar[i] + xunc[i], yvar[i] + capsize_uy)
					tryPoint(xvar[i] + xunc[i], yvar[i] - capsize_uy)
					tryPoint(xvar[i] - xunc[i], yvar[i] + capsize_uy)
					tryPoint(xvar[i] - xunc[i], yvar[i] - capsize_uy)
					tryPoint(xvar[i] + capsize_ux, yvar[i] + yunc[i])
					tryPoint(xvar[i] - capsize_ux, yvar[i] + yunc[i])
					tryPoint(xvar[i] + capsize_ux, yvar[i] - yunc[i])
					tryPoint(xvar[i] - capsize_ux, yvar[i] - yunc[i])
				
				if SWING_MODE == "corner":
					tryPoint(xvar[i] + xunc[i], yvar[i] + yunc[i])
					tryPoint(xvar[i] + xunc[i], yvar[i] - yunc[i])
					tryPoint(xvar[i] - xunc[i], yvar[i] + yunc[i])
					tryPoint(xvar[i] - xunc[i], yvar[i] - yunc[i])
					tryPoint(xvar[i] + xunc[i], yvar[i] + yunc[i])
					tryPoint(xvar[i] - xunc[i], yvar[i] + yunc[i])
					tryPoint(xvar[i] + xunc[i], yvar[i] - yunc[i])
					tryPoint(xvar[i] - xunc[i], yvar[i] - yunc[i])
				
				if SWING_MODE == "bar":
					tryPoint(xvar[i] + xunc[i], yvar[i])
					tryPoint(xvar[i] - xunc[i], yvar[i])
					tryPoint(xvar[i], yvar[i] + yunc[i])
					tryPoint(xvar[i], yvar[i] - yunc[i])
		
		_, cmax, xlmax, ylmax, _ = LOBF([xmed, xmmax], [ymed, ymmax], 0, max(xvar))
		_, cmin, xlmin, ylmin, _ = LOBF([xmed, xmmin], [ymed, ymmin], 0, max(xvar))
	else:
		mmax, cmax, xlmax, ylmax, _ = LOBF([xvar[0] + xunc[0], xvar[-1] - xunc[-1]], [yvar[0] - yunc[0], yvar[-1] + yunc[-1]], 0, max(xvar))
		mmin, cmin, xlmin, ylmin, _ = LOBF([xvar[0] - xunc[0], xvar[-1] + xunc[-1]], [yvar[0] + yunc[0], yvar[-1] - yunc[-1]], 0, max(xvar))

	def shortQuantityAndUnit(q, u):
		if u == "":
			return q
		else:
			if r"\ " in u:
				return "\\left(" + q + "/\!\\left(\\mathrm{" + u + "}\\right)\\right)"
			else:
				return "\\left(" + q + "/\\mathrm{" + u + "}\\right)"

	plt.text(
		0.1 if "left" in EQ_POS else 0.9,
		0.95 if "upper" in EQ_POS else 0.05,
		"$" + shortQuantityAndUnit(Y_Q, Y_U) + "=" + prettyNum(m0) + shortQuantityAndUnit(X_Q, X_U) + signedPretty(c0) + "$\n$R^2=" + prettyNum(Rsqr) + "$",
		verticalalignment=("top" if "upper" in EQ_POS else "bottom"),
		horizontalalignment=("left" if "left" in EQ_POS else "right"),
		transform=ax.transAxes
	)

	plt.text(
		0.1 if "left" in EQ_POS else 0.9,
		0.85 if "upper" in EQ_POS else 0.15,
		"$" + shortQuantityAndUnit(Y_Q + "_\\mathrm{max}", Y_U) + "=" + prettyNum(mmax) + shortQuantityAndUnit(X_Q, X_U) + signedPretty(cmax) + "$\n$" + shortQuantityAndUnit(Y_Q + "_\\mathrm{min}", Y_U) + "=" + prettyNum(mmin) + shortQuantityAndUnit(X_Q, X_U) + signedPretty(cmin) + "$",
		verticalalignment=("top" if "upper" in EQ_POS else "bottom"),
		horizontalalignment=("left" if "left" in EQ_POS else "right"),
		transform=ax.transAxes, fontsize=10
	)

	# Plot the lines of best fit
	ax.plot(xl0, yl0, color="red", linewidth=2, label="line of best fit")
	ax.plot(xlmax, ylmax, color="#19aeff", label="min/max slope")
	ax.plot(xlmin, ylmin, color="#19aeff")

	#ax.autoscale_view(True, True, True)

	#xmin, xmax = ax.get_xlim()
	#ymin, ymax = ax.get_ylim()
	#if xmin > 0:
	#	ax.set_xlim(left=0)
	#if ymin > 0:
	#	ax.set_ylim(bottom=0)

ax.legend(loc=LEG_POS)

print("Saving figure")

plt.tight_layout()
plt.savefig(OUTPUT_NAME)
#plt.show()
