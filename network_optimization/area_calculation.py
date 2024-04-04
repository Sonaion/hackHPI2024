import numpy as np

from shapely.geometry.polygon import orient


def gpd_geographic_area(geodf):
    if not geodf.crs and geodf.crs.is_geographic:
        raise TypeError('geodataframe should have geographic coordinate system')

    geod = geodf.crs.get_geod()

    def area_calc(geom):
        if geom.geom_type not in ['MultiPolygon', 'Polygon']:
            return np.nan

        # For MultiPolygon do each separately
        if geom.geom_type == 'MultiPolygon':
            return np.sum([area_calc(p) for p in geom.geoms])

        # orient to ensure a counter-clockwise traversal.
        # See https://pyproj4.github.io/pyproj/stable/api/geod.html
        # geometry_area_perimeter returns (area, perimeter)
        return geod.geometry_area_perimeter(orient(geom, 1))[0]

    return geodf.geometry.apply(area_calc)


from shapely.geometry import Polygon


def line_integral_polygon_area(geom, radius=6378137):
    """
    Computes area of spherical polygon, assuming spherical Earth.
    Returns result in ratio of the sphere's area if the radius is specified.
    Otherwise, in the units of provided radius.
    lats and lons are in degrees.

    from https://stackoverflow.com/a/61184491/6615512
    """
    if geom.geom_type not in ['MultiPolygon', 'Polygon']:
        return np.nan

    # For MultiPolygon do each separately
    if geom.geom_type == 'MultiPolygon':
        return np.sum([line_integral_polygon_area(p) for p in geom.geoms])

    # parse out interior rings when present. These are "holes" in polygons.
    if len(geom.interiors) > 0:
        interior_area = np.sum([line_integral_polygon_area(Polygon(g)) for g in geom.interiors])
        geom = Polygon(geom.exterior)
    else:
        interior_area = 0

    # Convert shapely polygon to a 2 column numpy array of lat/lon coordinates.
    geom = np.array(geom.boundary.coords)

    lats = np.deg2rad(geom[:, 1])
    lons = np.deg2rad(geom[:, 0])

    # Line integral based on Green's Theorem, assumes spherical Earth

    # close polygon
    if lats[0] != lats[-1]:
        lats = np.append(lats, lats[0])
        lons = np.append(lons, lons[0])

    # colatitudes relative to (0,0)
    a = np.sin(lats / 2) ** 2 + np.cos(lats) * np.sin(lons / 2) ** 2
    colat = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    # azimuths relative to (0,0)
    az = np.arctan2(np.cos(lats) * np.sin(lons), np.sin(lats)) % (2 * np.pi)

    # Calculate diffs
    # daz = np.diff(az) % (2*pi)
    daz = np.diff(az)
    daz = (daz + np.pi) % (2 * np.pi) - np.pi

    deltas = np.diff(colat) / 2
    colat = colat[0:-1] + deltas

    # Perform integral
    integrands = (1 - np.cos(colat)) * daz

    # Integrate
    area = abs(sum(integrands)) / (4 * np.pi)

    area = min(area, 1 - area)
    if radius is not None:  # return in units of radius
        return (area * 4 * np.pi * radius ** 2) - interior_area
    else:  # return in ratio of sphere total area
        return area - interior_area


# a wrapper to apply the method to a geo data.frame
def gpd_geographic_area_line_integral(geodf):
    return geodf.geometry.apply(line_integral_polygon_area)
