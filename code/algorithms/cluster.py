from ..algorithms import annealing
from ..classes import district as dt

class Cluster(annealing.Annealing):
    """
    Algorithm that repositions the batteries based on the existing clusters in a
    given solution (k-means). The batteries are repositioned to the mean of the houses connected
    to that battery in question.
    This algorithm stops repositioning after the difference in price becomes (relatively) small.
    The initial solution and new configurations of cables are made with the Greedy House Swap algorithm. 
    """

    def reposition_batteries(self, solution):
        """
        Given some configuration of a district (solution), we calculate the mean position
        of the houses per battery. We reposition the battery to that location. 
        After this we run the Greedy House algorithm to find a configuration with the new location.
        """

        # Calculate the mean position of the houses (cluster) per battery
        new_battery_positions = []
        for battery in solution["district"].batteries:
            sum_x = 0
            sum_y = 0
            for house in battery.connected:
                sum_x += house.position[0]
                sum_y += house.position[1]
            mean_x = sum_x / len(battery.connected)
            mean_y = sum_y / len(battery.connected)
            new_battery_positions.append((int(mean_x), int(mean_y))) 
        
        # Repeat procedure until new solution has lower total cost
        iterations = 0
        while True:

            # Make new district with the new battery positions (means of houses in old district)
            self.reset_district()
            index_counter = 0
            for battery in self.district.batteries:
                battery.position = new_battery_positions[index_counter]
                index_counter += 1
            
            # Make a new configuration from the repositioned battery district
            new_solution = self.run_houses_swap()
            if new_solution["district"].total_cost <= solution["district"].total_cost:
                break

            # Stop if the amount of iterations is too high
            iterations += 1
            if iterations >= 100:
                new_solution = solution
                break

        return new_solution
    
    def run_cluster(self):
        """
        Repeat the repositioning of batteries until the difference in price of the solution converges.
        This is done by imposing a threshold (called epsilon) for which if the difference is smaller, we 
        consider the last configuration as "converged".
        """
        # Make initial solution
        init_solution = self.run_houses_swap()

        # Declaring variables that keep track of difference of costs, iteration and a difference threshold (epsilon)
        iterations = 0
        difference = 1
        epsilon = 0.5

        # Keep on repositioning batteries until difference between old and new cost is small
        old_result = self.reposition_batteries(init_solution)
        while difference > epsilon:

            # Get new result from repositioning batteries
            new_result = self.reposition_batteries(old_result)
            
            # Calculate difference in price
            difference = old_result["district"].total_cost - new_result["district"].total_cost
            print("Difference:", difference)

            # Reset old result
            old_result = new_result
            print("Price:", new_result["district"].total_cost)

            # Counting number of iterations
            iterations += 1
            print("Iteration:", iterations)

        return new_result

