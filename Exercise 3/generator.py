from numba import jit
import numpy as np
from collections import deque
#Fiks en linje
def levelup(start_point, end_point):
    #No change in x directions means it goes upwards or downwards
    if end_point[0] == start_point[0]:
        new_s = (end_point[1]-start_point[1])/4
        return  start_point, (start_point[0], start_point[1] + new_s), (start_point[0] - new_s, start_point[1] + new_s), (start_point[0] - new_s, start_point[1] + 2*new_s), (start_point[0], start_point[1] + 2*new_s), (start_point[0] + new_s, start_point[1] + 2*new_s), (start_point[0] + new_s, start_point[1] + 3*new_s), (start_point[0], start_point[1] + 3*new_s)
    #No change in y direction, line goes in x-direction
    if end_point[1] == start_point[1]:
        new_s = (end_point[0]-start_point[0])/4
        return start_point, (start_point[0] + new_s, start_point[1]), (start_point[0] + new_s, start_point[1] + new_s), (start_point[0] + 2*new_s, start_point[1] + new_s), (start_point[0] + 2*new_s, start_point[1]), (start_point[0] + 2*new_s, start_point[1] - new_s), (start_point[0] + 3*new_s, start_point[1] - new_s), (start_point[0] + 3*new_s, start_point[1])
    
#Kjører alt på boksen
def boks(level, L):
    box = [(0,0), (L,0), (L,L), (0,L)]
    for l in range(level):
        new_box = []
        box_len = len(box)
        for i in range(box_len):
            new_box += [point for point in levelup(box[i], box[(i + 1)%box_len])]
            #new_box.append(levelup(box[i], box[(i + 1)%box_len]))
        box = new_box
        box.append(box[0]) #For å tegne siste delen av boksen
    return box


#Funksjon som tar inn en box med tupler, lager en matrise og markerer alle hjørnene i fraktalen med 1, 
# alt inni som 0, og alt utenfor som 2. Returnerer matrisen av størrelse
def make_lattice(fractal:list, level: int, L):
    """
    -----Part 1-----

    Makes a lattice using a fractal consisting of tuple values, marking x and y positions of the fractal corners.
    Lattice is a 2D matrix, consisting of 1s at the fractal borders and 0s elsewhere
    Level and L are variables used for creating the fractal.

    -----Part 2-----

    BFS technique to map all the points inside the fractal lattice. Changes each lattice point value inside the
    fractal from 0 to 2.
    
    Returns
    -------
    2D np.array with 1s marking the fractal borders, 2s marking inside the fractal, and 0s marking outside of the fractal

    """
    #Points in one direction, n_x=n_y
    n_x = 4**level
    #lattice_constant, spacing between each point
    delta = L/n_x  
    #To assure that none of the points will be on the outside of the lattice, 1/3*n_x points is added to each side
    lattice = np.zeros((2*n_x, 2*n_x))
    for x, y in fractal:
        #Each fractal point gets a value of 1 in the lattice. X and Y is multiplied with n_x to assure integers
        lattice[n_x//2 + int(y*n_x)][n_x//2 + int(x*n_x)] = 1
    


    #Run through and decide if the points are within the fractal
    visited = [] # List for visited nodes.
    queue = []  #Initialize a queue

    starting_node = (n_x, n_x)
    print("starting node: ", starting_node)
    visited.append(starting_node) #Starting fairly inside the fractal
    queue.append(starting_node)

    neighbour_nodes = [(1,0), (-1,0), (0,1), (0,-1)]

    while queue:          # Creating loop to visit each node
        m = queue.pop(0) 
        #print (m, end = " ")
        lattice[m[1]][m[0]] = 2 #Setting the value inside of the fractal to 2 
        #neighbours = [(m[1],m[0] + 1), lattice[m[1] + 1][m[0]], lattice[m[1]][m[0] - 1], lattice[m[1] - 1][m[0]]]
        for n_n in neighbour_nodes:
            neighbour = (m[0] + n_n[0],m[1] + n_n[1])
            if neighbour not in visited and lattice[neighbour[1]][neighbour[0]] == 0:
                visited.append(neighbour)
                queue.append(neighbour)
                lattice[neighbour[1]][neighbour[0]] = 1
        # for neighbour in neighbours:
        #     #Evt bruke et set
        #     if neighbour not in visited and lattice[neighbour[]]:
        #         visited.append(neighbour)
        #         queue.append(neighbour)

    return lattice

