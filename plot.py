"""Plot orbits of satellites around the earth in 3D."""

import json
import sys
from typing import List, TypedDict

import matplotlib.pyplot as plt
import numpy as np

MU_EARTH = 398600.4418  # m^2 s^-2
R_EARTH = 6781.0  # km


class Satellite(TypedDict):
    """Keys in the JSON from celestrak.org."""
    OBJECT_NAME: str
    OBJECT_ID: str
    EPOCH: str
    MEAN_MOTION: float
    ECCENTRICITY: float
    INCLINATION: float
    RA_OF_ASC_NODE: float
    ARG_OF_PERICENTER: float
    MEAN_ANOMALY: float
    EPHEMERIS_TYPE: int
    CLASSIFICATION_TYPE: str
    NORAD_CAT_ID: str
    ELEMENT_SET_NO: int
    REV_AT_EPOCH: int
    BSTAR: float
    MEAN_MOTION_DOT: float
    MEAN_MOTION_DDOT: int


def plot(satellites: List[Satellite]) -> None:
    """The the orbits of the satellites."""
    # pylint: disable-msg=too-many-locals
    ax = plt.axes(projection="3d", computed_zorder=False)

    # Plot satellites.
    for sat in satellites:

        # radians
        raan = sat["RA_OF_ASC_NODE"]

        # radians
        inc = sat["INCLINATION"]

        # radians
        omega = sat["ARG_OF_PERICENTER"]

        R_raan = np.array(
            [
                [np.cos(raan), -np.sin(raan), 0.0],
                [np.sin(raan), np.cos(raan), 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        R_inc = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, np.cos(inc), -np.sin(inc)],
                [0.0, np.sin(inc), np.cos(inc)],
            ]
        )
        R_omega = np.array(
            [
                [np.cos(omega), -np.sin(omega), 0.0],
                [np.sin(omega), np.cos(omega), 0.0],
                [0.0, 0.0, 1.0],
            ]
        )

        # Calculate the rotation matrix.
        R = R_raan.dot(R_inc).dot(R_omega)

        # rad / sec
        n = sat["MEAN_MOTION"]

        # unitless
        e = sat["ECCENTRICITY"]

        # Calculate semi-major axis (km) from mean motion.
        a = (MU_EARTH ** (1.0 / 3.0)) / ((2 * n * np.pi / 86400) ** (2.0 / 3.0))

        # Calculate semi-minor axis (km) from semi-major axis and eccentricty.
        b = a * np.sqrt(1 - e**2)

        # Calculate the distance of the focus (km) from semi-major axis and eccentricity.
        c = a * e

        x, y, z = [], [], []

        for theta in np.linspace(0.0, 2 * np.pi, 100):
            arr0 = np.array([[a * np.cos(theta)], [b * np.sin(theta)], [0.0]])

            arr1 = np.array([[c], [0.0], [0.0]])

            P = np.matmul(R, arr0) - np.matmul(R, arr1)

            x += [P[0]]
            y += [P[1]]
            z += [P[2]]

        ax.plot(x, y, z, zorder=5, label=sat["OBJECT_NAME"])

    # Plot a wireframe of the Earth.
    u, v = np.mgrid[0 : 2 * np.pi : 20j, 0 : np.pi : 10j]
    ax.plot_wireframe(
        R_EARTH * np.cos(u) * np.sin(v),
        R_EARTH * np.sin(u) * np.sin(v),
        R_EARTH * np.cos(v),
        color="b",
        alpha=0.5,
        lw=0.5,
        zorder=0,
    )

    # Configure axis.
    ax.set_xlabel("X-axis (km)")
    ax.set_ylabel("Y-axis (km)")
    ax.set_zlabel("Z-axis (km)")
    ax.xaxis.set_tick_params(labelsize=7)
    ax.yaxis.set_tick_params(labelsize=7)
    ax.zaxis.set_tick_params(labelsize=7)
    ax.set_aspect("equal", adjustable="box")
    ax.legend()

    plt.show()


with open(f"{sys.argv[1]}.json", encoding="utf-8") as f:
    data = json.load(f)

plot(data[:40])
