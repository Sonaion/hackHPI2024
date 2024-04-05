from src.nodes.consumption import Consumption

class Building:
    def __init__(self, id, type, summer_consumption, winter_consumption, points):
        self.id = id
        self.type = type

        self.summer_electricity_consumption = Consumption(summer_consumption['Electro'])
        self.summer_heating_consumption = Consumption(summer_consumption['Heating'])
        self.winter_electricity_consumption = Consumption(winter_consumption['Electro'])
        self.winter_heating_consumption = Consumption(winter_consumption['Heating'])

        self.points = points
        self.avg_point = self.calculate_avg_point()
        self.avg_point_arr = [self.avg_point['lat'], self.avg_point['lon']]

        self.is_open = False

    def calculate_avg_point(self):
        avg_lat = sum([point['lat'] for point in self.points]) / len(self.points)
        avg_lon = sum([point['lon'] for point in self.points]) / len(self.points)

        return {
            'lat': avg_lat,
            'lon': avg_lon
        }