import copy, random
from ..classes import cable


class GreedyHouse():
    """
    This algorithm connects every house to the battery with the shortest
    manhatten distance to the house that is available.
    """

    def __init__(self, district):
        self.district = copy.deepcopy(district)

    def find_battery(self, house):
        h_x = house.position[0]
        h_y = house.position[1]
        manhatten_distances = {}
        
        # Make list of all batteries that the house can be connected to
        possible_batteries = []
        for battery in self.district.batteries:
            if battery.remainder > house.maxoutput:
                possible_batteries.append(battery)
        
        # If there are batteries available, search for the closest one to the house
        if len(possible_batteries) > 0:
            for battery in possible_batteries:
                b_x = battery.position[0]
                b_y = battery.position[1]
                manhatten_distance = abs(h_x - b_x) + abs(h_y - b_y)
                manhatten_distances[battery] = manhatten_distance
            
            closest_battery = min(manhatten_distances.keys(), key=lambda k: manhatten_distances[k])
            return closest_battery
        
        # If there were no batteries available return False
        return False

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
    
    def run(self, houses):
        no_connection = []
        for house in houses:
            battery = self.find_battery(house)
            if battery != False:
                cable = self.generate_random_cable(house, battery)
                self.connect_house(house, battery, cable)
            else:
                no_connection.append(house)
        return [no_connection, self.district.total_cost]

class SwapGreedyHouse(GreedyHouse):
    def __init__(self, district):
        self.district = district
    
    def find_battery_to_empty(self):

        # Find battery with most remainder left
        battery_biggest_remainder = self.district.batteries[0]
        for battery in self.district.batteries:
            if battery.remainder > battery_biggest_remainder.remainder:
                battery_biggest_remainder = battery
        
        return battery_biggest_remainder
    
    def order_batteries(self):
        batteries = []
        for battery in self.district.batteries:
            batteries.append(battery)
        batteries.sort(key=lambda x:x.remainder, reverse=True)
        return batteries

    def remove_connection(self, house, battery):
        self.district.delete_cable(house.cables[0])
        house.delete_cable()
        battery.delete_house(house)
        return True
        
    def make_connection(self, house, battery, cable):
        house.add_cable(cable)
        self.district.add_cable(cable)
        battery.add_house(house)
        return True

    def swap_houses(self, battery):

        for house in battery.connected:

            # List of available batteries to choose from, other than the one the house is currently connected to
            new_battery_choices = []
            for battery_option in self.district.batteries:

                # Add battery to list if it is available 
                if (battery_option != battery) and house.maxoutput < battery_option.remainder:
                    new_battery_choices.append(battery_option)
            
            if len(new_battery_choices) > 0:

                # Choosing battery with least remainder
                battery_choice = min(new_battery_choices, key=lambda x:x.remainder)

                # Remove old connection.
                self.remove_connection(house, battery)

                # Generate new cable
                new_cable = self.generate_random_cable(house, battery_choice)
                
                # Make new connection for house.
                self.make_connection(house, battery_choice, new_cable)
    
        return True
    
    def run_swap(self):
        houses = self.district.houses
        #houses.sort(key=lambda x:x.maxoutput, reverse=True)
        #random.shuffle(houses)
        result = self.run(houses)

        if len(result[0]) > 0 :
            batteries = self.order_batteries()
            for battery in batteries:
                self.swap_houses(battery)
                new_result = self.run(result[0])
                if len(new_result[0]) == 0:
                    return [True, "AFTER SWAP"]
            return [False, "WITH SWAP"] 
        else:
            return [True, "WITHOUT SWAP", f"Price: {result[1]}"]
        




