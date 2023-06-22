import sys
import numpy as np
import math
from random import sample


my_argvs = sys.argv


k=None
print(my_argvs)
# try:
# 	wine_test = my_argvs[2]
# except:
# 	wine_test = r"wine-test"
try:
	wine_training = my_argvs[1]
except:
	wine_training = r"wine-training"
try:
	k = int(my_argvs[2])
except Exception as e:
	k=3
# wine_test = r"wine-test"
# wine_training = r"wine-training"



def e_distance2(old_centroid_line, new_centroid_line):

	"""Measuring distance between points (without normalising data)
	Arguments:
		old_centroid_line(list) - contains point's coordinates
		new_centroid_line(list) - contains other point's coordinate"
	Return:
		dist(float) - distance value
	"""
	my_sum = 0
	for i in range(len(old_centroid_line)):
		my_sum += math.pow(float(old_centroid_line[i]) - float(new_centroid_line[i]), 2)
	dist = math.sqrt(my_sum)
	return dist

def e_distance(instance, centroid_line, range_list):

	"""Measuring distance between points with normalising data"""
	my_sum = 0
	for i in range(len(instance)):
		my_sum += math.pow(float(instance[i]) - float(centroid_line[i]), 2)/range_list[i]
	root = math.sqrt(my_sum)
	return root


def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros

def get_squared_ranges(array,features_number):

	"""
	Gets list of squared ranges for each feature
	"""
	range_list = zerolistmaker(features_number)
	max_list=zerolistmaker(features_number)
	min_list=zerolistmaker(features_number)
	for ind,instance in enumerate(array):
		for i,feature in enumerate(instance):
			if  float(feature)>max_list[i]:
				max_list[i]=float(feature)
			if min_list[i]==0 or min_list[i]>float(feature):
				min_list[i]=float(feature)

	for idx in range(len(max_list)):
		range_list[idx]=math.pow(max_list[idx]-min_list[idx],2)
	return range_list



def assign_to_centroids(wine_training_array, k_init_list,range_list):

	"""Assigns points to centroids
	Arguments:
		wine_training_array(list) - data set
		k_init_list (list)- initial of further list of k coordinates
	Returns:
		centroids(dict) - dictionary with k clusters represented by indexes of instances
	"""
	centroids = {}
	distances =[]
	clasters = {}
	for ind, instance in enumerate(wine_training_array):
		distances=[]
		for i in range(len(k_init_list)):
			distance = e_distance(instance,k_init_list[i], range_list)
			distances+=[distance]

		for idx in range(len(distances)):
			if distances[idx]==min(distances):
				if not idx in centroids.keys():
					centroids[idx]=[ind]
				else:
					centroids[idx]+=[ind]

	return(centroids)


def find_mean(my_list):

	"""Finding means
	Returns:
		new_mean_list(lst) - with lists with means
	"""
	mean_list = zerolistmaker(13)

	for i in range(len(my_list)):
		one_list = my_list[i]
		for idx, number in enumerate(one_list):
			mean_list[idx]+=float(number)
	new_mean_list = []
	for el in mean_list:
		new_mean_list.append(el/len(my_list))
	return new_mean_list

	
def find_new_centroids(centroids_coordinates, wine_training_array,features_number):

	"""Finding new centroids by using mean function
	Arguments:
		centroids_coordinates(dictionary) - centroids with their coordinates
		features_number(int) - the number of features
		wine_training_array(list) -with lists - data set
	"""
	new_centroids = []
	for ind in centroids_coordinates.keys():
		mean_list = find_mean(centroids_coordinates[ind])
		new_centroids.append(mean_list)
	return new_centroids

def find_centroids_coordinates(index_dict, wine_training_array):

	"""Finding coordinates for all the points assignted to the  centroid
	Arguments:
		index_dict(dict) - dictionary of centroid with indexes of instances
	Returns:
		centroids_coordinates(dict) - with centroids index as key and lists of coordinates of all the points assigned

	"""
	centroids_coordinates = {}
	for i in index_dict.keys():
		my_list = index_dict[i]
		for ind , instance in enumerate(wine_training_array):
			if ind in my_list:
				if not i in centroids_coordinates.keys():
					centroids_coordinates[i] = [instance]
				else:
					centroids_coordinates[i] +=[instance]

	return(centroids_coordinates)


def find_k_initials(wine_training_array, k):
	"""Finding k centroids for the first time
	Arguments:
		k(int) - number of clusters givent as input
	Returns:
		k_init (list) - list of indexes of instances choosen for k_init
	"""
	k_init = sample(range(0,len(wine_training_array)),k)
	return k_init

