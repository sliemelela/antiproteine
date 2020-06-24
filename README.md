# Smart Grid (by Antiproteine)

Green energy is the energy of the future, and producing it yourself is today's fashion. Presently, many houses have solar pannels or windmills, or other installations that produce their own energy. Fortunately, these installations often produce more energy than is actually needed for a user's own consumption. The surplus could be sold back to the supplier, but the infrastructure (the grid) is often not designed for this. Batteries must be installed to manage the peaks in consumption and production. 

The challenge is to find a configuration of cables and batteries that is the cheapest, since cables (between houses and batteries) and batteries cost money. There are also some constraints we need to look out for:

- The maximum output of the houses counted up may not exceed the battery capacity
- Batteries should not be connected to each other, also not through a house. 
- A house should not be connected to more than one battery.
- Cables can be positioned over the same grid segment. If cables are positioned over the same grid segment, then the price can be discounted. For all intents and purposes, we can pretend there is only one cable on that particular grid segment with respect to the total cost.
- Each house needs to have a unique cable that is connected to a battery.

The following cases are treated:
1. Given the location of 150 houses and the location of 5 batteries, find the optimal configuration (with respect to the total cost) of cables that satisfies the above constraints. 
2. Given the location of 150 houses and 5 batteries, find the optimal configuration of the placement of the batteries and the cables. 
3. Given the location of 150 houses, find the best configuration of the placement and amount (and type) of batteries, and the placement of the cables. 

## Start up 
### Requirements
This codebase is written entirely in Python 3.7. The file requirements.txt contains all necessary packages to run the code successfully. These are easy to install via pip using the following instruction:
```bash
    pip install -r requirements.txt
```
Or using conda:
```bash
    conda install --file requirements.txt
```

### In Action
By calling
```bash
    python main.py
```
you are provided with a command line interface. The instructions are straight forward.

### Structure
The following list describes the most important maps and file in the project, and where you can find them:

- **/code**: contains all the code used for this project
    - **/code/algorithms**: contains the code for the algorithms
    - **/code/classes**: contains the code used for the classes (e.g. that are used in the algorithms)
    - **/code/visualisation**: contains the code for visualising the configurations. 
- **/data**: contains the various datafiles that for example specify the location of the houses and the batteries that are then used in the code.

## Pseudo Code: The three cases
### Case 1: Location/amount of both the houses and batteries known

#### The Random Algorithms 

##### Random Algorithm
This algorithm will randomly connect houses to batteries using cables satisfying the constraints described above. 
Also the generated cable between the house and the battery is generated randomly, but it does satisfy the extra constraint that the length of the cable is the same as the manhatten distance between the house and battery.
```
for house in list of houses:
    - find a random battery (that satisfies the constraints)
    - generate random cable 
```
Problem: Finding a solution that satisfies the constraints is not necessarily found. 
Solution: Repeat algorithm until solution is found.

Possible optimization: Given a configuration that does not satisfy the constraints, we want to find reshuffle (swap cables) it to find a configuration that does or is closer to it. 

##### Random Swap Algorithm
This algorithm is an optimization of the random algorithm. 

```
- First do random algorithm
- Look for the battery with the highest remainder left.
for house in (list of houses that is connected to that battery):
    - look for another battery that it can be connected to 
    - randomly choose a battery from that list of possible batteries
    - reconfigure the configuration
```

Possible optimization: Instead of choosing a random battery, choose the battery with the lowest remainder (to leave more space for other houses).

#### The Greedy Algorithms 

##### Greedy House Algorithm
This algorithm goes through a randomly sorted list of houses and tries to connect to the closest available battery. 
The pseudo code is very straight forward.
```
randomly shuffle list of houses
for house in houses:
    - look for closest battery to connect to 
    - connect if there is an available
```
If solution is not found, the swapping procedure is run (as described in Random Swap algorithm). 
The pseudo code for that is the exact same as the random swap algorithm except that 
```
    randomly choose a battery from that list of possible batteries
```
becomes
```
    choose the battery from the list with the smallest remainder
```
such that swap becomes "greedy".

What is important to note, is that the order of the houses greatly influences whether a solution will be found or not. 
So the code repeats until a solution is found.


##### Greedy Battery Algorithm
This algorithm goes through the list of batteries (in the order that is provided by the dataset) and tries to connect houses to each battery. 
The most straightforward way is to use the manhatten distance heuristic; first connect all the houses that are closest to the given battery.
Another factor that is important to realise, is that if we would use the maxoutput of a house as a heuristic, that we would maybe a find a solution faster, but the price would not maybe not be the best.


###### Heuristic: manhatten distance
In this case the pseudo code is straight forward.
```
for battery in batteries:
    - make a list of houses sorted by manhattan distance in ascending order
    - connect to houses until it is not possible anymore
```
Note, that since we begin with the same order of batteries every time, this final configuration will always be the same for every run for every district.
From here you can do the swapping algorithm if desired, in the same manner as in the greedy house algorithm.

###### Simulated Annealing
In this case, we want to combine the following heuristic given a battery:
```python
    house_score = w1 * manhatten_distance + w2 * house_maxoutput
```
for a given w1 and w2. Note that the final configuration using this new heuristic is going to give the exact same configuration for very run for every district. The question now becomes, which combination of w1 and w2 gives us the global minimum. 
Unconventionally, we use simulated annealing on this landscape of w1, w2 as x,y coordinates and the total cost of a district as the z coordinate.

### Case 2: Location/amount of houses known; amount of batteries known

#### The Clustering Algorithm (k-means)
Using some initial solution, we want to reposition the batteries in a better location. 
The location that is most straight forward is by taking the mean position of all the houses per battery, and making that the new location.
From here you try to find a new solution and repeat the process again. The process is stopped when the difference is price is smaller then some threshold. We chose to generate this initial solution and new solution with the most promising algorithm: the greedy house algorithm.
Note that other algorithms could have been chosen, but due to the lack of time, this is not implemented yet.

The pseudo code is then as follows:
```
- create initial solution with greedy house algorithm
- reposition the batteries to the means of their collection of connected houses
- if new location is on a house, change the location slightly, until this is not the case
- if new price is worse than old price, repeat above procedure
- repeat above procedure until difference in total cost of the new and old solution per iteration is smaller than some threshold (epsilon)
```

## Authors
- Sliem el Ela
- Sara Morcy
- Anastasija Markovic
