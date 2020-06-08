class Cable():
    def __init__(self):
        self.positions = []
        self.total_cost = 0
    
    def add_position(self, position):
        self.positions.append(position)
        self.total_cost += 9
