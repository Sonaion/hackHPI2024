package main

import (
	"encoding/json"
	"math"
	"os"
	"sort"
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
	ID                string      `json:"id"`
	Type              string      `json:"type"`
	Geometry          []Point     `json:"geometry"`
	Open              bool        `json:"open"`
	BaseArea          float64     `json:"base_area"`
	Levels            float64     `json:"levels"`
	Area              float64     `json:"area"`
	WinterConsumption Consumption `json:"winter"`
	SummerConsumption Consumption `json:"summer"`
}

type Consumption struct {
	Electro []float64 `json:"Electro"`
	Heating []float64 `json:"Heating"`
}

type CalcedConsumption struct {
	MinElectro  float64     `json:"min_electro"`
	MaxElectro  float64     `json:"max_electro"`
	AvgElectro  float64     `json:"avg_electro"`
	MinHeating  float64     `json:"min_heating"`
	MaxHeating  float64     `json:"max_heating"`
	AvgHeating  float64     `json:"avg_heating"`
	Consumption Consumption `json:"consumption"`
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
	ID                int               `json:"id"`
	Point             Point             `json:"center"`
	Type              string            `json:"type"`
	BaseArea          float64           `json:"base_area"`
	Area              float64           `json:"area"`
	WinterConsumption CalcedConsumption `json:"winter_consumption"`
	SummerConsumption CalcedConsumption `json:"summer_consumption"`
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

func median(data []float64) float64 {
	dataCopy := make([]float64, len(data))
	copy(dataCopy, data)
	sort.Float64s(dataCopy)
	var median float64
	l := len(dataCopy)
	if l == 0 {
		return 0
	} else if l%2 == 0 {
		median = (dataCopy[l/2-1] + dataCopy[l/2]) / 2
	} else {
		median = dataCopy[l/2]
	}
	return median
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

	buildingLats := []float64{}
	buildingLons := []float64{}
	for _, building := range input.Buildings {
		central := centralPoint(building.Geometry)
		buildingLats = append(buildingLats, central.Lat)
		buildingLons = append(buildingLons, central.Lon)
	}

	// Calculate the median of the building lats and lons
	buildingMedianLat := median(buildingLats)
	buildingMedianLon := median(buildingLons)

	filteredBuildings := BuildingMap{}

	for key, building := range input.Buildings {
		central := centralPoint(building.Geometry)
		if math.Abs(central.Lat-buildingMedianLat) > 1 || math.Abs(central.Lon-buildingMedianLon) > 1 {
			continue
		}

		minElectroSummer := math.Inf(1)
		maxElectroSummer := 0.0
		avgElectroSummer := 0.0

		minHeatingSummer := math.Inf(1)
		maxHeatingSummer := 0.0
		avgHeatingSummer := 0.0

		for _, consumption := range building.SummerConsumption.Electro {
			if consumption < minElectroSummer {
				minElectroSummer = consumption
			}
			if consumption > maxElectroSummer {
				maxElectroSummer = consumption
			}
			avgElectroSummer += consumption
		}

		if avgElectroSummer != 0 {
			avgElectroSummer /= float64(len(building.SummerConsumption.Electro))
		}

		for _, consumption := range building.SummerConsumption.Heating {
			if consumption < minHeatingSummer {
				minHeatingSummer = consumption
			}
			if consumption > maxHeatingSummer {
				maxHeatingSummer = consumption
			}
			avgHeatingSummer += consumption
		}

		if avgHeatingSummer != 0 {
			avgHeatingSummer /= float64(len(building.SummerConsumption.Heating))
		}

		minElectroWinter := math.Inf(1)
		maxElectroWinter := 0.0
		avgElectroWinter := 0.0

		minHeatingWinter := math.Inf(1)
		maxHeatingWinter := 0.0
		avgHeatingWinter := 0.0

		for _, consumption := range building.WinterConsumption.Electro {
			if consumption < minElectroWinter {
				minElectroWinter = consumption
			}
			if consumption > maxElectroWinter {
				maxElectroWinter = consumption
			}
			avgElectroWinter += consumption
		}

		if avgElectroWinter != 0 {
			avgElectroWinter /= float64(len(building.WinterConsumption.Electro))
		}

		for _, consumption := range building.WinterConsumption.Heating {
			if consumption < minHeatingWinter {
				minHeatingWinter = consumption
			}
			if consumption > maxHeatingWinter {
				maxHeatingWinter = consumption
			}
			avgHeatingWinter += consumption
		}

		if avgHeatingWinter != 0 {
			avgHeatingWinter /= float64(len(building.WinterConsumption.Heating))
		}

		if minElectroSummer == math.Inf(1) {
			minElectroSummer = 0
		}

		if minHeatingSummer == math.Inf(1) {
			minHeatingSummer = 0
		}

		if minElectroWinter == math.Inf(1) {
			minElectroWinter = 0
		}

		if minHeatingWinter == math.Inf(1) {
			minHeatingWinter = 0
		}

		filteredBuildings[key] = building
		outputBuildings = append(outputBuildings, OutputBuilding{
			ID:       len(outputBuildings),
			Point:    central,
			Type:     building.Type,
			BaseArea: building.BaseArea,
			Area:     building.Area,
			WinterConsumption: CalcedConsumption{
				MinElectro:  minElectroWinter,
				MaxElectro:  maxElectroWinter,
				AvgElectro:  avgElectroWinter,
				MinHeating:  minHeatingWinter,
				MaxHeating:  maxHeatingWinter,
				AvgHeating:  avgHeatingWinter,
				Consumption: building.WinterConsumption,
			},
			SummerConsumption: CalcedConsumption{
				MinElectro:  minElectroSummer,
				MaxElectro:  maxElectroSummer,
				AvgElectro:  avgElectroSummer,
				MinHeating:  minHeatingSummer,
				MaxHeating:  maxHeatingSummer,
				AvgHeating:  avgHeatingSummer,
				Consumption: building.SummerConsumption,
			},
		})
	}

	input.Buildings = filteredBuildings

	areaLats := []float64{}
	areaLons := []float64{}

	for _, area := range input.Areas {
		central := centralPoint(area.Geometry)
		areaLats = append(areaLats, central.Lat)
		areaLons = append(areaLons, central.Lon)
	}

	// Calculate the median of the area lats and lons
	areaMedianLat := median(areaLats)
	areaMedianLon := median(areaLons)

	filteredAreas := AreaMap{}

	for _, area := range input.Areas {
		central := centralPoint(area.Geometry)
		if math.Abs(central.Lat-areaMedianLat) > 1 || math.Abs(central.Lon-areaMedianLon) > 1 {
			continue
		}

		outputAreas = append(outputAreas, OutputArea{
			ID:       len(outputBuildings) + len(outputAreas),
			Point:    central,
			BaseArea: area.BaseArea,
		})
	}

	input.Areas = filteredAreas

	roadLats := []float64{}
	roadLons := []float64{}

	for _, road := range input.Highways {
		central := centralPoint(road.Geometry)
		roadLats = append(roadLats, central.Lat)
		roadLons = append(roadLons, central.Lon)
	}

	// Calculate the median of the road lats and lons
	roadMedianLat := median(roadLats)
	roadMedianLon := median(roadLons)

	filteredRoads := HighwayMap{}

	for _, road := range input.Highways {
		if len(road.Geometry) > 0 {
			central := centralPoint(road.Geometry)
			if math.Abs(central.Lat-roadMedianLat) > 1 || math.Abs(central.Lon-roadMedianLon) > 1 {
				continue
			}

			filteredRoads[road.ID] = road

			for _, point := range road.Geometry {
				outputRoads = append(outputRoads, OutputRoad{
					ID:    len(outputBuildings) + len(outputAreas) + len(outputRoads),
					Point: point,
				})
			}
		}
	}

	input.Highways = filteredRoads

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
