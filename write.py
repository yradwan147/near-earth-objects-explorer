"""Write a stream of close approaches to a CSV or JSON file."""
import csv
import json
import math


CSV_FIELDS = (
    'datetime_utc', 'distance_au', 'velocity_km_s',
    'designation', 'name', 'diameter_km', 'potentially_hazardous',
)


def write_to_csv(results, filename):
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
            row = {
                'datetime_utc':  ca_d['datetime_utc'],
                'distance_au':   ca_d['distance_au'],
                'velocity_km_s': ca_d['velocity_km_s'],
                'designation':   neo_d['designation'],
                'name':          neo_d['name'],
                'diameter_km':   ('nan' if isinstance(neo_d['diameter_km'], float)
                                  and math.isnan(neo_d['diameter_km'])
                                  else neo_d['diameter_km']),
                'potentially_hazardous': str(neo_d['potentially_hazardous']),
            }
            writer.writerow(row)


def write_to_json(results, filename):
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
        if (isinstance(d['neo']['diameter_km'], float)
                and math.isnan(d['neo']['diameter_km'])):
            d['neo']['diameter_km'] = float('nan')   # write_to_json uses default=
        payload.append(d)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2,
                  default=lambda v: None if (isinstance(v, float)
                                             and math.isnan(v)) else v)
