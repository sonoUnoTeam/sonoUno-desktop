#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 07:51:54 2022

@author: sonounoteam

This script is dedicated to 3D plot generation based on a LHC data set
"""

import numpy as np

#Global counters
count_colors = 0

#Global plot variables

def plot3D_init(figure):
    global ax_transversal, ax_longitudinal, fig
    fig = figure
    figure.clf()
    # =============
    # First subplot
    # =============
    # set up the axes for the first plot
    ax_transversal = figure.add_subplot(1, 2, 1, projection='3d')
    ax_transversal.set_xlabel('$X$')
    ax_transversal.set_ylabel('$Y$')
    ax_transversal.set_zlabel('$Z$')
    ax_transversal.set_xlim([-150,150])
    ax_transversal.set_ylim([-150,150])
    ax_transversal.set_zlim([-150,150])
    ax_transversal.view_init(90, 270)
    # ==============
    # Second subplot
    # ==============
    # set up the axes for the second plot
    ax_longitudinal = figure.add_subplot(1, 2, 2, projection='3d')
    ax_longitudinal.set_xlabel('$Z$')
    ax_longitudinal.set_ylabel('$Y$')
    ax_longitudinal.set_zlabel('$X$')
    ax_longitudinal.set_xlim([-300,300])
    ax_longitudinal.set_ylim([-300,300])
    ax_longitudinal.set_zlim([-300,300])
    ax_longitudinal.view_init(90, 270)
    # Refresh plot
    figure.tight_layout()
    figure.canvas.draw()
    return ax_transversal, ax_longitudinal

def plot_reset():
    global ax_transversal, ax_longitudinal, fig
    ax_longitudinal.cla()
    ax_transversal.cla()
    ax_transversal.set_xlabel('$X$')
    ax_transversal.set_ylabel('$Y$')
    ax_transversal.set_zlabel('$Z$')
    ax_longitudinal.set_xlabel('$Z$')
    ax_longitudinal.set_ylabel('$Y$')
    ax_longitudinal.set_zlabel('$X$')
    ax_transversal.set_xlim([-150,150])
    ax_transversal.set_ylim([-150,150])
    ax_transversal.set_zlim([-150,150])
    ax_longitudinal.set_xlim([-300,300])
    ax_longitudinal.set_ylim([-300,300])
    ax_longitudinal.set_zlim([-300,300])
    # Corte transversal
    ax_transversal.view_init(90, 270)
    ax_longitudinal.view_init(90, 270)
    # Refresh plot
    fig.tight_layout()
    fig.canvas.draw()
    
def get_plotcolours():
    plot_colours = ['blue','orange','green','red','purple','brown','pink','grey','olive','cyan']
    return plot_colours

def get_count_colors():
    return count_colors

def set_count_colors(value):
    global count_colors
    count_colors = value

#def plot_muontrack(ax_transversal, ax_longitudinal, track_elements, energy=3):
def plot_muontrack(track_elements, energy=3):
    global count_colors
    color = get_plotcolours()[count_colors]
    ax_transversal.plot3D(
        [float(track_elements[-6]),float(track_elements[-3])*energy],
        [float(track_elements[-5]),float(track_elements[-2])*energy],
        [float(track_elements[-4]),float(track_elements[-1])*energy],
        color)
    # Corte longitudinal
    ax_longitudinal.plot3D(
        [float(track_elements[-4]),float(track_elements[-1])*energy],
        [float(track_elements[-5]),float(track_elements[-2])*energy],
        [float(track_elements[-6]),float(track_elements[-3])*energy],
        color)
    count_colors = count_colors + 1
    # Refresh plot
    fig.tight_layout()
    fig.canvas.draw()
    
def plot_innertrack(track_elements):
    global count_colors
    color = get_plotcolours()[count_colors]
    ax_transversal.plot3D(
        [float(track_elements[-6]),float(track_elements[-3])],
        [float(track_elements[-5]),float(track_elements[-2])],
        [float(track_elements[-4]),float(track_elements[-1])],
        color)
    # Corte longitudinal
    ax_longitudinal.plot3D(
        [float(track_elements[-4]),float(track_elements[-1])],
        [float(track_elements[-5]),float(track_elements[-2])],
        [float(track_elements[-6]),float(track_elements[-3])],
        color)
    count_colors = count_colors + 1
    # Refresh plot
    fig.tight_layout()
    fig.canvas.draw()
    
def plot_cluster(phi,theta,eta,amplitud=10):
    """
    Hago una esfera
    """
    if np.abs(eta) < 1.5:
        r = 150
    else:
        r = 210
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    # Make data
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = amplitud * np.outer(np.cos(u), np.sin(v)) + x
    y = amplitud * np.outer(np.sin(u), np.sin(v)) + y
    z = amplitud * np.outer(np.ones(np.size(u)), np.cos(v)) + z
    # Plot
    ax_longitudinal.plot_surface(z, y, x, color='b')
    ax_transversal.plot_surface(x, y, z, color='b')
    # Refresh plot
    fig.tight_layout()
    fig.canvas.draw()
