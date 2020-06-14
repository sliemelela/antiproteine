# Smart Grid (by Antiproteine)

Green energy is the energy of the future, and producing it yourself is todays fasion. Presently, a lot of houses have solar pannel or windmill, or other installations that produce their own energy. 
Fortunately, often we have that those installations produce more energy than is actually needed for a user their own consumption. The surplus could be sold back to the supplier, but the infrastructure (the grid) is often not designed for this. 
Batteries must be installed to manage the peaks in consumption and production. 

The challenge is to find a configuration of cables and batteries that is the cheapest, since cables (between houses and batteries) and batteries cost money. There are also some constraints we need to look out for:
- The maximum output of the houses counted up may not exceed the battery capacity
- Batteries should not be connected to each other, also not through a house. 
- A house should not be connected to more than one batteries.
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
An example can be run by calling:
```bash
    python main.py
```

The file provides an example for the use of the various functions used in this project.

### Structure
De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- /code: contains all the code used for this project
    - /code/algorithms: contains the code for the algorithms
    - /code/classes: contains the code used for the classes (e.g. that are used in the algorithms)
    - /code/visualisation: contains the code for visualising the configurations. 
- /data: contains the various datafiles that for example specify the location of the houses and the batteries that are then used in the code.

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
for houses in (list of houses that is connected to that battery):
    - look for another battery that it can be connected to 
    - randomly choose a battery from that list of possible batteries
    - reconfigure the configuration
```

Possible optimization: Instead of choosing a random battery, choose the battery with the lowest remainder (to leave more space for other houses).
##### Random Greedy Swap Algorithm 

This algorithm is an optimization of the random swap algorithm. 

```
- First do random algorithm
- Look for the battery with the highest remainder left.
for houses in (list of houses that is connected to that battery):
    - look for another battery that it can be connected to 
    - choose the battery with the lowest remainder from that list of possible batteries
    - reconfigure the configuration
```

### Case 2: Location/amount of houses known; amount of batteries known

### Case 3: Location/amount of houses known
s
## Authors
- Sliem el Ela
- Sara Morcy
- Anastasija Markovic