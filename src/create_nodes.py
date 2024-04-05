import json

from nodes.area import Area
from nodes.building import Building
from filter import filter_data


def create_graph(path='./data/total_Potsdam_with_energies.json'):
    data = read_data(path)

    areas = create_areas(data['areas'])
    buildings = create_buildings(data['buildings'])

    data = filter_data(buildings, areas, roads=[])

    return areas, buildings


def create_areas(data):
    areas = []

    for id, row in data.items():
        areas.append(Area(
            id=id,
            type=row['type'],
            points=row['geometry']
        ))

    return areas


def create_buildings(data):
    buildings = []

    for id, row in data.items():
        buildings.append(Building(
            id=id,
            type=row['type'],
            winter_consumption=row['winter'],
            summer_consumption=row['summer'],
            points=row['geometry']
        ))

    return buildings


def read_data(path: str):
    # Read JSON string from file
    with open(path, 'r') as file:
        json_string = file.read()

    # Convert JSON string to a Python dictionary
    return json.loads(json_string)
