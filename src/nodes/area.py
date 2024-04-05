class Area:
    def __init__(self, id, type, points):
        self.id = id
        self.type = type
        self.points = points
        self.factored_points = [{'lat': p['lat'], 'lon': p['lon']*1.585} for p in points]

        self.is_open = True
        self.avg_point = self.calculate_avg_point()
        self.avg_point_arr = [self.avg_point['lat'], self.avg_point['lon']]
        self.area = self.calculate_area()

    def calculate_avg_point(self):
        avg_lat = sum([point['lat'] for point in self.points]) / len(self.points)
        avg_lon = sum([point['lon'] for point in self.points]) / len(self.points)

        return {
            'lat': avg_lat,
            'lon': avg_lon
        }

    def calculate_area(self):
        # calculate the area of the polygon
        n = len(self.factored_points)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.factored_points[i]['lat'] * self.factored_points[j]['lon']
            area -= self.factored_points[j]['lat'] * self.factored_points[i]['lon']
        area = abs(area) / 2.0
        return area