import utility as utility
import loader as loader
import numpy as np
from math import ceil


def nonelistmaker(n):
    listofones = [None]*n
    return listofones

def nonearraymaker(n, m):
    my_array = []
    for i in range(m):
        my_array.append(nonelistmaker(n))
    return my_array


def calculate_total_demand(my_list, demand_list):
    total_demand = 0
    for el  in my_list:
        total_demand+=demand_list[el]
    return(total_demand)

def merge_routes(routes, index1, index2, demand_list, capacity):

    for i,route in enumerate(routes):
        for idx, node in enumerate( route):
            if index1 == node:
                route_i1 = i
                route_ind1 =idx
            if index2 == node:
                route_i2 = i
                route_ind2 = idx
    total_demand1 = calculate_total_demand(routes[route_i1],demand_list)
    total_demand2 = calculate_total_demand(routes[route_i2], demand_list)
    total_demand = total_demand1+total_demand2
    if total_demand <= capacity and not (route_i2==route_i1):
        if len(routes[route_i1])>1 and len(routes[route_i2])>1:
            if routes[route_i2][-1]==index2:
                routes[route_i2]=list(reversed(routes[route_i2]))
            if routes[route_i1][0]==index1:
                routes[route_i1]=list(reversed(routes[route_i1]))

        elif len(routes[route_i1])==1 and len(routes[route_i2]) >1:
            if routes[route_i2][-1]==index2:
                routes[route_i2]=list(reversed(routes[route_i2]))
        elif len(routes[route_i1])>1 and len(routes[route_i2])==1:

            if routes[route_i1][0]==index1:
                routes[route_i1]=list(reversed(routes[route_i1]))
        routes[route_i1]+=routes[route_i2]
        routes[route_i2] = []
        flag = True
    else:
        flag =  False
    return flag


def find_maximum2(savings_array):
    max_save = 0
    for i, row in enumerate(savings_array):
            for ind, val in enumerate(row):
                if val:
                    if val>max_save:
                        max_save= val
                        index1 = i
                        index2 = ind
    return max_save, index1, index2




def savings_heuristic(px, py, demand, capacity, depot):

    my_demands = []
    demand_list = demand.tolist()
    savings_array = nonearraymaker(len(demand_list), len(demand_list))
    total_demands =[]

    for i,row in enumerate(savings_array):
        for ind, val in enumerate(row):
            if i != ind:
                savings_array[i][ind] = utility.calculate_euclidean_distance(px, py,i, 0) + utility.calculate_euclidean_distance(px, py,0,ind) - utility.calculate_euclidean_distance(px, py, i, ind)
    routes = []
    for i in range(len(demand_list)):
        routes.append([i])
        total_demands.append(demand_list[i])
    for i in range(len(demand)*20):
        try:
            max_save, index1, index2 = find_maximum2(savings_array)
            savings_array[index1][index2] = None
            savings_array[index2][index1] =None
            flag=merge_routes(routes, index1, index2, demand_list, capacity)
            if flag:
                savings_array[index1] = nonelistmaker(len(savings_array[index1]))
        except:
            new_routes = []
            for el in routes:
                if el !=[0] and el != []:
                    new_routes.append([0]+el+[0])
                    my_demands.append(calculate_total_demand(el, demand_list))
            print(my_demands)
            print(new_routes)
            return new_routes

def main():

    # Paths to the data and solution files.
    vrp_file = "data/n32-k5.vrp"  # "data/n80-k10.vrp"
    sol_file = "data/n32-k5.sol"  # "data/n80-k10.sol"
    # vrp_file = "data/n80-k10.vrp"  # "data/n80-k10.vrp"
    # sol_file = "data/n80-k10.sol"
    # Loading the VRP data file.
    px, py, demand, capacity, depot = loader.load_data(vrp_file)

    vrp_best_sol = loader.load_solution(sol_file)
    my_distance = []
    for el in vrp_best_sol:
        my_distance.append([0]+el.tolist()+[0])
    best_distance = utility.calculate_total_distance(my_distance, px, py, depot)

    sh_solution = savings_heuristic(px, py, demand, capacity, depot)
    sh_distance = utility.calculate_total_distance(sh_solution, px, py, depot)
    print("Saving VRP Heuristic Distance:", sh_distance)
    utility.visualise_solution(sh_solution, px, py, depot, "Savings Heuristic")
    utility.save_solution("sh2", sh_solution, sh_distance)


if __name__ == '__main__':
    main()
