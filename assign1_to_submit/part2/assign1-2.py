import pandas as pd
import numpy as np
import math
from pprint import pprint
import os
from collections import Counter
import sys


my_argvs = sys.argv
print(my_argvs)

try:
    first_file = my_argvs[1]
except:
    first_file = r"hepatitis-training"

try:
    testing_file = my_argvs[2]
except:
    testing_file = r"hepatitis-test"

route_nodes_dict = {}
data  = pd.read_csv(first_file , sep=" ")
target = data["Class"]

attributes = ['AGE', 'FEMALE', 'STEROID', 'ANTIVIRALS', 'FATIGUE', 'MALAISE','ANOREXIA','BIGLIVER','FIRMLIVER','SPLEENPALPABLE','SPIDERS','ASCITES', 'VARICES', 'BILIRUBIN', 'SGOT', 'HISTOLOGY']
testing_data = pd.read_csv(testing_file, sep = " ")

count = 0

def impurity_counter0(my_list):

    if len(my_list)!= 0:
        return((Counter(my_list)["live"]/len(my_list))*(Counter(my_list)["die"]/len(my_list)))
    else:
        return 0
def impurity_counter(my_list):
    if len(my_list)!=0:
        return (Counter(my_list)["live"]*Counter(my_list)["die"])/math.pow(len(my_list),2)
    else:
        return 0


def get_data(data, attribute_name, target_name):

    left_branch = []
    right_branch =[]
    left_indexes_list = []
    right_indexes_list = []
    for i in data.index.values:
        if data[attribute_name][i] == True:
            left_branch+=[data[target_name][i]] 
            left_indexes_list+=[i]           
        if data[attribute_name][i] == False:
            right_branch += [data[target_name][i]]
            right_indexes_list+=[i]
    true_imp = impurity_counter(left_branch)
    false_imp = impurity_counter(right_branch)
    average_imp = (true_imp*len(left_branch)/(len(left_branch)+len(right_branch)))+(false_imp*len(right_branch)/(len(left_branch)+len(right_branch)))
    return(attribute_name, average_imp, left_indexes_list, right_indexes_list)


    
def predict(query,tree,default = 1):
    

    for key in list(query.keys()):

        if key in list(tree.keys()):
            try:
                result = tree[key][query[key]] 
            except:
                return default
  
            result = tree[key][query[key]]
            if isinstance(result,dict):
                return predict(query,result)

            else:
                return result

def test(data,tree):

    queries = data.iloc[:,1:].to_dict(orient = "records") 
    predicted = pd.DataFrame(columns=["predicted"]) 
    for i in range(len(data)):
        predicted.loc[i,"predicted"] = predict(queries[i],tree,1.0) 
    predicted_list = predicted["predicted"].to_list()
    new_pred = []
    for el in predicted_list:
        new_pred+=[el[0]]
    pred = pd.DataFrame(new_pred)
    print('Accuracy is: ',round((np.sum(new_pred == data["Class"])/len(data))*100,2),'%')
       


def find_probability(my_data, value, originaldata):

    counts = my_data.value_counts()[value]
    return counts/len(originaldata)

def DT_builder(data,originaldata,attributes,target_attribute_name="Class",parent_node_class = None):

    if len(np.unique(data[target_attribute_name])) <= 1:
        return [np.unique(data[target_attribute_name])[0], round(find_probability(data[target_attribute_name],data[target_attribute_name].values[0], originaldata),2)]
    #instance is empty
    elif len(data)==0:
        return [np.unique(originaldata[target_attribute_name])[np.argmax(np.unique(originaldata[target_attribute_name],return_counts=True)[1])],1]
    #features are zero    
    elif len(attributes) ==0:
        return parent_node_class
       
    else:
        #getting maximum occurance inside one class name
        parent_node_class = np.unique(data[target_attribute_name]) [np.argmax(np.unique(data[target_attribute_name],return_counts=True)[1])]
        impurity_list = [get_data(data, attribute, target_attribute_name) for attribute in attributes]
        best_attribute_data = min(impurity_list, key = lambda t: t[1])
        best_attribute = best_attribute_data[0]
        left_branch = best_attribute_data[2]
        right_branch = best_attribute_data[3]
        tree = {best_attribute:{}}
        #Removing used node from attributes
        attributes = [i for i in attributes if i != best_attribute]
        #Removing used attribute from dataset
        subdata =data.drop([best_attribute], axis =1)

        for el  in [left_branch, right_branch]:
            sub_data = data.loc[el ]
            if el == left_branch:
                value = True
            if el == right_branch:
                value = False
            #print(data.where(data[best_attribute] == value).dropna())           
            subtree = DT_builder(sub_data,data,attributes,target_attribute_name,parent_node_class)
            tree[best_attribute][value] = subtree

            
        return(tree)   

tree = DT_builder(data, data, attributes)
print(tree)
test(testing_data, tree)
count =0