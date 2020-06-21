from ..algorithms import greedy 
from ..classes import district as dt

import random 
import math
import copy


class Annealing(greedy.SwapGreedy):

    def __init__(self, district):
        self.district = district

    def acceptence_prob(self, score_old, score_new, temp):
        """
        Defining the acceptance probability in the simulated annealing
        algorithm.
        """

        probability = math.exp((score_old - score_new) / temp)

        return probability

    def reset_district(self):
        """
        Creating the same district again, which effectively
        resets the district.
        """
        
        # Resetting district properties
        self.district = copy.deepcopy(dt.District(self.district.name))

    def random_solution(self):
        """
        Finding a solution using the greedy battery algorithm (with swap)
        using random weights w1 and w2 for the score function.
        """

        while True:
            
            # Generating random weights
            self.w1 = random.uniform(0,1)
            self.w2 = random.uniform(0,1)
            
            # Running greedy algorithm (with swap)
            result = self.run_battery_swap()

            if result["success"] == True:
                print("SUCCESS!")
                return result
            else:
                print("Nope")
                self.reset_district()

    def run_annealing(self):
        """
        Finding the global minimum (optimum) of the cost by optimalizing with respect to
        weights w1 and w2 of the score function in the greedy battery algorithm 
        (with swap) using simulated annealing.
        """

        # Setting initial solution and temperature
        result = self.random_solution()
        temp = 2000

        for iteration in range(1000):

            # Keeping track of old district configuration
            old_district = self.district
            old_w1 = self.w1
            old_w2 = self.w2
            
            # Little random change
            self.w1 += random.uniform(-0.04, 0.04)
            self.w2 += random.uniform(-0.04, 0.04)

            # Reset district 
            self.reset_district()

            # New solution with new weights 
            new_result = self.run_battery_swap()

            # Checking whether the new result is actually a solution
            if new_result["success"]:

                # Checking if we accept the new solution 
                if random.random() > self.acceptence_prob(score_old=result["total_cost"], score_new=new_result["total_cost"], temp=temp):
                    self.w1 = old_w1
                    self.w2 = old_w2 
                    self.district = old_district
                else:
                    result = new_result
            else:
                self.w1 = old_w1
                self.w2 = old_w2 
                self.district = old_district

            # Decreasing the temperature
            temp -= 1
        return result 




        

            



    

