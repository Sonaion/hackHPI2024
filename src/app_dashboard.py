import json
import plotly.graph_objects as go
import streamlit as st

import re
from objects import Shapes, Coordinate
from create_nodes import create_graph
from tools.build_road_network import build_road_network

def generate_dict_shapes(used_entities, all_entities, color_map, open=False):
    valuesPerObject = {}
    for objectName in color_map.keys():
        if objectName not in used_entities:
            continue
        multiPolygonCoordinatesLon = []
        multiPolygonCoordinatesLat = []
        for entityId, entityObject in all_entities.items():
            if entityObject.type != objectName:
                continue
            coordinates = entityObject.geometry
            if len(coordinates) == 0:
                continue
            for coord in coordinates:
                multiPolygonCoordinatesLon.append(coord.lon)
                multiPolygonCoordinatesLat.append(coord.lat)
            if not open:
                multiPolygonCoordinatesLon.append(coordinates[0].lon)
                multiPolygonCoordinatesLat.append(coordinates[0].lat)
            multiPolygonCoordinatesLon.append(None)
            multiPolygonCoordinatesLat.append(None)

        valuesPerObject[objectName] = {
            "lon": multiPolygonCoordinatesLon,
            "lat": multiPolygonCoordinatesLat,
            "color": color_map[objectName]
        }
    return valuesPerObject


def render_main(map_style, used_areas, used_highways, used_buildings):
    st.header("City Management")
    areaColorMapping = st.session_state.areaColorMapping
    buildingColorMapping = st.session_state.buildingColorMapping
    highwayColorMapping = st.session_state.highwayColorMapping

    valuesPerArea = generate_dict_shapes(used_areas, st.session_state.areasObj, areaColorMapping)
    # valuesPerResult = generate_dict_shapes(used_areas, st.session_state.areasObj, areaColorMapping)

    valuesPerHighway = generate_dict_shapes(used_highways, st.session_state.highwaysObj, highwayColorMapping, open=True)
    valuesPerBuilding = generate_dict_shapes(used_buildings, st.session_state.buildingsObj, buildingColorMapping)

    fig = go.Figure()

    for area, values in valuesPerArea.items():
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=values["lon"],
            lat=values["lat"],
            marker={"color": values["color"]},
            name=area,
            line=dict(width=1, color=values["color"]),
            fill="toself",
            hoverinfo="skip"
        ))

    for building, values in valuesPerBuilding.items():
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=values["lon"],
            lat=values["lat"],
            marker={"color": values["color"]},
            name=building,
            line=dict(width=1, color=buildingColorMapping[building]),
            fill="toself",
            hoverinfo="skip"
        ))

    for highway, values in valuesPerHighway.items():
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=values["lon"],
            lat=values["lat"],
            marker={"color": values["color"]},
            name=highway,
            line=dict(width=1, color=values["color"]),
            hoverinfo="skip"
        ))

    if "pipeRender" in st.session_state:
        for pipe, values in st.session_state.pipeRender.items():
            if len(values["lon"]) == 0:
                continue

            fig.add_trace(go.Scattermapbox(
                mode="lines",
                lon=values["lon"],
                lat=values["lat"],
                marker={"color": values["color"]},
                name=pipe,
                line=dict(width=2, color=values["color"]),
                hovertext=[json.dumps(val) for val in values["hover"]],
            ))

    if "supplierRenders" in st.session_state:
        for supplier, values in st.session_state.supplierRenders.items():
            if len(values["lat"]) == 0:
                continue

            fig.add_trace(go.Scattermapbox(
                mode="markers",
                lon=values["lon"],
                lat=values["lat"],
                marker={"color": values["color"]},
                name=supplier,
                hovertext=values["hoverText"],
            ))

    fig.update_layout(
        mapbox=dict(
            style=map_style,
            center=go.layout.mapbox.Center(
                lat=st.session_state.centroid.lat,
                lon=st.session_state.centroid.lon
            ),
            zoom=15
        ),
        height=st.session_state.map_height
    )

    st.plotly_chart(fig, use_container_width=True)


def calculate_polygon_center(coordinates):
    lats = [coord[0] for coord in coordinates]
    lons = [coord[1] for coord in coordinates]
    lat_center = sum(lats) / len(lats)
    lon_center = sum(lons) / len(lons)
    return lat_center, lon_center


def reset_store():
    st.session_state.clear()


def upload_callback():
    reset_store()


