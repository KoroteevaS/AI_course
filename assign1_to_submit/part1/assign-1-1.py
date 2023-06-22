#!python3.8
import sys
import math
import collections

k=None

wine_test = sys.argv[2]
wine_training = sys.argv[1]
try:
	k = int(sys.argv[3])
except:
	pass
if not k:
	k=3
# wine_test = r"D:\AICourse\assignment1\ass1_data\part1\wine-test"
# wine_training = r"D:\AICourse\assignment1\ass1_data\part1\wine-training"
def e_distance(training_line, test_line, range_list):
    my_sum = 0
    for i in range(len(training_line)):
        my_sum += math.pow(float(training_line[i]) - float(test_line[i]), 2)/range_list[i]

    root = math.sqrt(my_sum)
    return root


def k_nearest(wine_training_array, test_line,  k, range_list):
	distances = {}
	for i,line in enumerate(wine_training_array):
		distances[i]=(e_distance(line[:-1],test_line[:-1], range_list))
	# print(distances)
	sorted_distances = sorted(distances.items(), key=lambda x: x[1])
	# print(sorted_distances[:k])
	result_dict = {}
	for el in sorted_distances[:k]:
		#print(el[0])
		# print(wine_training_array[el[0]][-1])
		# print('class')
		if wine_training_array[el[0]][-1] not in result_dict:
			result_dict[wine_training_array[el[0]][-1]] = 1
		else:
			result_dict[wine_training_array[el[0]][-1]] +=1
	sorted_results = sorted(result_dict.items(), key=lambda x: x[1])
	# print(sorted_results[-1][0])
	return sorted_results[-1][0]
def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros

def get_squared_ranges(array,features_number):
	range_list=[]
	max_list =[]
	min_list = []
	range_list = zerolistmaker(features_number)
	max_list=zerolistmaker(features_number)
	min_list=zerolistmaker(features_number)
	for ind,instance in enumerate(array):
		for i,feature in enumerate(instance[:-1]):
			if  float(feature)>max_list[i]:
				max_list[i]=float(feature)
			if min_list[i]==0 or min_list[i]>float(feature):
				min_list[i]=float(feature)
	#print(max_list)
	#print(min_list)
	for idx in range(len(max_list)):
		range_list[idx]=math.pow(max_list[idx]-min_list[idx],2)
	#print(range_list)
	return range_list



			



	# print(sorted_distances[0][0])

	# return(wine_training_array[sorted_distances[0][0]][-1])


	



def main():
	wine_test_array = []
	wine_training_array = []
	with open(wine_test,"r") as f_test:
		test_data = f_test.read()
	headers= test_data.split("\n")[0]
	for line in test_data.split("\n")[1:-1]:
		test_line = []
		for el in line.split(" "):
			test_line.append(el)
		wine_test_array.append(test_line)
	# print(wine_test_array)
	
	with open(wine_training, "r") as f:
		data = f.read()
	for line in data.split("\n")[1:-1]:
		training_line = []
		features_number = 0
		for el in line.split(" "):
			features_number+=1
			training_line.append(el)
		wine_training_array.append(training_line)
	features_number = features_number-1
	range_list=get_squared_ranges(wine_training_array, features_number)

	# print(wine_training_array)
	count = 0
	for i,ln in enumerate(wine_test_array):

		my_label = k_nearest(wine_training_array, ln,k, range_list)
		print(f'Instance {i+1}: {my_label}')
		# print(f'Hello, {os.getlogin()}! How are you?')
		# print("real label")
		# print(ln[-1])
		if my_label == ln[-1]:
			count+=1

	print(f'Accuracy: {int(round(count/len(wine_test_array),2)*100)}%')




if __name__ == '__main__':
	main()