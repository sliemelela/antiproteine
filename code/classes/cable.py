class Cable():
    def __init__(self):
        self.positions = []
        self.lines = set()
        self.total_cost = 0
    
    def add_position(self, position):
        """
        List of coordinates of where the cable is going to run through.
        """

        self.positions.append(position)
    
    def add_lines(self):
        """
        Set of line segments (which is a set of two coordinates) of the cable.
        """
        
        amount = len(self.positions)
        for i in range(amount - 1):
            self.lines.add(frozenset({self.positions[i], self.positions[i+1]}))

