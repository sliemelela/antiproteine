from code.classes import cable
from code.classes import district as dt

import random, copy


class Random:
    def __init__(self, district):
        self.district = district
    
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
            
            # Choosing a new position 
            current_location = random.choice(new_location_choices)

            # Add chosen position to the list of positions of cable
            new_cable.add_position(current_location)

        return new_cable  

    def random_connect(self, house):
        """
        Given a house this function randomly connects the house to a random 
        (available) battery.
        """

        # Loading district and batteries
        battery_options = []
        for battery_option in self.district.batteries:
            battery_options.append(battery_option)

        # Checking which batteries can be connected
        battery_choices = []
        for battery_choice in battery_options:
            if battery_choice.remainder > house.maxoutput:
                battery_choices.append(battery_choice)
        
        # Checking if connections are possible
        if len(battery_choices) == 0:
            return False

        # Choosing random battery from available batteries   
        chosen_battery = random.choice(battery_choices)
        chosen_battery.add_house(house)

        # Generating a random cable
        cable = self.generate_random_cable(house, chosen_battery)
        
        # Storing connection
        house.add_cable(cable)
        self.district.add_cable(cable)

        return True

    def run_random(self, houses):
        """
        This function connects all the given houses to a random (available) battery.
        """

        # Kepping track of the houses for which are no batteries available
        no_connections = []

        # Coonnect every house from the given houses to a random available battery
        for house in houses:
            connected = self.random_connect(house)
            if connected == False:
                no_connections.append(house)
        
        # If some houses have no connection from the given houses, we have no success
        if len(no_connections) > 0:
            success = False

        # If all houses have a connection from the given houses, we have success
        else:
            success = True

        # Calculate the price after configuration is made 
        self.district.calculate_price()

        return {"success": success, "no_connections": no_connections, "total_cost": self.district.total_cost, "district": self.district}
    
    def connect_limited_batteries(self, battery, house):
        """
        Connect house to random (available) battery other than the battery that is given.
        """

        # Loading district and batteries
        battery_options = []
        for battery_option in self.district.batteries:
            if battery_option != battery:
                battery_options.append(battery_option)

        # Checking which batteries can be connected
        battery_choices = []
        for battery_choice in battery_options:
            if battery_choice.remainder > house.maxoutput:
                battery_choices.append(battery_choice)

        # Checking if connections are possible
        if len(battery_choices) == 0: 
            return False
        
        # Choosing random battery from available batteries   
        chosen_battery = random.choice(battery_choices)
        chosen_battery.add_house(house)

        # Generating a random cable
        cable = self.generate_random_cable(house, chosen_battery)
        
        # Store connection.
        self.district.add_cable(cable)
        house.add_cable(cable)

        return None          

    def swap_connections(self, battery):
        """
        Swapping houses from inputted battery to random other battery.
        """

        new_battery_choices = []
        for battery_option in self.district.batteries:
            if battery_option != battery:
                new_battery_choices.append(battery_option)

        for house in battery.connected:
            for battery_choice in new_battery_choices:

                # Check if house can connect to another battery.
                if house.maxoutput < battery_choice.remainder:

                    # Remove old connection.
                    self.district.delete_cable(house.cables[0])
                    house.delete_cable()
                    battery.delete_house(house)

                    # Make new random connection for house.
                    self.connect_limited_batteries(battery, house)

                    break

        return None

    def run_random_swap(self):
        """
        This function first randomly tries to connect all houses from the ddistrict to a battery.
        If there is no success, swapping starts. Houses from a battery get moved to another battery of possible.
        After swapping, we try connecting the leftover houses randomly to available batteries.
        If swapping for all batteries did not work, we have no success.
        """
        
        # Randomly connect all houses in district
        result = self.run_random(self.district.houses)

        # If all houses are connected we stop and return the result
        if result["success"]:
            result["swap"] = False

            # Calculate the price after configuration is made 
            self.district.calculate_price()
            return result

        # We try swapping per battery and try connecting afterwards again
        for battery in self.district.batteries:

            # Try swapping by trying to empty the inputted battery
            self.swap_connections(battery)

            # Try connecting again after swapping
            new_result = self.run_random(result["no_connections"])

            # If all houses are connected we stop and return the result
            if new_result["success"]:
                new_result["swap"] = True

                # Calculate the price after configuration is made 
                self.district.calculate_price()
                return new_result
            
            # If not all houses are connected yet, we try swapping with the new_result
            result = new_result
        
        # If not all houses are connected after swapping at every battery, we have no success
        new_result["swap"] = True 

        # Calculate the price after configuration is made 
        self.district.calculate_price()

        return new_result
    
    def reset_district(self):
        """
        Creating the same district again, which effectively
        resets the district.
        """
        
        # Resetting district properties
        self.district = dt.District(self.district.name)

        return None

    def run(self):
        """
        This function runs the random swap algorithm until a solution is 
        """

        while True:
            result = self.run_random_swap()
            if result["success"]:
                return result
            else:
                self.reset_district()


    
