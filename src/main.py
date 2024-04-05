from tools.build_road_network import build_road_network
from create_nodes import create_graph

if __name__ == '__main__':
    road_network = build_road_network()
    areas, buildings = create_graph()

    for building in buildings:
        print(building.nearest_road(road_network))
