import pandas as pd
import random
import sys
my_argvs = sys.argv
learning_rate = None
rounds= None
features_number = None
image_file = None
weights_zero = None
print_image = False
print_weights = False
print_rates = False
iter_flag = False
try:
	image_file = my_argvs[1]
except:
	print("Plese enter a file path. Otherwise place 'assign_1_3_2.data' to the script folder")
try:
	rounds = int(my_argvs[2])
	features_number = int(my_argvs[3])
	learning_rate = float(my_argvs[4])
	if my_argvs[5] == "f":
		weights_zero=False
	if my_argvs[6] == "p":
		print_image = True
	if my_argvs[7] == "wout":
		print_weights = True
	if my_argvs[7] == "rout":
		print_rates = True
except:
	print("""
The program applies the perception algorithm upon the table from assignment1 part 3.1.
Simple call:
                           python assign1-3_1.py image.data

The data -  image.data set. Number of iterations is 20 by default. Number of features is 50 by default. Learning rate is = 0.1 by default
Weights initially set as 0s lists by default. It is not printing_images by default.Not printing rates or weights by default.

 To change the paramenters use the following command python. Order of parameters should be the same.
 ____________________________________________________________________________________________________________________________________________________
 python assign1-3_2_1.py image.data <your number of iterations> <your number of features><your learning rate> f/anything else p/enything else wout/rout
 ______________________________________________________________________________________________________________________________________________________

                Examples:
                        python assign1-3_1.py image.data 10 60 0.01 f p rout
			python assign1-3_1.py image.data 15 50 0.1 t f wout
			python assign1-3_1.py image.data 30 50 0.1 f p
			python assign1-3_1.py image.data 30 40

		""")
if not rounds:
	rounds = 20
if not learning_rate:
	learning_rate = 0.1
if not image_file:
	image_file = "image.data"
if  weights_zero != False:
	weights_zero = True
if not features_number:
	features_number = 50
previous_count = 0

def feature_sum(df,feature):

	"""

	The function takes feature and image data and counts all 3 True and False in signature.Compares with image data.
	Calculates Trues and returns feature value
	Arguments:
		df(obj) - pandas dataframe object with image
		feature(dict) - dictionary of features
	"""
	my_sum=None
	true_count = 0
	false_count = 0

	for i in range(3):
		if df[feature["col"][i]][feature["row"][i]] ==feature["sgn"][i]:

			true_count+=1
	if "dum"in feature.keys():
		return 1
	else:
		if true_count>=2:
			return 1
		else:
			return 0


def zerolistmaker(n):

	"""Makes a list of zeros
	Parameters:
		n(int) - number of zeros in list
	Return:
		listofzero(list) - list of zeros
	"""
	listofzeros = [0] * n
	return listofzeros

def image_reader():
	"""This function reads .pbm files end extracting images from them to create image array
	Retruns:
		images_list(lst) - countains 0 representing "white" and 1 reresenting "black" pixels"""

	with open(image_file, "r") as f:
		data = f.read()
	row_count = 1
	image=""
	images_list = []
	for row in data.split("\n")[:-1]:
		if row_count%5!=0: #splits file by five rows
			if len(row)>7: #image row
				image +=row
		else:
			image+=row
			image_row=[]
			image_list = []
			pic_count = 1
			for el in image:

				image_row+=[el]
				if pic_count%10==0:
					image_list +=[image_row]
					image_row = []
				pic_count+=1
			#print(image_list)
			if print_image:
				for line in image_list:
					ln = ""
					for el in line:
						ln+=el.replace("0"," ").replace("1", "X")
					print(ln)
			images_list+=[image_list]
			image = ""
		row_count+=1
	return images_list

