from code.classes import district
from code.algorithms import randomize


if __name__ == "__main__":

    # Retrieving district information
    data_folder = "district-1"
    district = district.District(data_folder)

    # Generate random configuration in state space
    for house in district.houses:
        print(randomize.random_connect_battery(district, house))

    # Checking cable positions
    for cable in district.cables:
        print("CABLE BEGINS HERE")
        print(cable.positions)
        print("CABLE ENDS HERE")

    # Check amount of cables 
    print(len(district.cables))