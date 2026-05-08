"""A database of near-Earth objects and their close approaches.

NEODatabase indexes NEOs by primary designation and (when present) by name,
and links each close approach to the NEO it belongs to.
"""


class NEODatabase:
    def __init__(self, neos, approaches):
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
        return self._by_designation.get(str(designation))

    def get_neo_by_name(self, name):
        return self._by_name.get(name)

    def query(self, filters=()):
        """Yield close approaches that match every filter in `filters`."""
        for ca in self._approaches:
            if all(f(ca) for f in filters):
                yield ca
