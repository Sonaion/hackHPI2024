import json
from geopy.distance import distance


def build_road_network():
    network = {}

    with open("src/data/total_Potsdam.json", "r") as f:
        data = json.load(f)
        for _, road in data["highways"].items():
            prevPoint = None

            for point in road["geometry"]:
                if prevPoint is None:
                    prevPoint = point
                    continue

                prevPointID = get_point_id(prevPoint)
                pointID = get_point_id(point)

                dist = calc_distance(prevPoint, point)

                if prevPointID not in network:
                    network[prevPointID] = []

                network[prevPointID].append((pointID, dist))

                if pointID not in network:
                    network[pointID] = []

                network[pointID].append((prevPointID, dist))
                prevPoint = point

    return network


def calc_distance(point1, point2):
    return distance((point1["lat"], point1["lon"]), (point2["lat"], point2["lon"])).meters


def get_point_id(point):
    return f"lat<{point['lat']}>lon<{point['lon']}>"


def get_point_cords(point_id):
    lat = point_id.split("lat<")[1].split(">lon<")[0]
    lon = point_id.split("lat<")[1].split(">lon<")[1].split(">")[0]
    return {"lat": lat, "lon": lon}
