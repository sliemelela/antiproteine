from ..classes import cable
from ..classes import district as dt
from ..algorithms import randomize

import copy, random


class Greedy(randomize.Random):
    """
    This algorithm connects every house to the battery with the shortest
    manhatten distance to the house that is available. 
    This algorithm does that in two different ways. 
    - One is by putting the houses in a queue to connect 
    - The other is by putting the batteries in a queue
        to fill up with connections to houses that are nearby.
    """

    def __init__(self, district, w1, w2):
        self.district = copy.deepcopy(district)
        self.w1 = w1
        self.w2 = w2 

    def house_score(self, house, battery):
        """ 
        Given a battery, this method assigns a score to a house.
        This score is determined by the manhatten distance and the output of the house.
        The lower the score, the better. 
        """

        # Retrieving coordinates of house and battery
        h_x = house.position[0]
        h_y = house.position[1]
        b_x = battery.position[0]
        b_y = battery.position[1]

        # Calculating manhatten distance
        manhatten_distance = abs(h_x - b_x) + abs(h_y - b_y)

        # Retrieving house max output
        output = house.maxoutput

        # Scoring the house by distance and output
        score = self.w1 * manhatten_distance + self.w2 * output 

        return score 
    
    def find_battery(self, house):
        """
        Given a house, this method searches for the closest available battery 
        with respect to the manhatten distance.
        """

        # Retrieving house position
        h_x = house.position[0]
        h_y = house.position[1]

        # Declaring a list of all possible manhatten distances per battery
        manhatten_distances = {}
        
        # Make list of all batteries that the house can be connected to
        possible_batteries = [battery for battery in self.district.batteries if battery.remainder > house.maxoutput]
        
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

    def find_houses(self, battery):
        """
        Given a battery, this method searches for all the houses that it can connect to.
        The houses are sorted in ascending order with respect to the manhatten distance.
        """

        # Make list of eligible houses (no connections)
        houses = [house for house in self.district.houses if len(house.cables) == 0]
    
        # Sorting house by manhatten distance to the battery
        houses.sort(key=lambda house:self.house_score(house, battery))
        
        return houses  

    def connect_house(self, house, battery, cable):
        """
        This function saves the connection between battery and house with the inputted cable.
        """

        house.add_cable(cable)
        self.district.add_cable(cable)
        battery.add_house(house)

        return None
    
    def run_houses(self, houses):
        """
        This function runs the greedy algorithm with houses (the inputted list of houses) in the queue and returns
        the total price with the list of houses that were not connected.
        """

        # Declaring variables that keep track of whether config is one that satisfies constraints.
        success = False 
        no_connections = []

        # Check for every house if it can be connected to a suitable battery
        for house in houses:
            battery = self.find_battery(house)

            # If battery was found, connect the house to the battery
            if battery != False:
                cable = self.generate_random_cable(house, battery)
                self.connect_house(house, battery, cable)

            # If battery is not found, house has no connection
            else:
                no_connections.append(house)

        # Configuration satisfies the constraints if all houses are connected
        if len(no_connections) == 0:
            success = True

        # Calculate the price after configuration is made 
        self.district.calculate_price()

        return {"no_connections": no_connections, "total_cost": self.district.total_cost, "district": self.district}

    def run_battery(self):
        """
        This function runs the greedy algorithm with batteries in the queue and returns
        the total price with the list of houses that were not connected.
        """

        # Variable to keep track whether configuration satisfies constraints
        success = False 

        # Check what houses can be connected per battery
        for battery in self.district.batteries:

            # Find houses that can possibly be connected to battery
            houses = self.find_houses(battery)
            no_connections = []

            # First add the shorter distance houses until not possible anymore
            if len(houses) > 0:
                while houses[0].maxoutput < battery.remainder:
                    house = houses[0]
                    cable = self.generate_random_cable(house, battery)
                    self.connect_house(house, battery, cable)
                    houses.pop(0)
                    if len(houses) == 0:
                        break 
            
                # Add the farther houses in the list if possible
                for house in houses:
                    if house.maxoutput < battery.remainder and len(house.cables) == 0:
                        cable = self.generate_random_cable(house, battery)
                        self.connect_house(house, battery, cable)
                    else:
                        no_connections.append(house)

            # Configuration satisfies the constraints if all houses are connected
            if len(no_connections) == 0:
                success = True

        # Calculate the price after configuration is made
        self.district.calculate_price()

        return {"success": success, "no_connections": no_connections, "total_cost": self.district.total_cost, "district": self.district}