def load_solution(file):
    if "result_set" in st.session_state:
        return

    st.session_state.result_set = True
    pattern = re.compile(r"lat<([+-]?[0-9]*[.]?[0-9]+)>lon<([+-]?[0-9]*[.]?[0-9]+)>")
    solution = file
    system_file = "./../data/systems_optional.json"
    with open(system_file, "r") as file:
        systems = json.load(file)

    suppliers_options = systems["supplier"]
    pipe_options = systems["line"]

    buildings = solution["buildings"]
    areas = solution["areas"]
    pipes = solution["line"]

    line_types = set()
    for pipe in pipes:
        line_types.add(pipe["kind"])

    pipeRender = {}

    for line_type in line_types:
        lineCoordinatesLon = []
        lineCoordinatesLat = []
        pipe_option = pipe_options[line_type]
        line_color = pipe_option["color"]
        hover = []
        for pipe in pipes:
            if pipe["kind"] != line_type:
                continue

            for connection in pipe["connections"]:
                val = {
                    "capacity": connection["capacity"],
                    "usage": sum(connection["usage"]),
                    "loss": sum(connection["loss"]),
                    "invest": pipe["totalInvest"],
                    "operating": pipe["operatingCost"],
                    "co2": pipe["totalCo2"]
                }

                from_coord = connection["from"]
                to_coord = connection["to"]
                matched = pattern.match(from_coord)
                lat = float(matched.group(1))
                lon = float(matched.group(2))
                lineCoordinatesLat.append(lat)
                lineCoordinatesLon.append(lon)
                hover.append(val)

                matched = pattern.match(to_coord)
                lat = float(matched.group(1))
                lon = float(matched.group(2))
                lineCoordinatesLat.append(lat)
                lineCoordinatesLon.append(lon)
                hover.append(val)

                lineCoordinatesLat.append(None)
                lineCoordinatesLon.append(None)

            if len(lineCoordinatesLat) == 0:
                continue

            pipeRender[line_type] = {
                "lon": lineCoordinatesLon,
                "lat": lineCoordinatesLat,
                "color": line_color,
                "hover": hover
            }

    original_input = st.session_state.in_file
    buildings = solution["buildings"]
    buildingSupplierRender = {}
    supplierTypes = set()
    orgBuildings = original_input["buildings"]

    supplierRenders = {}
    for idx, supplierType in enumerate(suppliers_options):
        offset_percentage = idx / len(suppliers_options)
        coordinateLat = []
        coordinateLon = []
        hoverText = []
        for buildingId, building in buildings.items():
            suppliers = building["supplier"]
            if supplierType not in suppliers:
                continue

            orgBuilding = orgBuildings[buildingId]
            geometry = orgBuilding["geometry"]
            most_north_east = geometry[0]
            next_coordinate = geometry[1]
            for idx, coordinate in enumerate(geometry):
                if coordinate["lat"] > most_north_east["lat"] and coordinate["lon"] > most_north_east["lon"]:
                    most_north_east = coordinate
                    next_coordinate = geometry[(idx + 1) % len(geometry)]


            lat_a = most_north_east["lat"]
            lon_a = most_north_east["lon"]

            lat_b = next_coordinate["lat"]
            lon_b = next_coordinate["lon"]

            lat_center = (1-offset_percentage) * lat_a + offset_percentage * lat_b
            lon_center = (1-offset_percentage) * lon_a + offset_percentage * lon_b

            coordinateLat.append(lat_center)
            coordinateLon.append(lon_center)
            hoverText.append(supplierType)

        for areaId, area in areas.items():
            suppliers = area["supplier"]
            if supplierType not in suppliers:
                continue

            orgArea = original_input["areas"][areaId]
            geometry = orgArea["geometry"]
            most_north_east = geometry[0]
            next_coordinate = geometry[1]
            for idx, coordinate in enumerate(geometry):
                if coordinate["lat"] > most_north_east["lat"] and coordinate["lon"] > most_north_east["lon"]:
                    most_north_east = coordinate
                    next_coordinate = geometry[(idx + 1) % len(geometry)]

            lat_a = most_north_east["lat"]
            lon_a = most_north_east["lon"]

            lat_b = next_coordinate["lat"]
            lon_b = next_coordinate["lon"]

            lat_center = (1 - offset_percentage) * lat_a + offset_percentage * lat_b
            lon_center = (1 - offset_percentage) * lon_a + offset_percentage * lon_b

            coordinateLat.append(lat_center)
            coordinateLon.append(lon_center)
            hoverText.append(supplierType)

        if len(coordinateLat) == 0:
            continue

        color = suppliers_options[supplierType]["color"]
        supplierRenders[supplierType] = {
            "lat": coordinateLat,
            "lon": coordinateLon,
            "color": color,
            "hoverText": hoverText,
        }

    st.session_state.supplierRenders = supplierRenders
    st.session_state.pipeRender = pipeRender