def len_clusters(centroids):
	cl_length_dict = {}
	for el in centroids.keys():
		cl_length_dict[el] = len(centroids[el])
	return(cl_length_dict)

def centroids_routine(wine_training_array, k_init_list,range_list,features_number):

	"""The main clustering routine - implementation of clastering method algorythm

		2. Create k clusters by assigning every instance to the nearest cluster: based on the nearest mean according to the distance measure
		3. Replace the old means with the centroid(mean) of each cluster
		4. Repeat the above two steps until convergence (no change in each cluster centroid). 
	
	Returns:
		new_centroids(list) - of lists with new_centroids coordinates

	"""
	centroids = assign_to_centroids(wine_training_array, k_init_list,range_list)
	len(centroids[0])

	cl_length_dict = len_clusters(centroids)
	centroids_coordinates = find_centroids_coordinates(centroids, wine_training_array)
	new_centroids = find_new_centroids(centroids_coordinates, wine_training_array, features_number)


	return centroids, cl_length_dict, new_centroids

def get_data_to_array():

	"""Gets data to array
	Returns:
		wine_training_array(list) - list of lists with data set
		features_number(int) - number of features
		classes(list) - list of classes
	"""
	classes = []
	wine_training_array = []
	with open(wine_training,"r") as f_training:
		data = f_training.read()
	headers= data.split("\n")[0].split(" ")

	for line in data.split("\n")[1:-1]:
		#print(line)
		t_line = []
		features_number=0
		for ind, el in enumerate(line.split(" ")):
			if ind != len(line.split(" "))-1:
				t_line.append(el)
				features_number+=1
			else:
				classes.append(el)
		wine_training_array.append(t_line)
	return(wine_training_array, classes, features_number)



def main():
	


	wine_training_array, classes, features_number = get_data_to_array()
	range_list = get_squared_ranges(wine_training_array, features_number)
	k_init = find_k_initials(wine_training_array, k)

	k_init_list = []
	#getting lists with coordinates
	k_init_list = [wine_training_array[ind] for ind, line in enumerate(wine_training_array) if ind in k_init]

	#print('The coordinates of the centroids')
	#print('Starting from k_init')
	#print(k_init_list)
	my_list = list(k_init_list)
	dist_sum = 1
	count = 0
	while int(dist_sum)!=0:
		count +=1

		previous_list = list(my_list)
		centroids,cl_length_dict,my_list=centroids_routine(wine_training_array, my_list,range_list,features_number)
		#print(my_list)
		new_old_distances = []
		new_old_distances = [e_distance2(el, my_list[i]) for i,el in enumerate(previous_list)]
		dist_sum = 0
		for el in new_old_distances:
			dist_sum+=el

	

	print("The convergence of centroids happened on {} iteration". format(count))

	print("Final centroids coordinates:")
	print(my_list)
	print("The size of the final {} clusters is {}".format(k, list(cl_length_dict.values())))
	print('!!!!!!!!!!!!!!!!!!!!')
	print(centroids)
	#FURTHER LITTLE ANALYSIS
	class_dict  = {}
	for i,el in enumerate(classes):
		my_key = int(el)-1
		if not my_key in class_dict.keys():

			class_dict[my_key] = [i]
		else:
			class_dict[my_key].append(i)
	corrects = 0
	print(class_dict)
	print('!!!!!!!!!!!!!!!!!!!!!!!')
	for  i,el in enumerate(class_dict.keys()):
		corrects = 0
		for ind,inst in enumerate(class_dict[el]):
			if inst in centroids[el]:
				corrects+=1
		if not "test" in wine_training:
			print("The rate of right guesses for class {} is {}%".format(i+1, corrects/len(class_dict[el])*100))
	new_class_dict = {}
	if "test" in wine_training:
		for i, el in enumerate(class_dict.keys()):
			if el == 0:
				new_class_dict[1] =class_dict[el]
			elif el == 2:
				new_class_dict[0] = class_dict[el]
			else:
			 	new_class_dict[2] = class_dict[el]

		for  i,el in enumerate(new_class_dict.keys()):
			corrects = 0
			if i == 1:
				my_class = 0+1
			if i == 2:
				my_class = 1+1
			if i == 0:
				my_class = 2+1
			for ind,inst in enumerate(new_class_dict[el]):
				if inst in centroids[el]:
					corrects+=1
			print("The rate of right guesses for class {} is {}%".format(my_class, corrects/len(new_class_dict[el])*100))









	#print(wine_training_array)

	


	




if __name__ == '__main__':
	main()