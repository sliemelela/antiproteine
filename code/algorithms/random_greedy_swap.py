from code.classes import district, cable
import random, copy

# Random Algorithm 
def generate_random_cable(house_position, battery_position):
    """ 
    Given a house and battery, this function generates a list of coordinates (in Z^3) that is supposed 
    to represent the cable between the house and the battery. This function also satisfies the constraint
    that the length of the cable is the manhatten distance.
    """

    # Keeping track of current location
    current_location = house_position
    new_cable = cable.Cable()
    new_cable.add_position(current_location)

    # Defining coordinates for chosen battery
    a = battery_position[0]
    b = battery_position[1]

    # Generating random manhatten walk from house to battery 
    while current_location != battery_position:

        # Defining coordinates for current location
        x = current_location[0]
        y = current_location[1]

        # Possible new directions (such that manhatten distance is satisfied)
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

def random_connect_battery(district, house):
    """
    Given a district, this function randomly connects a given house to a random 
    (available) battery.
    """
    # Loading district and batteries
    battery_options = []
    for battery_option in district.batteries:
        battery_options.append(battery_option)

    # Checking which batteries can be connected
    battery_choices = []
    for battery_choice in battery_options:
        if battery_choice.remainder > house.maxoutput:
            battery_choices.append(battery_choice)

    # Checking if connections are possible
    if len(battery_choices) > 0: 

        # Choosing random battery from available batteries   
        chosen_battery = random.choice(battery_choices)
        chosen_battery.add_house(house)

        # Retrieving exact location of house and battery
        house_position = house.position
        battery_position = chosen_battery.position

        # Generating a random cable
        cable = generate_random_cable(house_position, battery_position)
        
        # Storing connection
        house.add_cable(cable)
        district.add_cable(cable)

        return True

    else:
        return False

# Swapping algorithm 
def connect_limited_batteries(district, chosen_battery, house):
    """
    Connect house to random battery with certain battery removed from choices.
    """

    # Choosing random battery from available batteries   
    chosen_battery.add_house(house)

    # Retrieving exact location of house and battery
    house_position = house.position
    battery_position = chosen_battery.position

    # Generating a random cable
    cable = generate_random_cable(house_position, battery_position)
    
    # Store connection.
    district.add_cable(cable)
    house.add_cable(cable)

    return True

def swap_connections(district, battery):
    """
    Swapping houses from inputted battery to random other battery.
    """
    
    for house in battery.connected:

        # List of available batteries to choose from
        new_battery_choices = []
        for battery_option in district.batteries:

            # Choose a battery that is different from the one the house is now connected to 
            if (battery_option != battery) and house.maxoutput < battery_option.remainder:
                new_battery_choices.append(battery_option)
        
        if len(new_battery_choices) > 0:

            # Choosing battery with least remainder
            battery_choice = min(new_battery_choices, key=lambda x:x.remainder)

            # Remove old connection.
            district.delete_cable(house.cables[0])
            house.delete_cable()
            battery.delete_house(house)

            # Make new random connection for house.
            connect_limited_batteries(district, battery_choice, house)
    
    return True

def swap_connects(district):
    """
    Swapping houses from battery with biggest remainder
    """

    # Find battery with most remainder left
    battery_biggest_remainder = district.batteries[0]
    for battery in district.batteries:
        if battery.remainder > battery_biggest_remainder.remainder:
            battery_biggest_remainder = battery
    
    # Increasing remainder of battery with biggest remainder
    swap_connections(district, battery_biggest_remainder)
    
    return True


