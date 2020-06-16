class Swap():
    def __init__(self, district):
        self.district = district
    
    def find_battery_to_empty(self):

        # Find battery with most remainder left
        battery_biggest_remainder = self.district.batteries[0]
        for battery in self.district.batteries:
            if battery.remainder > battery_biggest_remainder.remainder:
                battery_biggest_remainder = battery
        
        return battery_biggest_remainder

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
        for battery_option in district.batteries:

            # Choose a battery that is different from the one the house is now connected to 
            if (battery_option != battery) and house.maxoutput < battery_option.remainder:
                new_battery_choices.append(battery_option)
        
        if len(new_battery_choices) > 0:

            # Choosing battery with least remainder
            battery_choice = min(new_battery_choices, key=lambda x:x.remainder)

            # Remove old connection.
            self.district.delete_cable(house.cables[0])
            house.delete_cable()
            battery.delete_house(house)

            # Make new random connection for house.
            connect_limited_batteries(district, battery_choice, house)
    
    return True
    