def feature_maker(features_number):

	"""The function makes feature list of dictionaries which contains given number of features_number with random
	paramenters -3 column index, 3 row index, 3 signature
	Arguments:
		features_number(int) - given number of features
	Returns:
		my_features(list) - dictionaries with features

	"""

	my_features = []
	for idx in range(features_number+1):
		feature = {}
		feature["col"] = [random.randint(0,9),random.randint(0,9), random.randint(0,9)]
		feature["row"] = [random.randint(0,9),random.randint(0,9), random.randint(0,9)]
		feature["sgn"] = [str(random.randint(0,1)),str(random.randint(0,1)),str(random.randint(0,1))]
		my_features+=[feature]
	my_features[0]["dum"]=1
	return my_features

def get_weigts(image_feature_dict):

	"""Getting weights from array"""
	weight_lst = []
	for el in image_feature_dict.keys():
		for i,e in enumerate(image_feature_dict[el]):
			if i ==1:
				weight_lst+=[e]
	return weight_lst

def  image_feature_dict_maker(images_list, my_features):

	"""Creates dictionary which contains image inexes as keys and features and weights as lists,stored under each key

	Arguments:
		images_list(list) - list of lists with images
		my_features(list) - list of dictionaries with features
	Returns:
		image_feature_dict(dict) - which contains dictionaries with keys equal indexes of images and lists of features and weights stored
	"""
	image_feature_dict = {}
	perception ={}
	for idx, img in enumerate(images_list):
		for i, feature in enumerate(my_features):
			df = pd.DataFrame(img)
			value = feature_sum(df, feature)
			if not idx in image_feature_dict:
				image_feature_dict[idx] = [None, None ]
				image_feature_dict[idx][0] = [value]
				if weights_zero == False:
					image_feature_dict[idx][1]= [round(random.uniform(-1,1),2)]
				else:
				# 	image_feature_dict[idx][1]= 0
					image_feature_dict[idx][1] = [0]
			else:
				image_feature_dict[idx][0] += [value]
				if weights_zero == False:
					image_feature_dict[idx][1] +=[round(random.uniform(-1,1),2)]
				# 	image_feature_dict[idx][1] +=[0]
				else:
					image_feature_dict[idx][1]+=[0]
				
	return image_feature_dict


print("--------------------program starts --------------------------------")


images_list = image_reader()
my_features = feature_maker(features_number)
image_feature_dict = image_feature_dict_maker(images_list, my_features)
if print_weights:
	print(get_weigts(image_feature_dict))
for trial in  range(rounds):
	right_count = 0
	for i in image_feature_dict:
		percs = 0
		for idx, val in enumerate(image_feature_dict[i][0]):
			perc = val*image_feature_dict[i][1][idx]
			percs +=perc
		if i <50: #they are all x
			d = 1
			if percs<=0:
				for ind, ftr in enumerate(image_feature_dict[i][1]):
					image_feature_dict[i][1][ind]=round(image_feature_dict[i][1][ind]+image_feature_dict[i][0][ind]*learning_rate,3)
			else:
				right_count +=1
		if i >=50: #they are all 0
			d = 0
			if percs>0:
				for ind, ftr in enumerate(image_feature_dict[i][1]):
					image_feature_dict[i][1][ind] = round(image_feature_dict[i][1][ind]-image_feature_dict[i][0][ind]*learning_rate,3)
				#not sure here
				# weights[idx] = weights[idx]+(weights[idx]*learning_rate*(weights[idx]-values[idx]))

			else:
				right_count+=1
	if print_rates:
		print(len(image_feature_dict) - right_count)
	weights = get_weigts(image_feature_dict)
	#print(right_count)
	if print_weights:
		print(weights)
	
	if not iter_flag:
		if previous_count==int(right_count):
			my_iter = int(trial)
			my_weigts = get_weigts(image_feature_dict)	
			iter_flag = True	
	previous_count = int(right_count)

print("Wrong guesses: {}".format(len(image_feature_dict)-right_count))
if print_weights:
	print("Weights:")
	print(weights)
print("Stopped increasing on {} ".format(my_iter))
print("Number of iterations - {}, number of features - {}, learning_rate - {}, weights as zeros - {}, print images {}, print weights (wout) {}, print rates (rout) {}".format(rounds,features_number,learning_rate, weights_zero, print_image, print_weights, print_rates))
if print_weights:
	print(my_weigts)