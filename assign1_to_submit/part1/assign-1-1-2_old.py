import sys
import math
import collections
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import random

#Select the annual income and the spending score columns X=dataset.iloc[:, [3,4]].values
#from sklearn.cluster import KMeans
wcss=[]



k=None

# wine_test = sys.argv[2]
# wine_training = sys.argv[1]
try:
	k = int(sys.argv[3])
except:
	pass
if not k:
	k=3


wine_test = "wine-test"
wine_training = "wine-training"

def e_distance(training_line, test_line):
    my_sum = 0
    for i in range(len(training_line)):
        my_sum += math.pow(float(training_line[i]) - float(test_line[i]), 2)
    root = math.sqrt(my_sum)
    return root

def findClosestCentroids(centroids, X):
    assigned_centroid = []
    for i in X:
        distance=[]
        for j in centroids:
            distance.append(e_distance(i, j))
        assigned_centroid.append(np.argmin(distance))
    return assigned_centroid

def calc_centroids(clusters, X):
    new_centroids = []
    new_df = pd.concat([pd.DataFrame(X), pd.DataFrame(clusters, columns=['cluster'])],
                      axis=1)
    for c in set(new_df['cluster']):
        current_cluster = new_df[new_df['cluster'] == c][new_df.columns[:-1]]
        cluster_mean = current_cluster.mean(axis=0)
        new_centroids.append(cluster_mean)
    return new_centroids


def calc_centroids(clusters, X):
    new_centroids = []
    new_df = pd.concat([pd.DataFrame(X), pd.DataFrame(clusters, columns=['cluster'])],
                      axis=1)
    for c in set(new_df['cluster']):
        current_cluster = new_df[new_df['cluster'] == c][new_df.columns[:-1]]
        cluster_mean = current_cluster.mean(axis=0)
        new_centroids.append(cluster_mean)
    return new_centroids
def main():
	
	dataset= pd.read_csv(wine_training,delimiter=" ")
	X = np.array(dataset[:-1])
	init_centroids = random.sample(range(0, len(dataset)), 3)
	print(init_centroids)
	centroids = []
	for i in init_centroids:
	    centroids.append(dataset.loc[i])
	print(centroids)
	centroids = np.array(centroids)
	print(centroids)
	get_centroids = findClosestCentroids(centroids, X)
	print(get_centroids)
	for i in range(100):
	    get_centroids = findClosestCentroids(centroids, X)
	    centroids = calc_centroids(get_centroids, X)
	print("here")
	print(centroids)
	print(get_centroids)
	my_dict = {}
	for el in get_centroids:
		if el in my_dict:
			my_dict[el]+=1
		else:
			my_dict[el]=1
	print(my_dict)

	    # plt.figure()
	    # plt.scatter(np.array(centroids)[:, 0], np.array(centroids)[:, 1], color='black')
	    # plt.scatter(X[:, 0], X[:, 1], alpha=0.1)
	    # plt.show()

	wine_training_array = []
	with open(wine_training,"r") as f_training:
		data = f_training.read()
	headers= data.split("\n")[0]
	train_line = []
	for line in data.split("\n")[1:-1]:
		train_line = []
		for el in line.split(" "):
			train_line.append(el)
		wine_training_array.append(train_line)
	check_dict = {}
	for el in wine_training_array:
		if el[-1] in check_dict:
			check_dict[el[-1]]+=1
		else:
			check_dict[el[-1]]=1
	print(check_dict)
	# for i in range(1,16): 
	#      kmeans = KMeans(n_clusters=i, init ='k-means++', max_iter=300,  n_init=10,random_state=0 )
	# kmeans.fit(X)
	# wcss.append(kmeans.inertia_)
	# plt.plot(range(1,11),wcss)
	# plt.title('The Elbow Method Graph')
	# plt.xlabel('Number of clusters')
	# plt.ylabel('WCSS')
	# plt.show()



if __name__ == '__main__':
	main()