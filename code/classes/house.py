class House():
    def __init__(self, position, maxoutput):
        self.position = position
        self.maxoutput = float(maxoutput)
        self.cables = []
    
    def add_cable(self, cable):
        self.cables.append(cable)
    
    def delete_cable(self):
        self.cables.clear()

