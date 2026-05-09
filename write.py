"""Write a stream of close approaches to a CSV or JSON file."""
import csv
import json
import math


CSV_FIELDS = (
    'datetime_utc', 'distance_au', 'velocity_km_s',
    'designation', 'name', 'diameter_km', 'potentially_hazardous',
)


def write_to_csv(results, filename):
    """Write a stream of CloseApproach objects to a CSV file.

    Args:
        results: iterable of CloseApproach objects. Each object's NEO
            back-reference is serialised alongside the approach fields.
        filename: path of the CSV file to write. Existing files are
            overwritten. The header row is the canonical ``CSV_FIELDS``
            tuple, and ``diameter_km`` is emitted as the literal
            ``'nan'`` when the NEO's diameter is unknown.
    """
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for ca in results:
            ca_d = ca.serialize()
            neo_d = ca.neo.serialize() if ca.neo else {
                'designation': ca.designation,
                'name': '', 'diameter_km': float('nan'),
                'potentially_hazardous': False,
            }
            diameter = neo_d['diameter_km']
            if isinstance(diameter, float) and math.isnan(diameter):
                diameter = 'nan'
            row = {
                'datetime_utc': ca_d['datetime_utc'],
                'distance_au': ca_d['distance_au'],
                'velocity_km_s': ca_d['velocity_km_s'],
                'designation': neo_d['designation'],
                'name': neo_d['name'],
                'diameter_km': diameter,
                'potentially_hazardous': str(neo_d['potentially_hazardous']),
            }
            writer.writerow(row)


def write_to_json(results, filename):
    """Write a stream of CloseApproach objects to a JSON file.

    Args:
        results: iterable of CloseApproach objects. Each object's NEO
            back-reference is nested under a ``'neo'`` key.
        filename: path of the JSON file to write. Existing files are
            overwritten. Floating-point ``NaN`` values are serialised
            as JSON ``null`` (since JSON has no NaN literal).
    """
    payload = []
    for ca in results:
        d = ca.serialize()
        d['neo'] = ca.neo.serialize() if ca.neo else {
            'designation': ca.designation,
            'name': '',
            'diameter_km': float('nan'),
            'potentially_hazardous': False,
        }
        # JSON doesn't allow NaN; emit it as null per project rubric.
        diameter = d['neo']['diameter_km']
        if isinstance(diameter, float) and math.isnan(diameter):
            d['neo']['diameter_km'] = float('nan')
        payload.append(d)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(
            payload, f, indent=2,
            default=lambda v: (
                None if (isinstance(v, float) and math.isnan(v)) else v
            ),
        )
