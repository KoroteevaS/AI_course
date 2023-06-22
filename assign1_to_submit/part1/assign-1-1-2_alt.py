#!python3.8
import sys
import numpy as np
import math
from random import sample

my_argvs = sys.argv


k=None

try:
	wine_test = my_argvs[2]
except:
	wine_test = r"wine-test"
try:
	wine_training = my_argvs[1]
except:
	wine_training = r"wine-training"
try:
	k = my_argvs[3]
except:
	k=3
# wine_test = r"wine-test"
# wine_training = r"wine-training"



def e_distance(old_centroid_line, new_centroid_line):

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

def zerolistmaker(n):

	"""Makes a list of zeros
	Parameters:
		n(int) - number of zeros in list
	Return:
		listofzero(list) - list of zeros
	"""
	listofzeros = [0] * n
	return listofzeros

# def get_squared_ranges(array,features_number):

# 	max_list =[]
# 	min_list = []
# 	max_list=zerolistmaker(features_number)
# 	min_list=zerolistmaker(features_number)
# 	for ind,instance in enumerate(array):
# 		for i,feature in enumerate(instance):
# 			if  float(feature)>max_list[i]:
# 				max_list[i]=float(feature)
# 			if min_list[i]==0 or min_list[i]>float(feature):
# 				min_list[i]=float(feature)




def assign_to_centroids(wine_training_array, k_init_list):
	centroids = {}
	distances =[]
	clasters = {}
	for ind, instance in enumerate(wine_training_array):
		distances=[]
		for i in range(len(k_init_list)):
			# print(i)
			# print(instance)
			# print(len(instance))
			distance = e_distance(instance,k_init_list[i])#, range_list)
			distances+=[distance]
		# print(distances)
		for idx in range(len(distances)):
			# print(idx)
			# print(distances[idx])
			if distances[idx]==min(distances):
				# print(distances[idx])
				# print(idx)
				if not idx in centroids.keys():
					centroids[idx]=[ind]
				else:
					centroids[idx]+=[ind]
	return(centroids)


def find_mean(my_list):
	mean_list = zerolistmaker(13)
	#print(mean_list)
	for i in range(len(my_list)):
	#	print(my_list[i])
		one_list = my_list[i]
		for idx, number in enumerate(one_list):
			mean_list[idx]+=float(number)
	#print(mean_list)
	new_mean_list = []
	for el in mean_list:
		new_mean_list.append(el/len(my_list))
	#print(new_mean_list)
	return new_mean_list

		#mean_list[i] +=int(my_list[i])
	
def find_new_centroids(centroids_coordinates, wine_training_array,features_number):
	new_centroids = []
	#print("her1")
	for ind in centroids_coordinates.keys():
		#print(centroids_coordinates[ind])
		#print(len(centroids_coordinates[ind]))
		mean_list = find_mean(centroids_coordinates[ind])
		#print(mean_list)
		new_centroids.append(mean_list)
	return new_centroids

def find_centroids_coordinates(index_dict, wine_training_array):
	#print(index_dict)

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



