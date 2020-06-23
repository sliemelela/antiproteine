from code.classes import house, battery

import csv


class District():
    def __init__(self, name):
        self.name = name
        self.houses = self.load_houses(f"data/{name}/{name}_houses.csv")
        self.batteries = self.load_batteries(f"data/{name}/{name}_batteries.csv")
        self.cables = []
        self.total_cost = 0
        self.discounted_cost = 0

    def load_houses(self, source_file):
        """
        Load all the houses.
        """
        with open(source_file, 'r') as in_file:
            reader = csv.DictReader(in_file)
            
            houses = []    
            for row in reader:
                position = (int(row['x']), int(row['y']))
                maxoutput= row['maxoutput']
                houses.append(house.House(position=position, maxoutput=maxoutput))
            
        return houses
    
    def load_batteries(self, source_file):
        """
        Load all the batteries.
        """
        with open(source_file, 'r') as in_file:
            reader = csv.DictReader(in_file)

            batteries = []
            for row in reader:
                position = tuple(map(int, row['positie'].split(',')))
                capacity = row['capaciteit']
                batteries.append(battery.Battery(position=position, capacity=capacity))
            
        return batteries
    
    def add_cable(self, cable):
        """
        This function adds a cable to the district.
        """

        self.cables.append(cable)
        self.total_cost += cable.total_cost

    def delete_cable(self, cable):
        """
        This cable removes a cable from the district
        """

        self.cables.remove(cable)

    def calculate_price(self):
        """
        This function calculates the total cost.
        """

        # Keep track of amount of cables line segments 
        amount_cable_lines = 0

        # Keep track of actual cable lines, but delete duplicates (shared cable implementation) 
        shared_cables = set()
        
        # Add line segment to cable and update the information about cables
        for cable in self.cables:
            cable.add_lines()
            shared_cables.update(cable.lines)
            amount_cable_lines += len(cable.lines)
        
        # Calculate total cost and discounted cost
        self.total_cost = 5 * 5000 +  9 * amount_cable_lines 
        self.discounted_cost = 5 * 5000 + 9 * len(shared_cables)
