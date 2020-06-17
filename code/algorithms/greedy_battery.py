import copy, random
from ..classes import cable

class GreedyBattery():
    """
    This algorithm fills up every battery by connecting the houses with the shortest
    manhatten distance to the battery that is available.
    """
    def __init__(self, district):
        self.district = copy.deepcopy(district)
    
    def find_houses(self, battery):

        # Get battery coordinates
        b_x = battery.position[0]
        b_y = battery.position[1]

        # Make list of eligible houses (no connections)
        houses = [house for house in self.district.houses if len(house.cables) == 0]

        # Sorting house by manhatten distance to the battery
        houses.sort(key=lambda house:abs(house.position[0] - b_x) + abs(house.position[1] - b_y))
        
        return houses
    
    def generate_random_cable(self, house, battery):
        """ 
        Given a house and battery, this function generates a list of coordinates (in Z^2) that is supposed 
        to represent the cable between the house and the battery. This function also satisfies the constraint
        that the length of the cable is the manhatten distance.
        """

        # Keeping track of current location
        current_location = house.position
        new_cable = cable.Cable()
        new_cable.add_position(current_location)

        # Defining coordinates for chosen battery
        a = battery.position[0]
        b = battery.position[1]

        # Generating random manhatten walk from house to battery 
        while current_location != battery.position:

            # Defining coordinates for current location
            x = current_location[0]
            y = current_location[1]

            # Possible new directions
            if x > a and y > b:
                new_location_choices = [(x - 1, y), (x, y - 1)]
            if x > a and y < b:
                new_location_choices = [(x - 1, y), (x, y + 1)]
            if x > a and y == b:
                new_location_choices = [(x - 1, y)]
            if x < a and y > b:
                new_location_choices = [(x + 1, y), (x, y - 1)]
            if x < a and y < b:
                new_location_choices = [(x + 1, y), (x, y + 1)]
            if x < a and y == b:
                new_location_choices = [(x + 1, y)]
            if x == a and y > b:
                new_location_choices = [(x, y - 1)]
            if x == a and y < b:
                new_location_choices = [(x, y + 1)]
            
            current_location = random.choice(new_location_choices)
            new_cable.add_position(current_location)

        return new_cable  

    def connect_house(self, house, battery, cable):
        house.add_cable(cable)
        self.district.add_cable(cable)
        battery.add_house(house)
        return True
    
    def run(self):
        for battery in self.district.batteries:
            houses = self.find_houses(battery)
            while houses[0].maxoutput < battery.remainder:
                house = houses[0]
                print(house)
                cable = self.generate_random_cable(house, battery)
                self.connect_house(house, battery, cable)
                houses.pop(0)
            print(battery.connected)
        if len(houses) > 0:
            return [False]
        else:
            return [True, f"Price: {self.district.total_cost}"]
