"""A database of near-Earth objects and their close approaches.

NEODatabase indexes NEOs by primary designation and (when present) by name,
and links each close approach to the NEO it belongs to.
"""


class NEODatabase:
    """In-memory database wrapping a collection of NEOs and CloseApproaches.

    On construction the database builds two lookup tables for the NEOs
    (by designation, by name) and walks every close approach to attach
    it to its parent NEO. Approaches whose designation does not match
    any known NEO are dropped.
    """

    def __init__(self, neos, approaches):
        """Construct the database from iterables of NEOs and approaches.

        Args:
            neos: iterable of :class:`NearEarthObject`. The full
                collection is stored verbatim and indexed by
                designation (always) and by name (if the NEO has one).
            approaches: iterable of :class:`CloseApproach`. Each is
                attached to its parent NEO via the NEO's primary
                designation; approaches whose designation does not
                match any NEO are dropped from the database.
        """
        self._neos = list(neos)
        self._approaches = list(approaches)

        self._by_designation = {}
        self._by_name = {}
        for neo in self._neos:
            self._by_designation[neo.designation] = neo
            if neo.name:
                self._by_name[neo.name] = neo

        # Hook each approach to its NEO; orphans are dropped (NASA's data is
        # mostly clean but the test fixtures include unknown designations).
        kept = []
        for ca in self._approaches:
            neo = self._by_designation.get(ca._designation)
            if neo is None:
                continue
            ca.neo = neo
            neo.approaches.append(ca)
            kept.append(ca)
        self._approaches = kept

    def get_neo_by_designation(self, designation):
        """Return the NEO with the given primary ``designation``, or ``None``.

        Args:
            designation: the NEO's primary designation as a string (or
                anything ``str()`` can coerce; the lookup is by string
                key).

        Returns:
            The matching :class:`NearEarthObject` or ``None`` if no NEO
            in the database has that designation.
        """
        return self._by_designation.get(str(designation))

    def get_neo_by_name(self, name):
        """Return the NEO with the given IAU ``name``, or ``None``.

        Args:
            name: the NEO's IAU name (e.g. ``'Eros'``). The lookup is
                exact-match; ``None`` and the empty string never
                resolve to a NEO.

        Returns:
            The matching :class:`NearEarthObject` or ``None`` if no NEO
            in the database has that name.
        """
        return self._by_name.get(name)

    def query(self, filters=()):
        """Yield close approaches that match every filter in `filters`."""
        for ca in self._approaches:
            if all(f(ca) for f in filters):
                yield ca
