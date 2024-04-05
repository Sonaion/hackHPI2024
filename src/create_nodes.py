from src.nodes.area import Area
from src.nodes.building import Building

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