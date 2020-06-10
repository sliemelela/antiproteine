from code.classes import district
from code.algorithms import randomize, random_swap


if __name__ == "__main__":

    # Retrieving district information
    data_folder = "district-1"
    district = district.District(data_folder)

    # Generate random configuration in state space
    no_connections = []
    for house in district.houses:
        if random_swap.random_connect_battery(district, house) is False:
            no_connections.append(house)

    # Check amount of cables
    print(len(district.cables))

    # Swapping houses from biggest remainder battery to other random batteries
    random_swap.swap_connects(district)

    # Checking if swapping was done correctly
    for battery in district.batteries:
        print("connected: ", len(battery.connected))
        print("remainder: ", battery.remainder)
    print(len(district.cables))

    # Attempt connecting houses again (that were not conected)
    for house in no_connections:
        print(house.maxoutput)
        random_swap.random_connect_battery(district, house)
    print(len(no_connections))
    

    ##CONCLUSION: Just swapping from biggest remainder to another random battery does not help!
    ## Need to choose to which battery we should swap! (next optimization step)
