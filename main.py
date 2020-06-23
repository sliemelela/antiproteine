from __future__ import print_function, unicode_literals
from code.classes import district as dt
from code.algorithms import randomize, random_swap, random_greedy_swap, greedy, annealing, random
from code.visualisation import visualise as vis


from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
from pyfiglet import Figlet
from prettytable import PrettyTable



if __name__ == "__main__":

    # Intro Banner
    f = Figlet(font='slant')
    print(f.renderText('Smart Grid'))

    # Style of the questions
    style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
    })


    district_type = [
        {
            'type': 'list',
            'message': 'What district do you want to run the algorithm on?',
            'name': 'district',
            'choices': [
                {
                    'name': 'District 1'
                },
                {
                    'name': 'District 2'
                },
                {
                    'name': 'District 3'
                }
            ],
        }
    ]

    algo_type = [
        {
            'type': 'list',
            'message': 'What kind of algorithm do you want to run?',
            'name': 'algorithm',
            'choices': [
                {
                    'name': 'Random'
                },
                {
                    'name': 'Greedy'
                },
                {
                    'name': 'Clustering (k-means)'
                }
            ],
        }
    ]

    greedy_type = [
        {
            'type': 'list',
            'message': 'What kind of greedy algorithm do you want to run?',
            'name': 'algorithm',
            'choices': [
                {
                    'name': 'Greedy House'
                },
                {
                    'name': 'Greedy Battery'
                },
            ],
        }
    ]

    swap_type = [
        {
            'type': 'confirm',
            'message': 'Do you want to include the swapping procedure or not?',
            'name': 'swap',
            'default': True,
        }
    ]

    annealing_type = [
        {
            'type': 'confirm',
            'message': 'Do you want to do the simulated annealing algorithm?',
            'name': 'annealing',
            'default': True,
        }
    ]

    x = PrettyTable()

    # Retrieving the desired district
    district_answers = prompt(district_type, style=style)

    # Generating district object
    data_folder = district_answers["district"].replace(' ', '-')
    district = dt.District(data_folder)

    algo_answers = prompt(algo_type, style=style)

    # Random algoritms 
    if algo_answers["algorithm"] == "Random":
        swap_answers = prompt(swap_type, style=style)

        # With Swap
        if swap_answers["swap"]:
            raise "Not implemented"
        else:
            random = random.Random(district)
            result = random.run_random(district.houses)

    # Greedy algorithms
    elif algo_answers["algorithm"] == "Greedy":
        greedy_answers = prompt(greedy_type, style=style)

        # Greedy Battery
        if greedy_answers["algorithm"] == "Greedy Battery":
            annealing_answers = prompt(annealing_type, style=style)

            # Simulated Annealing 
            if annealing_answers["annealing"]:
                sim = annealing.Annealing(district)
                result = sim.run_annealing()

            # No simulated annealing
            else:
                swap_answers = prompt(swap_type, style=style)

                # With Swap
                if swap_answers["swap"]:
                    greedy_swap = greedy.SwapGreedy(district, 1, 0)
                    result = greedy_swap.run_battery_swap()
                else:
                    greedy = greedy.Greedy(district, 1, 0)
                    result = greedy.run_battery()

        # Greedy House
        else:
            greedy_swap = greedy.SwapGreedy(district, 1, 0)
            result = greedy_swap.run_houses_swap()

    # Clustering algorithms
    # TODO

    # Table overview of results
    x.add_column("District", [result["district"].name])
    x.add_column("Success", [result["success"]])
    x.add_column("Total Cost", [result["district"].total_cost])

    print(x)

    #########################################################################
    # # Retrieving district information
    # data_folder = "district-2"

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

    # Visualisation
    vis.visualise(result["district"])
