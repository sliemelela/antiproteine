class Battery():

    def __init__(self, position, capacity):
        self.position = position
        self.capacity = float(capacity)
        self.price = 5000
        self.connected = []
        self.remainder = float(capacity)
    
    def add_house(self, house):
        self.connected.append(house)
        self.remainder -= house.maxoutput

    def delete_house(self, house):
        self.connected.remove(house)
        self.remainder += house.maxoutput