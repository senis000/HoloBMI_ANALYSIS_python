# some utils that may be shared among some plot functions
from typing import Optional

import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np


def open_plot(sizes: tuple = [8, 6]):
    fig = plt.figure(figsize=sizes)
    ax = fig.add_subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig, ax


def open_2subplots():
    fig = plt.figure(figsize=(14, 6))
    ax = fig.add_subplot(121)
    bx = fig.add_subplot(122)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    bx.spines["top"].set_visible(False)
    bx.spines["right"].set_visible(False)
    return fig, ax, bx


def open_xsubplots(num_subplots: int = 4):
    fig = plt.figure(figsize=(12, 8))
    subplots = []
    for ind in np.arange(1, num_subplots+1):
        ax = fig.add_subplot(np.ceil(np.sqrt(num_subplots)), np.sqrt(num_subplots), ind)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        subplots.append(ax)
    return fig, subplots


def save_plot(fig: plt.figure, ax: Optional, folder_path: Path, var_y: str = '', var_x: str = '',
              set_labels: bool = True):
    if set_labels:
        ax.set_xlabel(var_x)
        ax.set_ylabel(var_y)
    file_name = var_y + "_" + var_x
    file_png = file_name + ".png"
    fig.savefig(folder_path / file_png, bbox_inches="tight")
    file_eps = file_name + ".eps"
    fig.savefig(folder_path / file_eps, format='eps', bbox_inches="tight")
    plt.close(fig)