from code.classes import district as dt
from code.algorithms import randomize, random_swap, random_greedy_swap, greedy


if __name__ == "__main__":

    # Retrieving district information
    data_folder = "district-1"

    # Generating district object
    district = dt.District(data_folder)

    # Starting greedy algorithm
    while True:
        greedy_swap = greedy.SwapGreedy(district)
        result = greedy_swap.run_swap()
        print(result)
        if result[0] == True:
            print("SUCCES")
            break


    #########################################################################
    # # Retrieving district information
    # data_folder = "district-3"

    # # Trying random algorithm until solution is found
    # satisfactory = False
    # while satisfactory == False:

    #     # Generating district object
    #     district = dt.District(data_folder)

    #     # Generate random configuration in state space
    #     no_connections = []
    #     for house in district.houses:
    #         if random_greedy_swap.random_connect_battery(district, house) is False:
    #             no_connections.append(house)

    #     # Checking if swapping was done correctly
    #     print("NO SWAP")
    #     for battery in district.batteries:
    #         print("connected: ", len(battery.connected))
    #         print("remainder: ", battery.remainder)

    #     # Check amount of cables
    #     print("Amount of cables", len(district.cables))

    #     # Swapping houses from biggest remainder battery to other random batteries
    #     random_greedy_swap.swap_connects(district)

    #     # Attempt connecting houses again (that were not conected)
    #     for house in no_connections:
    #         random_greedy_swap.random_connect_battery(district, house)

    #     # Checking if swapping was done correctly
    #     print("AFTER SWAP")
    #     for battery in district.batteries:
    #         print("connected: ", len(battery.connected))
    #         print("remainder: ", battery.remainder)
    #     print("Amount of cables", len(district.cables))
    #     print("Total Cost", district.total_cost)

    #     if len(district.cables) == 150:
    #         satisfactory = True
