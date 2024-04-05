import dataclasses
import uuid

@dataclasses.dataclass
class Coordinate:
    lat: float
    lon: float

    def serialize(self):
        return {
            "lat": self.lat,
            "lon": self.lon
        }

    @staticmethod
    def deserialize(data):
        return Coordinate(
            lat=data["lat"],
            lon=data["lon"]
        )


@dataclasses.dataclass
class Shapes:
    id: uuid.UUID
    type: str
    geometry: list[Coordinate]
    open: bool = False

    def serialize(self):
        return {
            "id": str(self.id),
            "type": self.type,
            "geometry": [coord.serialize() for coord in self.geometry],
            "open": self.open
        }

    @staticmethod
    def deserialize(data):
        return Shapes(
            id=uuid.UUID(data["id"]),
            type=data["type"],
            open=data["open"],
            geometry=[Coordinate.deserialize(coord) for coord in data["geometry"]]
        )

    def get_area(self):
        from shapely.geometry import Polygon
        import geopandas as gpd
        from area_calculation import gpd_geographic_area_line_integral

        latitudes = [coord.lat for coord in self.geometry]
        longitudes = [coord.lon for coord in self.geometry]


        # Create LineString geometry
        polygon_geometry = Polygon(zip(longitudes, latitudes))

        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame(geometry=[polygon_geometry])

        # Calculate area
        return gpd_geographic_area_line_integral(gdf)[0]
