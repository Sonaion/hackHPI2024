package main

import (
	"encoding/json"
	"math"
	"os"
)

type Input struct {
	Highways  HighwayMap  `json:"highways"`
	Buildings BuildingMap `json:"buildings"`
	Areas     AreaMap     `json:"areas"`
}

type Output struct {
	Graph     []OutputNode     `json:"graph"`
	Buildings []OutputBuilding `json:"buildings"`
	Areas     []OutputArea     `json:"areas"`
	Roads     []OutputRoad     `json:"roads"`
}

type OutputNode struct {
	ID       int            `json:"id"`
	Children []NodeDistance `json:"children"`
}

type NodeDistance struct {
	Node     int
	Distance float64
}

type BuildingMap map[string]Building

type Building struct {
	ID       string  `json:"id"`
	Type     string  `json:"type"`
	Geometry []Point `json:"geometry"`
	Open     bool    `json:"open"`
	BaseArea float64 `json:"base_area"`
	Levels   float64 `json:"levels"`
	Area     float64 `json:"area"`
}

type AreaMap map[string]Area
type Area struct {
	ID       string  `json:"id"`
	Type     string  `json:"type"`
	Geometry []Point `json:"geometry"`
	Open     bool    `json:"open"`
	BaseArea float64 `json:"base_area"`
}

type OutputRoad struct {
	ID    int   `json:"id"`
	Point Point `json:"point"`
}

type OutputBuilding struct {
	ID       int     `json:"id"`
	Point    Point   `json:"center"`
	Type     string  `json:"type"`
	BaseArea float64 `json:"base_area"`
	Area     float64 `json:"area"`
}

type OutputArea struct {
	ID       int     `json:"id"`
	Point    Point   `json:"center"`
	BaseArea float64 `json:"base_area"`
	Area     float64 `json:"area"`
}

type HighwayMap map[string]Highway

type Highway struct {
	ID       string  `json:"id"`
	Type     string  `json:"type"`
	Geometry []Point `json:"geometry"`
}

type Point struct {
	Lat float64 `json:"lat"`
	Lon float64 `json:"lon"`
}

// The distance function remains the same.
func distance(p1 Point, p2 Point) float64 {
	xDist := p1.Lat - p2.Lat
	yDist := p1.Lon - p2.Lon
	return math.Sqrt(xDist*xDist+yDist*yDist) * 111249.23412498034
}

func centralPoint(points []Point) Point {
	var avgLat, avgLon float64
	for _, point := range points {
		avgLat += point.Lat
		avgLon += point.Lon
	}

	avgLat /= float64(len(points))
	avgLon /= float64(len(points))

	return Point{Lat: avgLat, Lon: avgLon}
}

func nearestRoad(p Point, roads []OutputRoad) (OutputRoad, float64) {
	var nearest OutputRoad
	nearestDistance := math.Inf(1)

	for _, road := range roads {
		dist := distance(p, road.Point)
		if dist < nearestDistance {
			nearestDistance = dist
			nearest = road
		}
	}

	return nearest, nearestDistance
}

type RoadNetwork map[Point][]PointDistance

type PointDistance struct {
	Point    Point
	Distance float64
}

type HighDensityResidential struct {
	ID       string  `json:"id"`
	Geometry []Point `json:"geometry"`
}

type Residential struct {
	ID       string  `json:"id"`
	Geometry []Point `json:"geometry"`
}

func main() {
	inputFile := "input.json"
	// Read file as input.
	file, err := os.ReadFile(inputFile)
	if err != nil {
		panic("Could not open file")
	}

	var input Input
	err = json.Unmarshal(file, &input)
	if err != nil {
		panic("Could not parse input")
	}

	outputBuildings := []OutputBuilding{}
	outputAreas := []OutputArea{}
	outputRoads := []OutputRoad{}

	for _, building := range input.Buildings {
		central := centralPoint(building.Geometry)

		outputBuildings = append(outputBuildings, OutputBuilding{
			ID:       len(outputBuildings),
			Point:    central,
			Type:     building.Type,
			BaseArea: building.BaseArea,
			Area:     building.Area,
		})
	}

	for _, area := range input.Areas {
		central := centralPoint(area.Geometry)

		outputAreas = append(outputAreas, OutputArea{
			ID:       len(outputBuildings) + len(outputAreas),
			Point:    central,
			BaseArea: area.BaseArea,
		})
	}

	for _, road := range input.Highways {
		for _, point := range road.Geometry {
			outputRoads = append(outputRoads, OutputRoad{
				ID:    len(outputBuildings) + len(outputAreas) + len(outputRoads),
				Point: point,
			})
		}
	}

	outputNodes := []OutputNode{}

	for _, building := range outputBuildings {
		outputNodes = append(outputNodes, OutputNode{
			ID:       building.ID,
			Children: []NodeDistance{},
		})
	}

	for _, area := range outputAreas {
		outputNodes = append(outputNodes, OutputNode{
			ID:       area.ID,
			Children: []NodeDistance{},
		})
	}

	for _, road := range outputRoads {
		outputNodes = append(outputNodes, OutputNode{
			ID:       road.ID,
			Children: []NodeDistance{},
		})
	}

	highways := []Highway{}
	for _, highway := range input.Highways {
		highways = append(highways, highway)
	}

	totalVisited := 0
	for _, highway := range highways {
		var prev Point
		for j, p := range highway.Geometry {
			index := len(outputBuildings) + len(outputAreas) + totalVisited + j
			if j > 0 {
				dist := distance(prev, p)
				outputNodes[index-1].Children = append(outputNodes[index-1].Children, NodeDistance{Node: index, Distance: dist})
				outputNodes[index].Children = append(outputNodes[index].Children, NodeDistance{Node: index - 1, Distance: dist})
			}

			prev = p
		}

		totalVisited += len(highway.Geometry)
	}

	roadPoints := []Point{}
	for _, road := range outputRoads {
		roadPoints = append(roadPoints, road.Point)
	}

	for i, building := range outputBuildings {
		nearest, dist := nearestRoad(building.Point, outputRoads)
		outputNodes[i].Children = append(outputNodes[i].Children, NodeDistance{Node: nearest.ID, Distance: dist})
		outputNodes[nearest.ID].Children = append(outputNodes[nearest.ID].Children, NodeDistance{Node: i, Distance: dist})
	}

	for i, area := range outputAreas {
		nearest, dist := nearestRoad(area.Point, outputRoads)
		outputNodes[len(outputBuildings)+i].Children = append(outputNodes[len(outputBuildings)+i].Children, NodeDistance{Node: nearest.ID, Distance: dist})
		outputNodes[nearest.ID].Children = append(outputNodes[nearest.ID].Children, NodeDistance{Node: len(outputBuildings) + i, Distance: dist})
	}

	output := Output{
		Graph:     outputNodes,
		Buildings: outputBuildings,
		Areas:     outputAreas,
		Roads:     outputRoads,
	}

	// save output to json
	outputFile := "output.json"
	outputJson, err := json.Marshal(output)
	if err != nil {
		panic("Could not marshal output")
	}

	err = os.WriteFile(outputFile, outputJson, 0644)
	if err != nil {
		panic("Could not write output")
	}
}
