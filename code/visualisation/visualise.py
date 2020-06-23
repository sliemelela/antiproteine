from matplotlib import pyplot as plt


def visualise(district):
    """ 
    Visualisation code that represents the configuration of 
    houses, cables and batteries.
    """

    # Retrieving house, battery and cable objects
    houses = district.houses
    batteries = district.batteries
    cables = district.cables

    # Creating dict of battery (key) and houses (value)
    relationship = {}
    for battery in batteries:
        relationship[battery] = battery.connected

    # Plotting data
    batteries_enum = enumerate(batteries) 
    colors = ['b', 'g', 'r', 'c', 'm']
    for counter, battery in batteries_enum:

        # Plotting houses and cables
        for house in battery.connected:
            cable_positions = [cable.positions for cable in house.cables]
            cable_positions_x = [cable_position[0] for cable_position in cable_positions[0]]
            cable_positions_y = [cable_position[1] for cable_position in cable_positions[0]]
            plt.plot(cable_positions_x, cable_positions_y, color=colors[counter-1], zorder=-1)
            plt.scatter(house.position[0], house.position[1], c=colors[counter - 1], s=10, marker="s")
        
        # Plotting batteries
        plt.scatter(battery.position[0], battery.position[1], c=colors[counter - 1], s=50, marker="D", label=f'Battery {counter}')

    # Put a legend to the right of the current axis
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

    return None
    

