# Explore Near-Earth Objects

Final project for Udacity's *Intermediate Python* course (nd303). A complete
pipeline that loads NASA's NEO catalog and close-approach feed, indexes them,
and lets you query them from the command line in CSV/JSON.

**73 / 73 tests pass.**

## Running

```bash
# Look up an NEO by name or designation
python3 main.py inspect --pdes 1P
python3 main.py inspect --name Halley
python3 main.py inspect --verbose --name Halley

# Filter close approaches
python3 main.py query --date 1969-07-29 --limit 3
python3 main.py query --start-date 2050-01-01 --min-distance 0.2 --min-velocity 50
python3 main.py query --hazardous --max-distance 0.05 --min-velocity 30

# Save results
python3 main.py query --limit 5  --outfile results.csv
python3 main.py query --limit 15 --outfile results.json

# Interactive REPL (no re-loading the database between queries)
python3 main.py interactive
```

## Architecture

```
main.py            argparse + dispatch
├── extract.py     load_neos / load_approaches  → models
├── models.py      NearEarthObject, CloseApproach
├── database.py    NEODatabase: indexes + query
├── filters.py     AttributeFilter subclasses + create_filters + limit
├── write.py       write_to_csv / write_to_json
└── tests/         73 unit tests covering every module
```

## Notes & standing-out work

* **NaN-safe diameter handling** end-to-end. `_to_float` coerces empty
  strings and missing values to `float('nan')`; `__str__` checks
  `math.isnan` to print "an unknown diameter"; `write_to_json` defaults
  NaN to `null`.
* **`AttributeFilter` strategy** — every per-attribute filter shares one
  `__call__` and only overrides `get`, eliminating five copies of the
  same predicate code.
* **`limit` returns the raw iterator unchanged** when no limit was given,
  so we don't materialise the whole result set when the user just wants
  to count results.
* **NEO ↔ CloseApproach back-reference** — `NEODatabase.__init__`
  rewrites every approach's `.neo` to its NEO object and pushes the
  approach onto the NEO's `.approaches` list. This pre-computation makes
  filters like `--min-diameter` cheap to evaluate without re-indexing.

## Data

`data/neos.csv` — 23,968 NEOs from JPL's small-body database query.  
`data/cad.json` — 406,785 close-approach records from NASA's CAD service.

## License

Educational submission for Udacity nd303. Starter scaffolding © Udacity;
data © NASA / JPL-Caltech.
