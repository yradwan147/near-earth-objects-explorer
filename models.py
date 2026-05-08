"""Represent models for near-Earth objects and their close approaches."""
import math

from helpers import cd_to_datetime, datetime_to_str


def _to_float(value):
    """Coerce a value to float, returning NaN on empty/missing values."""
    try:
        if value is None or value == '':
            return float('nan')
        return float(value)
    except (TypeError, ValueError):
        return float('nan')


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    s = str(value).strip().lower()
    return s in ('y', 'yes', 'true', '1')


class NearEarthObject:
    """A near-Earth object (NEO).

    Required:  designation
    Optional:  name (None if missing), diameter (NaN if unknown),
               hazardous (False if unknown).
    """

    def __init__(self, designation, name=None, diameter=float('nan'),
                 hazardous=False, **_extra):
        self.designation = str(designation) if designation else ''
        self.name = name if name else None
        self.diameter = _to_float(diameter)
        self.hazardous = _to_bool(hazardous)
        self.approaches = []

    @property
    def fullname(self):
        return f"{self.designation} ({self.name})" if self.name else self.designation

    def __str__(self):
        haz = "is" if self.hazardous else "is not"
        diam = ("an unknown diameter" if math.isnan(self.diameter)
                else f"a diameter of {self.diameter:.3f} km")
        return (f"NEO {self.fullname} has {diam} and "
                f"{haz} potentially hazardous.")

    def __repr__(self):
        return (f"NearEarthObject(designation={self.designation!r}, "
                f"name={self.name!r}, diameter={self.diameter:.3f}, "
                f"hazardous={self.hazardous!r})")

    def serialize(self):
        return {
            "designation": self.designation,
            "name": self.name if self.name else "",
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous,
        }


class CloseApproach:
    """A close approach to Earth by an NEO."""

    def __init__(self, designation, time=None, distance=0.0, velocity=0.0,
                 neo=None, **_extra):
        self._designation = str(designation) if designation else ''
        if isinstance(time, str):
            self.time = cd_to_datetime(time) if time else None
        else:
            self.time = time
        self.distance = _to_float(distance)
        self.velocity = _to_float(velocity)
        self.neo = neo

    @property
    def designation(self):
        return self._designation

    @property
    def time_str(self):
        return datetime_to_str(self.time) if self.time else "an unknown time"

    def __str__(self):
        neo_name = self.neo.fullname if self.neo else self._designation
        return (f"On {self.time_str}, '{neo_name}' approaches Earth at a "
                f"distance of {self.distance:.2f} au and a velocity of "
                f"{self.velocity:.2f} km/s.")

    def __repr__(self):
        return (f"CloseApproach(time={self.time_str!r}, "
                f"distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        return {
            "datetime_utc": datetime_to_str(self.time) if self.time else "",
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
        }