def find_new_centroids_old(centroids, wine_training_array,features_number):

	new_centroids = {}
	new_centroids_loc = {}
	new_centroids_tuple = {}
	centroids_length={}
	new_centroids_dict = {}
	my_new_cluster_values = []
	for ind in centroids.keys():
		centroids_length[ind] = len(centroids[ind])
		for i, instance in enumerate(wine_training_array):
			# print(i)
			# print(centroids[ind])
			
			if i in centroids[ind]:
				for idx, feature in enumerate(instance):
					
					if not ind in new_centroids.keys():
						new_centroids[ind]=[feature]
					else:
						new_centroids[ind]+=[feature]
					if not ind in new_centroids_tuple.keys():

						new_centroids_tuple[ind]=[(i, feature)]
					else:
						new_centroids_tuple[ind]+=[(i,feature)]
	print(new_centroids_tuple)
	for new_centr_index in new_centroids.keys():
		# print("##########################")
		# print("##########################")
		# print("##########################")
		# print("##########################")
		# print("##########################")
		# print("##########################")
		# print("##########################")
		# print(new_centr_index)
		centroids_index = 0
		my_sum = 0
		my_new_cluster_values = []
		for i,feature in enumerate(new_centroids[new_centr_index]):
			print("-----------------------")
			#print(i)
			print(feature)
			#print(centroids_index)
			print(centroids[new_centr_index][centroids_index])
			my_sum+=float(feature)
		# 	print(i)
			print("sum")
			print(my_sum)
			print(features_number)
			if (i+1)%(features_number)==0:
				print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
				centroids_index+=1
				
				print(my_sum/centroids_length[new_centr_index])
				my_new_cluster_values += [my_sum/centroids_length[new_centr_index]]
				my_sum=0

		new_centroids_dict[new_centr_index] = my_new_cluster_values
	print(new_centroids_dict)
	return(new_centroids_dict)
			
			

def find_k_initials(wine_training_array, k):
	k_init = sample(range(0,len(wine_training_array)),k)
	# print(k_init)
	return k_init
# def compare_centroids(old_centroids, new_centroids, diff):
# 	for ind in range(len(old_centroids)):
# 		for i in range(len(old_centroids[ind])):
# 			old_centroids[i]
def centroids_routine(wine_training_array, k_init_list,features_number):
	#print(k_init_list)
	centroids = assign_to_centroids(wine_training_array, k_init_list)
	#print("centroids")
	#print(centroids)
	len(centroids[0])
	centroids_coordinates = find_centroids_coordinates(centroids, wine_training_array)
	#print("centroids_coordinates")
	#print(centroids_coordinates)
	#print(len(centroids_coordinates[0]))
	new_centroids = find_new_centroids(centroids_coordinates, wine_training_array, features_number)

	#print(new_centroids)
	# print(k_init_list)
	#print(new_centroids)
	#print(len(new_centroids[0]))
	#print(k_init_list)
	#print(len(k_init_list[0]))

	# reorg_new_centroids = {}

	# reorg_k_init = []
	# for i, nc in enumerate(new_centroids):

	# 	# print(nc)
	# 	# print(i)
	# 	min_ed = 0

	# 	for ind, oc in enumerate(k_init_list):
	# 		ed = e_distance(oc,nc )
	# 		# print(ed)
	# 		if min_ed ==0 or ed<min_ed:
	# 				min_ed = float(ed)
	# 		# print(min_ed)
	# 	for ind, oc in enumerate(k_init_list):
	# 		if e_distance(oc,nc ) == min_ed:
	# 			reorg_k_init += [oc]
	# #print(reorg_k_init)
	sum_ed = 0
	for idx , centr in enumerate(new_centroids):
		ed =e_distance(centr, k_init_list[idx])
		sum_ed+=ed
	return sum_ed, new_centroids



def main():
	# wine_test_array = []
	wine_training_array = []
	with open(wine_training,"r") as f_training:
		data = f_training.read()
	headers= data.split("\n")[0].split(" ")
	for line in data.split("\n")[1:-1]:
		t_line = []
		features_number=0
		for ind, el in enumerate(line.split(" ")):
		# 	print(ind)
		# 	print(len(line.split(" "))-1)
		# quit()
			if ind != len(line.split(" "))-1:
				t_line.append(el)
				features_number+=1
		wine_training_array.append(t_line)
	
	#range_list = get_squared_ranges(wine_training_array, features_number)

	k_init = find_k_initials(wine_training_array, k)

	k_init_list = []
	x_data = []
	#y_data = []
	k_init_list = [wine_training_array[ind] for ind, line in enumerate(wine_training_array) if ind in k_init]
		#print(k_init_list)
	my_list = k_init_list
	new_list =[]
	for i in range(10):
		# print(i)
		# print(my_list)
		# print(new_list)

		my_sum,my_list=centroids_routine(wine_training_array, my_list,features_number)
		print(my_list)
		#my_list =list(new_list)
		# print("!!!!!!!!!!!!!!!!!!!!!!!!")
		# print(my_sum)
		# print("!!!!!!!!!!!!!!!!!!!!!")

	


