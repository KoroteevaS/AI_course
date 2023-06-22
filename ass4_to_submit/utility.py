import matplotlib.pyplot as plt
import math

def save_solution(name, routes,cost):
    
    with open(name +".sol", "w") as f:
         f.write("")
    for i,el in enumerate(routes):

            my_row = "Route #" + str(i+1) +": " 
            for ind,e in enumerate(el):
                if ind!=0 and ind !=len(el)-1:
                    my_row+=str(e) + " "
            my_row.rstrip(" ")
            with open(name +".sol", "a") as f:
                f.write(my_row)
                f.write("\n")
    with open (name+".sol", "a") as f:
        f.write("Cost "+str(cost))


def calculate_euclidean_distance(px, py, index1, index2):


    """
    Calculating the Euclidean distances between two nodes

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param index1: Node 1 index in the coordinate list.
    :param index2: Node 2 index in the coordinate list.
    :return: Euclidean distance between node 1 and 2.
    """
    dist=math.pow(px[index1] - px[index2],2)+math.pow(py[index1] - py[index2],2)
    root = math.sqrt(dist)

    return root

def calculate_total_distance(routes, px, py, depot):

    """
    Calculating the total Euclidean distance of a solution.

    :param routes: List of routes (list of lists).
    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param depot: Depot.
    :return: Total tour euclidean distance.
    """

    total_distance = 0
    for route in routes:
        #print(route)
        my_sum = 0
        for ind in range(len(route)-1):
            # print(route[ind])
            # print(route[ind+1])
            # print(ind)
      
            # print(ind+1)
            # print(route)
            my_sum += calculate_euclidean_distance(px, py, route[ind], route[ind+1])
        total_distance+=my_sum

    return total_distance



def visualise_solution(vrp_sol, px, py, depot, title):

    """
    Function for visualise the tour on a 2D figure.

    :param vrp_sol: The vrp solution, which is a list of lists (excluding the depot).
    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param depot: the depot index
    :param title: Plot title.
    """

    n_routes = len(vrp_sol)
    s_vrp_sol = vrp_sol

    # Set axis too slightly larger than the set of x and y
    min_x, max_x, min_y, max_y = min(px), max(px), min(py), max(py)
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    width = (max(px) - min(px)) * 1.1
    height = (max(py) - min(py)) * 1.1

    min_x = center_x - width / 2
    max_x = center_x + width / 2
    min_y = center_y - height / 2
    max_y = center_y + height / 2

    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)

    plt.plot(px[depot], py[depot], 'rs', markersize=5)

    cmap = plt.cm.get_cmap("tab20", n_routes)
    for k in range(n_routes):
        a_route = s_vrp_sol[k]

        # Draw the route: linking to the depot
        plt.plot([px[depot], px[a_route[0]]], [py[depot], py[a_route[0]]], color=cmap(k))
        plt.plot([px[a_route[-1]], px[depot]], [py[a_route[-1]], py[depot]], color=cmap(k))

        # Draw the route: one by one
        for i in range(0, len(a_route)-1):
            plt.plot([px[a_route[i]], px[a_route[i + 1]]], [py[a_route[i]], py[a_route[i + 1]]], color=cmap(k))
            plt.plot(px[a_route[i]], py[a_route[i]], 'co', markersize=5, color=cmap(k))

        plt.plot(px[a_route[-1]], py[a_route[-1]], 'co', markersize=5, color=cmap(k))

    plt.title(title)
    plt.show()
