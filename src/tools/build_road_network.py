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
                    network[prevPointID] = (prevPoint, [])

                network[prevPointID][1].append((pointID, dist))

                if pointID not in network:
                    network[pointID] = (point, [])

                network[pointID][1].append((prevPointID, dist))
                prevPoint = point

    return network

def build_road_network2():
    network = {}
    road_points = []

    with open("src/data/total_Potsdam.json", "r") as f:
        data = json.load(f)
        #iterate over all roads
        for _, road in data["highways"].items():
            #iterate over all points in the road
            prevPoint = None
            for point in road["geometry"]:
                if prevPoint is None:
                    prevPoint = point
                    continue

                prevPointID = get_point_id(prevPoint)
                pointID = get_point_id(point)

                dist = calc_distance((prevPoint["lat"], prevPoint["lon"]), (point["lat"], point["lon"]))

                if prevPointID not in network:
                    road_points.append((prevPointID, (prevPoint["lat"], prevPoint["lon"])))
                    network[prevPointID] = []
                network[prevPointID].append((pointID, dist))

                if pointID not in network:
                    road_points.append((pointID, (point["lat"], point["lon"])))
                    network[pointID] = []

                network[pointID].append((prevPointID, dist))

                prevPoint = point
    return network, road_points



def calc_distance(point1, point2):
    x_dist = (point1[0] - point2[0])
    y_dist = (point1[1] - point2[1]) * 1.585
    return (x_dist ** 2 + y_dist ** 2) ** 0.5
    # return distance((point1["lat"], point1["lon"]), (point2["lat"], point2["lon"])).meters

def calc_dist_meter(point1, point2):
    return calc_distance(point1, point2) * 111249.23412498034

def calc_distance2(point1, point2):
    return distance((point1["lat"], point1["lon"]), (point2["lat"], point2["lon"])).meters

def get_point_id(point):
    return f"lat<{point['lat']}>lon<{point['lon']}>"


def get_point_cords(point_id, network):
    # lat = point_id.split("lat<")[1].split(">lon<")[0]
    # lon = point_id.split("lat<")[1].split(">lon<")[1].split(">")[0]
    # return {"lat": lat, "lon": lon}
    return network[point_id][0]
