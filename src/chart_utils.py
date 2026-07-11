import matplotlib.pyplot as plt
from style import *


def createFigure(figsize=DEFAULT_FIGURE_SIZE):
    fig, ax = plt.subplots(figsize=figsize)
    return fig , ax 


def applyChartGrid(ax,axis="both",linestyle=GRID_LINESTYLE,alpha = GRID_ALPHA):
     ax.grid(axis=axis,linestyle=linestyle,alpha=alpha)
    
    