# 	#compare_centroids(k_init_list, new_centroids_list, diff)
# 	#print(new_list)

# 	# dd = []  
# 	# d = distant_dict(wine_training_array, k_init_list)
# 	# print(d)
# 	# clusters = assign_cluster(d, k)
# 	# data_clusters = [[],[],[]]
# 	# for ind in range(len(clusters)):
# 	# 	for inst in clusters[ind]:
# 	# 		data_clusters[ind].append(wine_training_array[inst])
# 	# print(data_clusters)
# 	# centr_dict = assign_centroid(data_clusters)
# 	#fig, ax = plt.subplots()
# 	#ax.plot(data_clusters[0],y_data,linestyle='', marker='o')
# # 	ax.plot(k_xdata,k_ydata, linestyle = '', color = "red",marker = "+")
# # 	loc = plticker.MultipleLocator(base=5.0) # this locator puts ticks at regular intervals
# # 	ax.xaxis.set_major_locator(loc)
# # 	plt.xlabel(headers[0])
# # 	plt.ylabel(headers[1])
# # 	plt.title(f'{headers[0]} vs {headers[1]}')
# # 	#plt.legend()
# # # 	label = ind+1
# # 	plt.show()


# 		# 	if dd[0][i]< dd[1][i] and dd[0][i]<dd[2][i]:
# 	# 		cluster1.append(dd[0])
# 	# 	if dd[1][i] <dd[0][i] and dd[1][i]<dd[2][i]:
	# 		cluster2.append(dd[1])
	# 	else:
	# 		cluster3.append(dd[2])
	# print(cluster1)
	# print(len(cluster1))
	# print(cluster2)
	# print(len(cluster2))			




	# 	if i+1  not in dd.keys():
	# 		dd[i+1] = d
	# 	else:
	# 		dd[i+1] += {d}
	# print(dd)
	
# 	print(y_data)
# 	print(headers)
# 	print(k_init_list)
# 	# plt.plot(x_data,y_data,label=0, linestyle='', marker='o')
# 	# plt.xticks(np.arange(float(min(x_data)), float(max(x_data))+1, 5.0))
# 	# plt.xlabel(headers[0])
# 	# plt.ylabel(headers[1])
# 	# plt.title(f'{headers[3]} vs {headers[4]}')
# 	k_xdata = []
# 	k_ydata = []
# 	for el in k_init_list:
# 		k_xdata.append(el[0])
# 		k_ydata.append(el[1])

# 	fig, ax = plt.subplots()
# 	ax.plot(x_data,y_data,linestyle='', marker='o')
# 	ax.plot(k_xdata,k_ydata, linestyle = '', color = "red",marker = "+")
# 	loc = plticker.MultipleLocator(base=5.0) # this locator puts ticks at regular intervals
# 	ax.xaxis.set_major_locator(loc)
# 	plt.xlabel(headers[0])
# 	plt.ylabel(headers[1])
# 	plt.title(f'{headers[0]} vs {headers[1]}')
# 	#plt.legend()
# # 	label = ind+1
# 	plt.show()
# # 	sleep(1)
# # 	plt.close("all")
# 	# print(wine_training_array)
# 	# count = 0
# 	# print(len(wine_training_array))
# 	# for i,ln in enumerate(wine_test_array):

# 	# 	my_label = k_nearest(wine_training_array, ln,k)
# 	# 	print(f'Instance {i+1}: {my_label}')
# 	# 	# print(f'Hello, {os.getlogin()}! How are you?')
# 	# 	# print("real label")
# 	# 	# print(ln[-1])
# 	# 	if my_label == ln[-1]:
# 	# 		count+=1

# 	# print(f'Accuracy: {int(round(count/len(wine_test_array),2)*100)}%')





if __name__ == '__main__':
	main()