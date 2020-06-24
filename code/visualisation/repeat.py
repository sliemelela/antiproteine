import numpy as np
from matplotlib import pyplot as plt

def repeat_graph(result_costs, result_shared):

    # Calculate mean of the costs
    result_costs_mean = [np.mean(result_costs)]*len(result_costs)
    result_shared_mean = [np.mean(result_shared)]*len(result_shared)

    # Plot the results 
    plt.plot(result_costs)
    plt.plot(result_shared)
    
    # Plot the average line
    mean_line_costs = plt.plot(result_costs_mean, "--")
    mean_line_shared = plt.plot(result_shared_mean, "--")

    # Make a legend
    plt.legend(["Total Costs", "Shared Costs", "Mean Total Costs", "Mean Shared Costs"])

    # Specify labels for axes
    plt.xlabel("Iterations")
    plt.ylabel("Cost")

    # Show plot
    plt.show()

    return None