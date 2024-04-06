import math

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
        # Earth's radius in meters
        R = 6378137
        area = 0.0

        # Convert all coordinates from degrees to radians
        points_rad = [{'lat': math.radians(p['lat']), 'lon': math.radians(p['lon'])} for p in self.points]

        n = len(points_rad)
        for i in range(n):
            j = (i + 1) % n
            area += (points_rad[i]['lon'] - points_rad[j]['lon']) * (
                2 + math.sin(points_rad[i]['lat']) + math.sin(points_rad[j]['lat'])
            )

        area = -area * R * R / 2.0
        return abs(area)