import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
x = [ -1.2,   -0.9,      -0.6,   -0.3,  0,    0.3,    0.6,     0.9, 1.2]
y = [ -6.748, -5.119,  -3.976, -3.157, -2.5, -1.843, -1.024,  0.119 ,1.748 ]
# plt.plot(x,y)
# plt.show()
arr = pd.read_csv("regression.txt", sep="\t") 
print(arr)