def main():
    # render in wide mode
    st.set_page_config(layout="wide")

    st.sidebar.header("Store Management")

    reset_store_button = st.sidebar.button("Reset Store")
    if reset_store_button:
        reset_store()

    input_file = st.sidebar.file_uploader("Upload File", on_change=upload_callback)
    default_file_path = "../data/total_Arnis.json"
    default_file = json.load(open(default_file_path, "r"))
    st.session_state.in_file = default_file

    result_file = st.sidebar.file_uploader("Upload Solution")
    if not result_file:
        result_file = "../data/output/arnis_random.json"
        result_file = json.load(open(result_file, "r"))
    if result_file:
        load_solution(result_file)

    result_file_path = "./data/output_example.json"
    result_file = json.load(open(result_file_path, "r"))

    # Define a Store
    if "init" not in st.session_state:
        st.session_state.init = True
        file_to_use = default_file
        if input_file:
            file_to_use = json.load(input_file)
        st.session_state.file = file_to_use
        areaObj = {}
        buildingsObj = {}
        highwaysObj = {}
        for id, obj in file_to_use["areas"].items():
            areaObj[id] = Shapes.deserialize(obj)

        for id, obj in file_to_use["buildings"].items():
            buildingsObj[id] = Shapes.deserialize(obj)

        for id, obj in file_to_use["highways"].items():
            highwaysObj[id] = Shapes.deserialize(obj)

        coordinates_lat = set()
        coordinates_lon = set()

        for id, obj in areaObj.items():
            for coord in obj.geometry:
                coordinates_lat.add(coord.lat)
                coordinates_lon.add(coord.lon)

        for id, obj in buildingsObj.items():
            for coord in obj.geometry:
                coordinates_lat.add(coord.lat)
                coordinates_lon.add(coord.lon)

        centroid = (sum(coordinates_lat) / len(coordinates_lat), sum(coordinates_lon) / len(coordinates_lon))
        centroid = Coordinate(lat=centroid[0], lon=centroid[1])

        areas = set()
        for areaId, area in areaObj.items():
            areas.add(area.type)

        highways = set()
        for highwayId, highway in highwaysObj.items():
            highways.add(highway.type)

        buildings = set()
        for buildingId, building in buildingsObj.items():
            buildings.add(building.type)

        areas = list(areas)
        sorted(areas)
        highways = list(highways)
        sorted(highways)
        buildings = list(buildings)
        sorted(buildings)

        areas_results = {}
        for id, obj in result_file["area"].items():
            areas_results[id] = [supplier for supplier in obj["supplier"].keys()] + [storage for storage in obj["storage"].keys()]

        buildings_results = {}
        for id, obj in result_file["buildings"].items():
            buildings_results[id] = [supplier for supplier in obj["supplier"].keys()] + [storage for storage in obj["storage"].keys()]

        highways_results = {}
        for obj in result_file["line"]:
            for highway in highwaysObj:
                for coordinate in highwaysObj.geometry:
                    if coordinate.lat == obj["geometry"][0]["lat"] and coordinate.lon == obj["geometry"][0]["lon"]:
                        id = highway
                        break
            if id not in highways_results:
                highways_results[id] = []

            highways_results[id].append(obj["kind"])

        areaColorMapping = {}
        for idx, area in enumerate(areas):
            areaColorMapping[area] = f"hsl(138, 100%, 50%)"

        buildingColorMapping = {}
        for idx, building in enumerate(buildings):
            # set a gradient but dont use greens
            buildingColorMapping[building] = f"hsl({((idx * 180 // len(buildings)) + 180) % 360}, 100%, 50%)"

        highwayColorMapping = {}
        for idx, highway in enumerate(highways):
            highwayColorMapping[highway] = f"hsl(0%, 0%, 100%)"

        st.session_state.areasObj = areaObj
        st.session_state.buildingsObj = buildingsObj
        st.session_state.highwaysObj = highwaysObj

        st.session_state.areas_results = areas_results
        st.session_state.buildings_results = buildings_results
        st.session_state.highways_results = highways_results

        st.session_state.centroid = centroid

        st.session_state.areaColorMapping = areaColorMapping
        st.session_state.areas = areas

        st.session_state.buildingColorMapping = buildingColorMapping
        st.session_state.buildings = buildings

        st.session_state.highwayColorMapping = highwayColorMapping
        st.session_state.highways = highways

    st.sidebar.header("Parameters")

    map_height = st.sidebar.slider("Map Height", 0, 2000, 750)
    st.session_state.map_height = map_height

    map_options = ["open-street-map", "carto-positron", "carto-darkmatter", "white-bg"]
    map_style = st.sidebar.selectbox("Map Style", map_options, index=2)

    possible_areas = st.session_state.areas
    used_areas = st.sidebar.multiselect("Areas Uses", possible_areas, default=possible_areas)

    possible_highways = st.session_state.highways
    used_highways = st.sidebar.multiselect("Highways", possible_highways, default=possible_highways)

    possible_buildings = st.session_state.buildings
    used_buildings = st.sidebar.multiselect("Buildings", possible_buildings, default=possible_buildings)

    render_main(map_style, used_areas, used_highways, used_buildings)


if __name__ == "__main__":
    #main()
    road_network = build_road_network()
    _, buildings = create_graph()
    for building in buildings:
        print(building.nearest_road(road_network))
