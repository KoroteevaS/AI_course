import utility as utility
import loader as loader
import numpy as np
from math import ceil


def main():

    # Paths to the data and solution files.
    vrp_file = "data/n32-k5.vrp"  # "data/n80-k10.vrp"
    sol_file = "data/n32-k5.sol"  # "data/n80-k10.sol"
    # vrp_file = "data/n80-k10.vrp"  # "data/n80-k10.vrp"
    # sol_file = "data/n80-k10.sol"
    # Loading the VRP data file.
    px, py, demand, capacity, depot = loader.load_data(vrp_file)

    # Displaying to console the distance and visualizing the optimal VRP solution.
    vrp_best_sol = loader.load_solution(sol_file)
    my_distance = []
    for el in vrp_best_sol:
        my_distance.append([0]+el.tolist()+[0])
    best_distance = utility.calculate_total_distance(my_distance, px, py, depot)
   


    print("Best VRP Distance:", best_distance)

    utility.visualise_solution(vrp_best_sol, px, py, depot, "Optimal Solution")

    # Executing and visualizing the nearest neighbour VRP heuristic.
    # Uncomment it to do your assignment!

    nnh_solution = nearest_neighbour_heuristic(px, py, demand, capacity, depot)
    print(nnh_solution)

    nnh_distance = utility.calculate_total_distance(nnh_solution, px, py, depot)

    print("Nearest Neighbour VRP Heuristic Distance:", nnh_distance)

    utility.visualise_solution(nnh_solution, px, py, depot, "Nearest Neighbour Heuristic")
    utility.save_solution("nnh", nnh_solution, nnh_distance)

    
    sh_solution = savings_heuristic(px, py, demand, capacity, depot)
    print(sh_solution)
    sh_distance = utility.calculate_total_distance(sh_solution, px, py, depot)
    print("Saving VRP Heuristic Distance:", sh_distance)
    utility.visualise_solution(sh_solution, px, py, depot, "Savings Heuristic")
    utility.save_solution("sh", sh_solution, sh_distance)


def get_minimum(distance_array, visited_nodes):
    my_min = 0
    index = None

    for i, row in enumerate(distance_array):
        if i == visited_nodes[-1]:
            for ind, el in enumerate(row):
                if ind not in visited_nodes and el:
                    if my_min!=0:

                        if el < my_min:
                                my_min = float(el)
                                index = int(ind)
                    else:
                        my_min=float(el)
                        index = int(ind)
    return my_min, index


def nearest_neighbour_heuristic(px, py, demand, capacity,depot):
    try:
        routes  = [[0]]
        my_demands = [0]
        visited_nodes = [0]
        demand_list = demand.tolist()
        distance_array = nonearraymaker(len(demand_list), len(demand_list))
        for i,row in enumerate(distance_array):
            for ind, val in enumerate(row):
                if i != ind:# and ind!=0 and i!=0:
                    distance_array[i][ind] = utility.calculate_euclidean_distance(px, py,i, ind)
        my_index = ceil(sum(demand_list)/capacity)
        for i in range(len(distance_array)+my_index):
            my_min, index = get_minimum(distance_array, visited_nodes)
            if routes[-1] == [0] or my_demands[-1]+demand_list[index] <= capacity:
                routes[-1].append(index)
                visited_nodes.append(index)
                my_demands[-1]+=demand_list[index]
            else:
                routes[-1].append(0)
                routes.append([0])
                visited_nodes.append(0)
                my_demands.append(0)
    except TypeError:
            routes[-1].append(0)

    print("Summary")
    #print(sorted(visited_nodes))
    print(my_demands)
    return routes


def nonelistmaker(n):
    listofones = [None]*n
    return listofones

def nonearraymaker(n, m):
    my_array = []
    for i in range(m):
        my_array.append(nonelistmaker(n))
    return my_array

def onelistmaker(n):
    listofones = [1]*n
    return listofones

def onearraymaker(n, m):
    my_array = []
    for i in range(m):
        my_array.append(onelistmaker(n))
    return my_array

def zerolistmaker(n):
    listofzeros = [0]*n
    return listofzeros
#[[18, 28, 4, 11, 8, 9, 22, 15], [23, 2, 3, 17, 19, 31, 21], [29, 10, 25]]
def zeroarraymaker(n , m):
    my_array = []
    for ind in range(m):
        my_array.append(zerolistmaker(n))
    return my_array

def find_maximum(savings_array,visited_nodes, routes, ind1 = None, ind2 = None):

    max_save=0
    for i,row in enumerate(savings_array):
        if i==0:
            pass
        elif routes[-1]==[] and i in visited_nodes:
            pass
        else:
            if (ind1 and i == ind1) or (ind2 and i==ind2) or (not ind1==0 and not ind2==0):
                if visited_nodes ==[]:
                    visited_nodes = [0]
                if routes[-1] == [] or (routes[-1]!=[] and (routes[-1][-1]==i or routes[-1][0]==i)):
                    for ind, val in enumerate(row):
                        if not val or val ==0:
                            pass
                        if ind not in visited_nodes:# or visited_nodes[-1]==0:
                            if val:# and ind!=0:
                                if val> max_save:
                                    #print(ind)
                                    max_save = float(val)
                                    index1= int(i)
                                    index2 = int(ind)
    return index1, index2, max_save

def savings_heuristic(px, py, demand, capacity, depot):

    """
    Algorithm for Implementing the savings heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each nodes demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """
    routes  = [[]]
    my_demands = [0]
    demand_list = demand.tolist()
    visited_nodes = []
    savings_array = nonearraymaker(len(demand_list), len(demand_list))
    #print(savings_array)
    for i,row in enumerate(savings_array):
        for ind, val in enumerate(row):
            if i != ind:# and ind!=0 and i!=0:
                savings_array[i][ind] = utility.calculate_euclidean_distance(px, py,i, 0) + utility.calculate_euclidean_distance(px, py,0,ind) - utility.calculate_euclidean_distance(px, py, i, ind)

    savings_array_initial = list(savings_array)
    my_index = ceil(sum(demand_list)/capacity)
    for el in range(len(demand_list)+my_index):
        try:
            try:
                ind1, ind2, max_save = find_maximum(savings_array,visited_nodes, routes, routes[-1][0], routes[-1][-1])

            except:

                ind1, ind2, max_save = find_maximum(savings_array,visited_nodes,routes)

            if routes[-1] ==  []:

                    visited_nodes.append(ind1)
                    routes[-1].append(ind1)
                    my_demands[-1]+=demand_list[ind1]
                    visited_nodes.append(ind2)
                    routes[-1].append(ind2)
                    my_demands[-1]+=demand_list[ind2]
                    savings_array[ind1][ind2] = 0
                    savings_array[ind2][ind1] = 0



            elif my_demands[-1]+demand_list[ind2] <= capacity:

                    if ind1 == routes[-1][-1]:

                            routes[-1].append(ind2)
                    elif ind1==routes[-1][0]:
                            routes[-1]= [ind2]+routes[-1]
                    my_demands[-1] += demand_list[ind2]
                    visited_nodes.append(ind2)
                    savings_array[ind1][ind2]=0
                    savings_array[ind2][ind1]=0
            else:
                routes.append([])
                my_demands.append(0)


        except Exception as e:

            new_routes = []
            print("Summary")
            print(my_demands)
            #print(sorted(visited_nodes))
            for el in routes:
                new_route = [0] + el +[0]
                new_routes.append(new_route)
            return new_routes

if __name__ == '__main__':
    main()
