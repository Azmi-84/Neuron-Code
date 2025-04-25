"""
This project simulates the gravitational interactions between earth and a hypothetical planet named "Super Jupiter", which is 500 times the mass of Jupiter. Here we will use NumPy to perform the calculations and visualize the results using Matplotlib.
"""

"""
    Learning:
    - How to use NumPy for numerical calculations
    - How to visualize data using Matplotlib
    - How to understand and apply Newton's law of universal gravitation
    - How to simulate gravitational interactions
    - How to simulate orbital mechanics of planets in the presence of a massive body
    - How to explore the effects of different masses and distances on gravitational force
    - How to calculate gravitational potential energy
    - How to implement numerical integration for simulating orbits
    - How to analyze the stability of orbits over time
    - How to visualize the trajectory of a planet in orbit
    - How to calculate escape velocity of a planet
"""

from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from matplotlib import animation
from matplotlib.lines import Line2D
from tqdm import trange

# Define constants
G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
AU = 1.496e11  # Astronomical unit in meters
YEAR = 365.25 * 24 * 3600  # Year in seconds
MM = 6e24  # Normalizing mass
ME = 6e24 / MM  # Mass of Earth in normalized units
MS = 2e30 / MM  # Mass of Sun in normalized units
MJ = 500 * 1.898e27 / MM  # Mass of Jupiter in normalized units
GG = (MM * G * YEAR**2) / (AU**3)  # Gravitational constant for simulation

# Define the Gravitational Force function


def gravitational_force(m1: float, m2: float, r: np.ndarray) -> np.ndarray:
    """
    Calculate the gravitational force between two masses.

    Parameters:
    m1 (float): Mass of the first object
    m2 (float): Mass of the second object
    r (np.ndarray): A NumPy array representing the displacement vector between the two bodies.

    Returns:
    np.ndarray: Gravitational force between the two objects
    """

    F_mag = (
        GG * m1 * m2 / (np.linalg.norm(r) + 1e-20) ** 2
    )  # 1e-20 is a tiny number added to avoid division by zero (numerical stability)

    # First Approach: Using the direction of the force vector
    # F_direction = -r / np.linalg.norm(r)
    # r_norm = np.linalg.norm(r) + 1e-20  # Corrected variable name and added definition
    # F = -GG * m1 * m2 / r_norm**3 * r  # r/r_norm gives unit vector

    # Second Approach: Using theta angle
    theta = np.arctan2(np.abs(r[1]), np.abs(r[0]) + 1e-20)
    F = F_mag * np.array([np.cos(theta), np.sin(theta)])
    F *= -np.sign(r)  # Apply the sign of r to the force vector
    return F


# Implementing a RK4 Solver
## RK4 Solver
def RK4Solver(
    t: float,
    r: np.ndarray,
    v: np.ndarray,
    h: float,
    planet: str,
    r_other: np.ndarray,
    v_other: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Fourth order Runge-Kutta solver for planetary motion.
    """

    def dr_dt(v: np.ndarray) -> np.ndarray:
        return v

    def dv_dt(r: np.ndarray, planet: str) -> np.ndarray:
        if planet == "earth":
            return (
                gravitational_force(ME, MS, r)
                + gravitational_force(ME, MJ, r - r_other)
            ) / ME
        elif planet == "jupiter":
            return (
                gravitational_force(MJ, MS, r)
                - gravitational_force(MJ, ME, r - r_other)
            ) / MJ

    k11 = dr_dt(v)
    k21 = dv_dt(r, planet)

    k12 = dr_dt(v + 0.5 * h * k21)
    k22 = dv_dt(r + 0.5 * h * k11, planet)

    k13 = dr_dt(v + 0.5 * h * k22)
    k23 = dv_dt(r + 0.5 * h * k12, planet)

    k14 = dr_dt(v + h * k23)
    k24 = dv_dt(r + h * k13, planet)

    y0 = r + h * (k11 + 2 * k12 + 2 * k13 + k14) / 6
    y1 = v + h * (k21 + 2 * k22 + 2 * k23 + k24) / 6

    return y0, y1
