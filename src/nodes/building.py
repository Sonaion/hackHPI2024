from src.nodes.consumption import Consumption

class Building:
    def __init__(self, id, type, summer_consumption, winter_consumption, points):
        self.id = id
        self.type = type

        self.summer_electricity_consumption = Consumption(summer_consumption['Electro'])
        self.summer_heating_consumption = Consumption(summer_consumption['Heating'])
        self.winter_electricity_consumption = Consumption(winter_consumption['Electro'])
        self.winter_heating_consumption = Consumption(winter_consumption['Heating'])

        self.points = points

        self.is_open = False
