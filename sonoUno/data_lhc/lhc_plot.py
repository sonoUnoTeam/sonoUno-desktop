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

def plot3D_init(figure):
    """
    Initialize the subplots needed to lhc plot with the given figure.

    Parameters
    ----------
    figure : TYPE Figure() of matplotlib

    """
    global ax_transversal, ax_longitudinal, fig
    fig = figure
    figure.clf()
    # Transversal subplot
    # set up the axes
    ax_transversal = figure.add_subplot(1, 2, 1, projection='3d')
    ax_transversal.set_xlabel('$X$')
    ax_transversal.set_ylabel('$Y$')
    ax_transversal.set_zlabel('$Z$')
    ax_transversal.set_xlim([-150,150])
    ax_transversal.set_ylim([-150,150])
    ax_transversal.set_zlim([-150,150])
    ax_transversal.view_init(90, 270)
    # Longitudinal subplot
    # set up the axes
    ax_longitudinal = figure.add_subplot(1, 2, 2, projection='3d')
    ax_longitudinal.set_xlabel('$Z$')
    ax_longitudinal.set_ylabel('$Y$')
    ax_longitudinal.set_zlabel('$X$')
    ax_longitudinal.set_xlim([-300,300])
    ax_longitudinal.set_ylim([-300,300])
    ax_longitudinal.set_zlim([-300,300])
    ax_longitudinal.view_init(90, 270)
    # Refresh plot to update changes
    figure.tight_layout()
    figure.canvas.draw()

def plot_reset():
    """
    Use the global vars (ax_transversal, ax_longitudinal, fig) to set the plot
    as at the beginning.
    """
    global ax_transversal, ax_longitudinal, fig
    # Transversal subplot
    ax_transversal.cla()
    ax_transversal.set_xlabel('$X$')
    ax_transversal.set_ylabel('$Y$')
    ax_transversal.set_zlabel('$Z$')
    ax_transversal.set_xlim([-150,150])
    ax_transversal.set_ylim([-150,150])
    ax_transversal.set_zlim([-150,150])
    ax_transversal.view_init(90, 270)
    # Longitudinal subplot
    ax_longitudinal.cla()
    ax_longitudinal.set_xlabel('$Z$')
    ax_longitudinal.set_ylabel('$Y$')
    ax_longitudinal.set_zlabel('$X$')
    ax_longitudinal.set_xlim([-300,300])
    ax_longitudinal.set_ylim([-300,300])
    ax_longitudinal.set_zlim([-300,300])
    ax_longitudinal.view_init(90, 270)
    # Refresh plot to update changes
    fig.tight_layout()
    fig.canvas.draw()
    
def get_plotcolours():
    """
    Returns
    -------
    plot_colours : TYPE list, provide the possible colours to represent the 
        different tracks on the plot.
    """
    plot_colours = ['blue','orange','green','red','purple','brown','pink','grey','olive','cyan']
    return plot_colours

def get_count_colors():
    """
    Returns
    -------
    count_colors : TYPE int, represent the actual index of the color used to plot.
    """
    return count_colors

def set_count_colors(value):
    """
    Parameters
    ----------
    value : TYPE int, represent the actual index of the color used to plot.
    """
    global count_colors
    count_colors = value

def plot_muontrack(track_elements, energy=3):
    """
    Plot the track of a muon, using the energy parameter to extend the track
    outside the inner detector (muons pass all the detector layers).

    Parameters
    ----------
    track_elements : TYPE list, contain the track elements
    energy : TYPE int, OPTIONAL value, the default is 3.
    """
    global count_colors
    color = get_plotcolours()[count_colors]
    ax_transversal.plot3D(
        [float(track_elements[-6]),float(track_elements[-3])*energy],
        [float(track_elements[-5]),float(track_elements[-2])*energy],
        [float(track_elements[-4]),float(track_elements[-1])*energy],
        color)
    ax_longitudinal.plot3D(
        [float(track_elements[-4]),float(track_elements[-1])*energy],
        [float(track_elements[-5]),float(track_elements[-2])*energy],
        [float(track_elements[-6]),float(track_elements[-3])*energy],
        color)
    count_colors = count_colors + 1
    # Refresh plot to update changes
    fig.tight_layout()
    fig.canvas.draw()
    
def plot_innertrack(track_elements):
    """
    Plot the track of all particles except muons.

    Parameters
    ----------
    track_elements: TYPE list, contain the track elements
    """
    global count_colors
    color = get_plotcolours()[count_colors]
    ax_transversal.plot3D(
        [float(track_elements[-6]),float(track_elements[-3])],
        [float(track_elements[-5]),float(track_elements[-2])],
        [float(track_elements[-4]),float(track_elements[-1])],
        color)
    ax_longitudinal.plot3D(
        [float(track_elements[-4]),float(track_elements[-1])],
        [float(track_elements[-5]),float(track_elements[-2])],
        [float(track_elements[-6]),float(track_elements[-3])],
        color)
    count_colors = count_colors + 1
    # Refresh plot to update changes
    fig.tight_layout()
    fig.canvas.draw()
    
def plot_cluster(phi,theta,eta,amplitud=10):
    """
    Plot the cluster using an sphere. Phi, theta and eta indicate the position
    where the sphere has to be plotted.

    Parameters
    ----------
    phi : TYPE float, phi value of the 3D sphere coordinates
    theta : TYPE float, theta value of the 3D sphere coordinates
    eta : TYPE float, eta value of the 3D sphere coordinates
    amplitud : TYPE int, OPTIONAL value, the default is 10, represent the 
        cluster energy
    """
    if amplitud != 10:
        amplitud = amplitud * 10 + 2
    # Depending on eta value set the r coordinate, information proportionated 
    # by WP5 team, REINFORCE project.
    if np.abs(eta) < 1.5:
        r = 150
    else:
        r = 210
    # Pass from sphere coordinates to cartesian coordinates
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    # Make the sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = amplitud * np.outer(np.cos(u), np.sin(v)) + x
    y = amplitud * np.outer(np.sin(u), np.sin(v)) + y
    z = amplitud * np.outer(np.ones(np.size(u)), np.cos(v)) + z
    # Plot the sphere in the subplots
    ax_longitudinal.plot_surface(z, y, x, color='k')
    ax_transversal.plot_surface(x, y, z, color='k')
    # Refresh plot to update changes
    fig.tight_layout()
    fig.canvas.draw()
