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
    """Coerce a value to bool ('y'/'yes'/'true'/'1' map to True)."""
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
        """Construct a NEO from its NASA-JPL fields.

        Args:
            designation: NEO designation (e.g. ``'2020 AB1'``); required.
            name: human-readable name (e.g. ``'Eros'``), or None if unknown.
            diameter: estimated diameter in km; NaN if unknown.
            hazardous: True if NASA flags it as potentially hazardous.
            _extra: extra keyword arguments accepted-and-ignored so that
                the NEO can be constructed straight from a CSV ``DictReader``
                row without filtering the keys first.
        """
        self.designation = str(designation) if designation else ''
        self.name = name if name else None
        self.diameter = _to_float(diameter)
        self.hazardous = _to_bool(hazardous)
        self.approaches = []

    @property
    def fullname(self):
        """Return ``'designation (name)'`` or just ``designation``."""
        return f"{self.designation} ({self.name})" if self.name else self.designation

    def __str__(self):
        """Human-readable one-line summary used by ``main.py``."""
        haz = "is" if self.hazardous else "is not"
        diam = ("an unknown diameter" if math.isnan(self.diameter)
                else f"a diameter of {self.diameter:.3f} km")
        return (f"NEO {self.fullname} has {diam} and "
                f"{haz} potentially hazardous.")

    def __repr__(self):
        """Computer-readable repr — usable verbatim in a debugger."""
        return (f"NearEarthObject(designation={self.designation!r}, "
                f"name={self.name!r}, diameter={self.diameter:.3f}, "
                f"hazardous={self.hazardous!r})")

    def serialize(self):
        """Return a JSON/CSV-friendly dict of the NEO's public fields."""
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
        """Construct a CloseApproach record.

        Args:
            designation: designation of the NEO that made the approach
                (used by ``NEODatabase`` to link the record to its NEO).
            time: approach datetime (str ``'YYYY-MMM-DD HH:MM'`` or
                already a ``datetime``).
            distance: nominal approach distance in astronomical units.
            velocity: relative velocity at approach in km/s.
            neo: back-reference to the parent ``NearEarthObject`` once
                ``NEODatabase`` has linked them.
            _extra: see ``NearEarthObject.__init__``.
        """
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
        """Read-only NEO designation this approach belongs to."""
        return self._designation

    @property
    def time_str(self):
        """Return the approach time as a formatted string."""
        return datetime_to_str(self.time) if self.time else "an unknown time"

    def __str__(self):
        """Human-readable one-line summary used by ``main.py``."""
        neo_name = self.neo.fullname if self.neo else self._designation
        return (f"On {self.time_str}, '{neo_name}' approaches Earth at a "
                f"distance of {self.distance:.2f} au and a velocity of "
                f"{self.velocity:.2f} km/s.")

    def __repr__(self):
        """Computer-readable repr — usable verbatim in a debugger."""
        return (f"CloseApproach(time={self.time_str!r}, "
                f"distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        """Return a JSON/CSV-friendly dict of the approach's public fields."""
        return {
            "datetime_utc": datetime_to_str(self.time) if self.time else "",
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
        }
