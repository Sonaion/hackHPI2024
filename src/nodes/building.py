from nodes.consumption import Consumption
from tools.build_road_network import calc_dist_meter, get_point_cords


class Building:
    def __init__(self, id, type, summer_consumption, winter_consumption, points):
        self.id = id
        self.type = type

        self.summer_electricity_consumption = Consumption(
            summer_consumption['Electro'])
        self.summer_heating_consumption = Consumption(
            summer_consumption['Heating']) if 'Heating' in summer_consumption else None
        self.winter_electricity_consumption = Consumption(
            winter_consumption['Electro'])
        self.winter_heating_consumption = Consumption(
            winter_consumption['Heating']) if 'Heating' in winter_consumption else None

        self.points = points
        self.factored_points = [{'lat': p['lat'], 'lon': p['lon']*1.585} for p in points]
        self.avg_point = self.calculate_avg_point()
        self.avg_point_arr = [self.avg_point['lat'], self.avg_point['lon']]

        self.is_open = False

    def calculate_avg_point(self):
        avg_lat = sum([point['lat']
                      for point in self.points]) / len(self.points)
        avg_lon = sum([point['lon']
                      for point in self.points]) / len(self.points)

        return {
            'lat': avg_lat,
            'lon': avg_lon
        }

    def nearest_road(self, road_network):
        nearest_point = (None, None)

        # # optimize this function
        

        # for point_id, _ in road_network.items():
        #     if nearest_point[0] is None:
        #         nearest_point = (point_id, calc_distance(
        #             self.avg_point, get_point_cords(point_id, road_network)))
        #     else:
        #         dist = calc_distance(self.avg_point, get_point_cords(point_id, road_network))
        #         if dist < nearest_point[1]:
        #             nearest_point = (point_id, dist)

        # return nearest_point[0]

        for point_id, _ in road_network.items():
            dist = calc_dist_meter(self.avg_point, get_point_cords(point_id, road_network))
            if nearest_point[0] is None or dist < nearest_point[1]:
                nearest_point = (point_id, dist)