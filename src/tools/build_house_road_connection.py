import build_road_network
import src.create_nodes as create_nodes


def build_house_road_connection():
    _, buildings = create_nodes.create_graph()
    road_network = build_road_network.build_road_network()
    
    
    return house_connections