from geopy.distance import distance


class Point:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    def __str__(self):
        return f"lat<{self.lat}>lon<{self.long}>"

    def distance(self, point):
        return distance((self.lat, self.long), (point.lat, point.long)).meters