class SwapGreedy(Greedy):
    """
    This algorithm runs the greedy algorithm and tries swapping afterward if
    the result was of the greedy algorithm was not successfull. Even after swapping,
    the result can still be unsuccessfull.
    """
    
    def order_batteries(self):
        """
        This function sorts the list of batteries from biggest to smallest remainder.
        """

        batteries = [battery for battery in self.district.batteries]
        batteries.sort(key=lambda x:x.remainder, reverse=True)

        return batteries

    def remove_connection(self, house, battery):
        """
        This function removes the connection between inputted battery and house.
        """

        self.district.delete_cable(house.cables[0])
        house.delete_cable()
        battery.delete_house(house)

        return None

    def swap_houses(self, battery):
        """
        This functions tries to move the houses connected to the given battery to other batteries 
        (with lowest remainder battery as priority) if possible.
        """

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
                self.connect_house(house, battery_choice, new_cable)
    
        return None
    
    def run_houses_swap_choice(self, choice):
        """
        This function runs the greedy algorithm with houses in the queue and tries swapping 
        (if the result was not successfull) afterward.
        """

        houses = self.district.houses

        # Sorting the houses by their choice (by output or random)
        if choice == "random":
            random.shuffle(houses)
        elif choice == "sort":
            houses.sort(key=lambda x:x.maxoutput, reverse=True)

        # Run the greedy algorithm with houses in the queue
        result = self.run_houses(houses)

        # If all houses are connected, swapping is not needed
        if len(result["no_connections"]) == 0:

            # Calculate the price after configuration is made 
            self.district.calculate_price()

            # We already have succes and give the result
            return {"success": True, "swap": False, "district": self.district}
        
        # Sort the batteries from biggest to smallest remainder
        batteries = self.order_batteries()

        # Start swapping per battery
        for battery in batteries:

            # Try swapping by emptying the inputted battery
            self.swap_houses(battery)

            # Try connecting the houses again that were not connected yet
            new_result = self.run_houses(result["no_connections"])

            # If swapping worked, stop and return the result
            if len(new_result["no_connections"]) == 0:

                # Calculate the price after configuration is made 
                self.district.calculate_price()

                # We have succes and give the result
                return {"success": True, "swap": True, "district": self.district}
        
        # Calculate the price after configuration is made 
        self.district.calculate_price()

        # If swapping did not help for all batteries, we have no success
        return {"success": False, "swap": True, "district": self.district}

    def run_houses_swap(self):
        """
        This function repeats the houses swap procedure (run_houses_swap_choice),
        where the queue of houses is determined randomly, until a solution is found.
        """

        success = False
        while success == False:
            result = self.run_houses_swap_choice("random")
            success = result["success"]

            # If there is no success, we reset the district and try again.
            if success == False:
                self.reset_district()
        
        return result

    def run_battery_swap(self):
        """
        This function runs the greedy algorithm with batteries in the queue and tries swapping 
        (if the result was not successfull) afterward.
        """

        # Run the greedy algorithm with batteries in the queue
        result = self.run_battery()
        
        # If all houses are connected, swapping is not needed
        if len(result["no_connections"]) == 0 :

            # Calculate the price after configuration is made 
            self.district.calculate_price()

            # We have succes and give the result
            return {"success": True, "swap": False, "district": self.district}

        # Sort the batteries from biggest to smallest remainder
        batteries = self.order_batteries()

        # Start swapping per battery
        for battery in batteries:

            # Try swapping by emptying the inputted battery
            self.swap_houses(battery)
            
            # Try connecting the houses again that were not connected yet
            new_result = self.run_houses(result["no_connections"])

            # If swapping worked, stop and return the result
            if len(new_result["no_connections"]) == 0:

                # Calculate the price after configuration is made
                self.district.calculate_price()

                # We have succes and give the result
                return {"success": True, "swap": True, "district": self.district}
        
        # Calculate the price after configuration is made
        self.district.calculate_price()

        # If swapping for all batteries did not work, we have no succes
        return {"success": False, "swap": True, "district": self.district}
            
        





