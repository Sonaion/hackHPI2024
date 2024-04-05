from nodes.building import Building
from nodes.area import Area
import statistics


def filter_data(buildings: list[Building], areas: list[Area], roads):
    all_lats = []
    all_lons = []
    for building in buildings:
        for point in building.points:
            all_lats.append(point['lat'])
            all_lons.append(point['lat'])

    median_lat = statistics.median(all_lats)
    median_lon = statistics.median(all_lons)

    filtered_buildings = []
    for building in buildings:
        if abs(building.points[0]['lat'] - median_lat) < 1.0 and abs(building.points[0]['lon'] - median_lon) < 1.0:
            filtered_buildings.append(building)

    filtered_areas = []
    for area in areas:
        if abs(area.points[0]['lat'] - median_lat) < 1.0 and abs(area.points[0]['lon'] - median_lon) < 1.0:
            filtered_areas.append(area)

    filtered_roads = []
    for road in roads:
        if abs(road.points[0]['lat'] - median_lat) < 1.0 and abs(road.points[0]['lon'] - median_lon) < 1.0:
            filtered_roads.append(road)

    return filtered_buildings, filtered_areas, filtered_roads
