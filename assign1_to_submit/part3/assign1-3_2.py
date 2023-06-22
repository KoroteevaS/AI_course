#!/usr/bin/env python3
import pandas as pd
import random
import numpy as np
import sys
my_argvs = sys.argv
l = None
b= None
rounds= None
file_path = None
weights_zero = None
try:
	file_path = my_argvs[1]
except:
	print("Plese enter a file path. Otherwise place 'assign_1_3_2.data' to the script folder")

try:
	rounds = int(my_argvs[2])
	l = float(my_argvs[3])
	b = float(my_argvs[4])
	if my_argvs[5] == "f":
		weights_zero=False
except:
	print("""The program applies the perception algorithm upon the table from assignment1 part 3.2. 
		The data from table is in the ass1_3_2.data file.
		Learning rate is = 0.1 by default.Bios b = 1 by default. Number of iterations is 20 by default. 
		Weights as 0 lists by default.
		To change them use the following command python. Order of parameters should be the same.
		_______________________________________________________________________________________________________
		   python assign1-3_2.py assign1_3_2.data <your number of iterations> <your learning rate> <your bios> f
		________________________________________________________________________________________________________
		
		Example:
			python assign1-3_2.py ass1_3_2.data 3 0.01 -0.5 f

		""")
if not rounds:
	rounds = 20
if not l:
	l = 0.1
if not b: 
	b= 1
if not file_path:
	file_path = "ass1_3_2.data"
if  weights_zero != False:
	weights_zero = True


print("******Solving classification problem with perception.**********")
print("Data set = {}, Number of iterations = {}, learning rate = {}, bios = {}, initial weights are 0s = {}".format(file_path, rounds, l,b, weights_zero))



def values(v):

	"""Takes value of feature(s) and returns a percepted value 1 or 0 depends on feature value
	Parameters:
		v (NumPy obj)(float) - value of feature
	Return:
		1,0 - if v>=0 or v<0"""

	if v >= 0:
		return 1
	else:
		return 0

def percept(x, w, b):
	"""Calculates a perception according formula sum(w*x)+b and passes the result to value funcion.
	Parameters:
		x(int) - initial feature value
		w(int/float) - weight for particular feature
		b(int/float) - bios
	Return:
		y(int) - 0 or 1 - value of feature
	"""

	v = np.dot(w, x) + b
	y = values(v)
	return y

def zerolistmaker(n):
	"""Makes a list of zeros
	Parameters:
		n(int) - number of zeros in list
	Return:
		listofzero(list) - list of zeros
	"""
	listofzeros = [0] * n
	return listofzeros


def increase_weights(ws,i,y,d,l):
	"""Incresing weights in the weights list.
	Parameters:
		ws - weigths
		i - current working index
		y - value of function
		d - real class value
		l -learining, rate
	Retrurn:
		None
	"""
	for w in ws:
		if y>0:
			w[i] = round(w[i]-(d-y)*l,3)
		else:
			w[i]=round(w[i]+(d-y)*l,3)
	

def decrease_weights(ws,i,y,d,l):

	"""Decreasing weights in the weights list.
	Parameters:
		ws - weigths
		i - current working index
		y - value of function
		d - real class value
		l -learining, rate
	Retrurn:
		None
	"""
	for w in ws:
		if  y>0:
			w[i] =round(w[i]+(d-y)*l,3)
		else:
			w[i]=round(w[i]-(d-y)*l,3)



#######################DATA PREPARATION############################################################
data = pd.read_csv(file_path, delimiter=" ")
features = [data["Feature1"].to_list(),data["Feature2"].to_list(), data["Feature3"].to_list()]
classes = data["Class"].to_list()
if weights_zero == True:
	ws = [zerolistmaker(len(classes)),zerolistmaker(len(classes)),zerolistmaker(len(classes))]
if weights_zero == False:
	ws = [None,None,None]
	for i,el in enumerate(features):
		w_list = []
		for el in range(len(classes)):
			w_list+=[round(random.uniform(-1,1),2)]
		ws[i] = w_list

##########################ROUND LOOP###################################################################

print('-------Start calculations--------')
for rnd in range(rounds):
	correct_count=0
	for i,d in enumerate(classes):
		y= percept([features[0][i],features[1][i],features[2][i]],[ws[0][i],ws[1][i],ws[2][i]],b)
##########Perception learing part######################################################################
		if y!=d:
			if d==1 and y==0:
				increase_weights(ws,i,y,d,l)
			if d==0 and y ==1:
				decrease_weights(ws,i,y,d,l)
#######################################################################################################
		else:
			#print(correct_count)
			correct_count+=1
	

	print("Iteration ",rnd)
	print("Weigths: ",ws)
	print("Correct rate: {}%".format(round(correct_count/len(classes)*100,2)))
print("Filename = {}, number of iterations = {}, learning rate = {}, bios = {}, initial weights as zerous = {}".format(file_path, rounds, l,b,weights_zero) )


			