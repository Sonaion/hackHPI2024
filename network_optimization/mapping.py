COMMERCIAL = 'commercial'
RESIDENTIAL = 'residential'
HIGH_DENSITY_RESIDENTIAL = 'high_density_residential'
INDUSTRIAL = 'industrial'
CONSTRUCTION = 'construction'
RETAIL = 'retail'
TRANSPORT = 'transport'
FREE_FIELD = 'free_field'
FARM = 'farm'
WATER = 'water'
OTHER = 'other'

map = {
    "construction": CONSTRUCTION,
    "industrial": INDUSTRIAL,
    "greenhouse_horticulture": INDUSTRIAL,
    "residential": RESIDENTIAL,
    "allotments": RESIDENTIAL,
    "retail": RETAIL,
    "garages": TRANSPORT,
    "port": TRANSPORT,
    "depot": TRANSPORT,
    "brownfield": FREE_FIELD,
    "meadow": FREE_FIELD,
    "fairground": FREE_FIELD,
    "grass": FREE_FIELD,
    "greenfield": FREE_FIELD,
    "village_green": FREE_FIELD,
    "aquaculture": FARM,
    "animal_keeping": FARM,
    "flowerbed": FARM,
    "farmland": FARM,
    "farmyard": FARM,
    "paddy": FARM,
    "orchard": FARM,
    "plant_nursery": FARM,
    "vineyard": FARM,
    "basin": WATER,
    "reservoir": WATER,
    "salt_pond": WATER,
}


def get_all_usage_types():
    return [COMMERCIAL, RESIDENTIAL, INDUSTRIAL, CONSTRUCTION, RETAIL, TRANSPORT, FREE_FIELD, FARM, WATER, OTHER]

def get_useable_areas():
    return [FREE_FIELD, FARM, OTHER]

def map_to_usage_type(landuse):
    return map.get(landuse, OTHER)


ROAD = 'road'
road_map = {
    "motorway": ROAD,
    "trunk": ROAD,
    "primary": ROAD,
    "secondary": ROAD,
    "tertiary": ROAD,
    "unclassified": ROAD,
    "residential": ROAD,
    "motorway_link": ROAD,
    "trunk_link": ROAD,
    "primary_link": ROAD,
    "secondary_link": ROAD,
    "tertiary_link": ROAD,
    "living_street": ROAD,
    "service": ROAD,
    "pedestrian": ROAD,
    "busway": ROAD,
}


def get_all_highway_types():
    return [ROAD, OTHER]


def map_to_highway_type(highway):
    return road_map.get(highway, OTHER)


building_map = {
    "yes": RESIDENTIAL,
    "bungalow": RESIDENTIAL,
    "cabin": RESIDENTIAL,
    "detached": RESIDENTIAL,
    "dormitory": RESIDENTIAL,
    "house": RESIDENTIAL,
    "residential": RESIDENTIAL,
    "semidetached_house": RESIDENTIAL,
    "static_caravan": RESIDENTIAL,
    "terrace": RESIDENTIAL,
    "allotment_house": RESIDENTIAL,
    "boathouse": RESIDENTIAL,
    "hut": RESIDENTIAL,
    "shed": RESIDENTIAL,

    "carport": TRANSPORT,
    "garage": TRANSPORT,
    "garages": TRANSPORT,
    "parking": TRANSPORT,

    "apartments": HIGH_DENSITY_RESIDENTIAL,
    "hotel": HIGH_DENSITY_RESIDENTIAL,
    "barracks": HIGH_DENSITY_RESIDENTIAL,

    "industrial": INDUSTRIAL,
    "warehouse": INDUSTRIAL,
    "hangar": INDUSTRIAL,

    "commercial": COMMERCIAL,
    "office": COMMERCIAL,
    "bakehouse": COMMERCIAL,
    "grandstand": COMMERCIAL,
    "pavilion": COMMERCIAL,
    "riding_hall": COMMERCIAL,
    "sports_hall": COMMERCIAL,
    "sports_centre": COMMERCIAL,
    "stadium": COMMERCIAL,
    "civic": COMMERCIAL,
    "college": COMMERCIAL,
    "fire_station": COMMERCIAL,
    "government": COMMERCIAL,
    "gatehouse": COMMERCIAL,
    "hospital": COMMERCIAL,
    "kindergarten": COMMERCIAL,
    "musuem": COMMERCIAL,
    "public": COMMERCIAL,
    "school": COMMERCIAL,
    "toilets": COMMERCIAL,
    "train_station": COMMERCIAL,
    "university": COMMERCIAL,
    "container": COMMERCIAL,

    "kiosk": RETAIL,
    "retail": RETAIL,
    "supermarket": RETAIL,

    "farm": FARM,
    "barn": FARM,
    "conservatory": FARM,
    "greenhouse": FARM,
    "ger": FARM,

    "construction": CONSTRUCTION,

    "religious": OTHER,
    "cathedral": OTHER,
    "chapel": OTHER,
    "church": OTHER,
    "kingdom_hall": OTHER,
    "mosque": OTHER,
    "presbytery": OTHER,
    "shrine": OTHER,
    "synagogue": OTHER,
    "temple": OTHER,
    "tree_house": OTHER,
}


def get_all_building_types():
    return [COMMERCIAL, RESIDENTIAL, HIGH_DENSITY_RESIDENTIAL, INDUSTRIAL, CONSTRUCTION, RETAIL, TRANSPORT, FARM, OTHER]


def get_used_building_types():
    return [COMMERCIAL, RESIDENTIAL, HIGH_DENSITY_RESIDENTIAL, INDUSTRIAL, RETAIL, TRANSPORT, FARM]


def map_to_building_type(building):
    return building_map.get(building, OTHER)
