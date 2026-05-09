"""Filter classes used by `NEODatabase.query`.

Each filter is a callable predicate (CloseApproach -> bool). The
`create_filters` factory builds the right combination from CLI args.

`limit` lets the caller cap the number of results returned by an iterator.
"""
import operator
import itertools


class AttributeFilter:
    """Generic attribute-vs-reference filter (e.g. `time >= 2020-01-01`)."""

    def __init__(self, op, value):
        """Store the comparison operator + the reference value."""
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Return True iff the approach's attribute satisfies op(value)."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Pull the relevant attribute from a CloseApproach (override me)."""
        raise NotImplementedError

    def __repr__(self):
        """Computer-readable repr."""
        return (f"{type(self).__name__}(op=operator.{self.op.__name__}, "
                f"value={self.value})")


class DateFilter(AttributeFilter):
    """Filter close approaches by their `date()` of approach."""

    @classmethod
    def get(cls, approach):
        """Return the date of the approach (None if it has no time)."""
        return approach.time.date() if approach.time else None


class DistanceFilter(AttributeFilter):
    """Filter close approaches by their nominal approach distance (au)."""

    @classmethod
    def get(cls, approach):
        """Return the approach distance in astronomical units."""
        return approach.distance


class VelocityFilter(AttributeFilter):
    """Filter close approaches by their relative velocity (km/s)."""

    @classmethod
    def get(cls, approach):
        """Return the approach relative velocity in km/s."""
        return approach.velocity


class DiameterFilter(AttributeFilter):
    """Filter close approaches by the parent NEO's diameter (km)."""

    @classmethod
    def get(cls, approach):
        """Return the parent NEO's diameter in km, or NaN if missing."""
        return approach.neo.diameter if approach.neo else float('nan')


class HazardousFilter(AttributeFilter):
    """Filter close approaches by the parent NEO's hazardous flag."""

    @classmethod
    def get(cls, approach):
        """Return the parent NEO's hazardous flag (False if missing)."""
        return approach.neo.hazardous if approach.neo else False


def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    """Build the list of predicates from `main.py`-style kwargs."""
    filters = []
    if date is not None:
        filters.append(DateFilter(operator.eq, date))
    if start_date is not None:
        filters.append(DateFilter(operator.ge, start_date))
    if end_date is not None:
        filters.append(DateFilter(operator.le, end_date))
    if distance_min is not None:
        filters.append(DistanceFilter(operator.ge, distance_min))
    if distance_max is not None:
        filters.append(DistanceFilter(operator.le, distance_max))
    if velocity_min is not None:
        filters.append(VelocityFilter(operator.ge, velocity_min))
    if velocity_max is not None:
        filters.append(VelocityFilter(operator.le, velocity_max))
    if diameter_min is not None:
        filters.append(DiameterFilter(operator.ge, diameter_min))
    if diameter_max is not None:
        filters.append(DiameterFilter(operator.le, diameter_max))
    if hazardous is not None:
        filters.append(HazardousFilter(operator.eq, hazardous))
    return filters


def limit(iterator, n=None):
    """Return at most `n` items from `iterator` (all if n is None or 0)."""
    if not n:
        return iterator
    return itertools.islice(iterator, n)
