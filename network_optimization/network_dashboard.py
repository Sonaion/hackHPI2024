import json

import plotly.graph_objects as go
import streamlit as st

from objects import Shapes, Coordinate


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



    fig.update_layout(
        mapbox=dict(
            style=map_style,
            center=go.layout.mapbox.Center(
                lat=st.session_state.centroid.lat,
                lon=st.session_state.centroid.lon
            ),
            zoom=10
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


def main():
    # render in wide mode
    st.set_page_config(layout="wide")

    st.sidebar.header("Store Management")

    reset_store_button = st.sidebar.button("Reset Store")
    if reset_store_button:
        reset_store()

    input_file = st.sidebar.file_uploader("Upload File", on_change=upload_callback)
    default_file_path = "./total_Freyburg (Unstrut).json"
    default_file = json.load(open(default_file_path, "r"))

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

        areaColorMapping = {}
        for idx, area in enumerate(areas):
            areaColorMapping[area] = f"hsl(138, 100%, 50%)"

        buildingColorMapping = {}
        for idx, building in enumerate(buildings):
            # set a gradient but dont use greens
            buildingColorMapping[building] = f"hsl({((idx * 180 // len(buildings))+180) % 360}, 100%, 50%)"

        highwayColorMapping = {}
        for idx, highway in enumerate(highways):
            highwayColorMapping[highway] = f"hsl(0%, 0%, 100%)"

        st.session_state.areasObj = areaObj
        st.session_state.buildingsObj = buildingsObj
        st.session_state.highwaysObj = highwaysObj

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
    main()
