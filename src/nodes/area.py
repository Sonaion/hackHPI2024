class Area:
    def __init__(self, id, type, points):
        self.id = id
        self.type = type
        self.points = points
        self.is_open = True
        self.avg_point = self.calculate_avg_point()
        self.avg_point_arr = [self.avg_point['lat'], self.avg_point['lon']]

    def calculate_avg_point(self):
        avg_lat = sum([point['lat'] for point in self.points]) / len(self.points)
        avg_lon = sum([point['lon'] for point in self.points]) / len(self.points)

        return {
            'lat': avg_lat,
            'lon': avg_lon
        }
