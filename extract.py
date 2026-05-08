"""Extract NEO and close-approach data from CSV / JSON files."""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read every row of `neo_csv_path` and return a list of `NearEarthObject`."""
    neos = []
    with open(neo_csv_path, 'r', encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            neos.append(NearEarthObject(
                designation=row.get('pdes', ''),
                name=row.get('name') or None,
                diameter=row.get('diameter') or float('nan'),
                hazardous=(row.get('pha') == 'Y'),
            ))
    return neos


def load_approaches(cad_json_path):
    """Read NASA's close-approach JSON file into a list of `CloseApproach`."""
    with open(cad_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fields = data['fields']
    idx = {name: i for i, name in enumerate(fields)}

    approaches = []
    for row in data['data']:
        approaches.append(CloseApproach(
            designation=row[idx['des']],
            time=row[idx['cd']],
            distance=row[idx['dist']],
            velocity=row[idx['v_rel']],
        ))
    return approaches
