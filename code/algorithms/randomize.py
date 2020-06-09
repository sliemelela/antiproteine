from code.classes import district, cable
import random, copy

# Pick a house (we are going to loop through every house)
# We pick a battery RANDOMLY for that house that satisfies constraints
    # If it does not satisfy: go next house
# Generate RANDOM path for cable.

def generate_random_cable(house_position, battery_position):

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
        
        current_location = random.choice(new_location_choices)
        new_cable.add_position(current_location)

    return new_cable

def random_connect_battery(district, house):

    # Loading district and batteries
    battery_choices = copy.deepcopy(district.batteries)

    # Checking which batteries can be connected
    for battery_choice in battery_choices: 
        if battery_choice.remainder < house.maxoutput:
            battery_choices.remove(battery_choice)

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
        district.add_cable(cable)

        return True

    else:
        return False



