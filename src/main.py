import numpy as np
from tools.build_road_network import build_road_network2, calc_dist_meter
from create_nodes import create_graph
from geopy.distance import distance
import time

def test_speed():
    time1 = time.time()
    dist = distance((51, 13), (51.1, 13)).meters
    time2 = time.time()
    time3 = time.time()
    dist3 = calc_dist_meter((51, 13), (51.1, 13))
    time4 = time.time()
    print(dist, dist3)
    print(time2-time1, time4-time3)



if __name__ == '__main__':
    # road_network, road_points = build_road_network2()
    areas, buildings, building_roads, network = create_graph()
    print(len(building_roads))
    for id, road_point in building_roads:
        print(id, road_point)

