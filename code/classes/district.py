from code.classes import house, battery
import csv

class District():
    def __init__(self, name):
        self.name = name
        self.houses = self.load_houses(f"data/{name}/{name}_houses.csv")
        self.batteries = self.load_batteries(f"data/{name}/{name}_batteries.csv")
        self.cables = []

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
        self.cables.append(cable)

    def delete_cable(self, cable):
        self.cables.remove(cable)

