#taken from
import pandas as pd
import operator
import math
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
from matplotlib import pyplot as plt

data = pd.read_csv("regression.txt", sep=",")
print(data)
x_list = data['x'].to_list()
y_list = data['y'].to_list()

def my_super_func(x):
    return (x*4)-(2*x**3)+(x**2)

new_y_list = []
for el in range(len(x_list)):
    new_y_list.append(my_super_func(el))
print(new_y_list)
print(y_list)

#plt.plot(x_list, y_list)
plt.plot(x_list, new_y_list)
plt.xlabel("x")
plt.ylabel("y")

try:
    plt.savefig('fig6_equation.png', dpi=300, bbox_inches='tight')
except:
    pass
plt.show()