import pandas as pd
from time import sleep
import sys

my_argvs = sys.argv
training_file = my_argvs[1]
test_file = my_argvs[2]



#Preparing training data
labled_data = pd.read_csv(training_file, delimiter = " ", header = None)
labels = labled_data.iloc[:, -1]
instances = labled_data.iloc[:, :-1]
labels_list = labels.values.tolist()
instances = instances.values.tolist()


#Preparing testing data
unlabled_data = pd.read_csv(test_file, delimiter = " ", header = None)
test_instances_list  = unlabled_data.values.tolist()
# for i,el in enumerate(labels_list):
#     print(str(i) + ": " + str(el))
numb_spam = 1 #to avoid 0 case
numb_non_spam=1 # to avoid 0 case
for el in labels:
    if el ==  0:
        numb_non_spam+=1
    if el ==1:
        numb_spam+=1
print("Number of spam in training set is ", numb_spam)
print("Number of non spam in traing set is ", numb_non_spam)
prob_spam = numb_spam/(numb_spam+numb_non_spam)
prob_non_spam = numb_non_spam/(numb_spam+numb_non_spam)

print("Probability of spam in training set  - {}".format(prob_spam))
print("Probability of non spam in training set  - {}".format(prob_non_spam))


def count_probability(query_list, prob):
    enom = 1
    query_list.append(prob)
    for el in query_list:
        enom*=el
    denom = 1
    my_prob = enom/denom

    return my_prob



def onelistmaker(n):
    listofones = [1]*n
    return listofones
def onearraymaker(n, m):
    my_array = []
    for i in range(m):
        my_array.append(onelistmaker(n))
    return my_array
def zerolistmaker(n):
    listofzeros = [0]*n
    return listofzeros
def zeroarraymaker(n , m):
    my_array = []
    for ind in range(m):
        my_array.append(zerolistmaker(n))
    return my_array

def multiply_list(my_list) :
     
    result = 1
    for x in my_list:
         result = result * x
    return result

def make_join_probability_table():
    pass

def predict(test_instance):
    query_list_spam = []
    query_list_non_spam = []
    for i  in range(12):
        query_list_spam.append(probability_spam_table[i][test_instance[i]])
        query_list_non_spam.append(probability_non_spam_table[i][test_instance[i]])
    probability_spam = count_probability(query_list_spam, prob_spam )
    probability_non_spam = count_probability(query_list_non_spam, prob_non_spam)
    print("Probability of spam for {} is {}".format(test_instance, probability_spam))
    print("Probability of non spam for {} is {}".format(test_instance, probability_non_spam))
    if probability_spam>probability_non_spam:
        print("Result: SPAM")
    else:
        print("Result: NON SPAM")


def predict_labelled(test_instance):

    query_list_spam = []
    query_list_non_spam = []
    for i  in range(12):
        query_list_spam.append(probability_spam_table[i][test_instance[i]]) 
        query_list_non_spam.append(probability_non_spam_table[i][test_instance[i]])
    probability_spam = count_probability(query_list_spam, prob_spam )
    probability_non_spam = count_probability(query_list_non_spam, prob_non_spam)
    print("Probability of spam for {} is {}".format(test_instance, probability_spam))
    print("Probability of non spam for {} is {}".format(test_instance, probability_non_spam))

    if probability_spam>probability_non_spam:
        print('Result: SPAM')
        result = 1
    else:
        print('Result: NON SPAM')
        result = 0
    print("REAL CLASS ", test_instance[-1])
    if test_instance[-1] == result:
        return 1
    else:
        return 0
    
     

spam_count_table = onearraymaker(2, 12) #to avoid 0 case
non_spam_count_table = onearraymaker(2,12) #to avoid 0 case
probability_spam_table = zeroarraymaker(2,12)
probability_non_spam_table = zeroarraymaker(2,12)

#
print("Training process")
#Going through lines of the training set
for i, instance in enumerate(instances):
#Going through each featire
    for ind, feature in enumerate(instance):
        #labels_list in rach instance
        if labels_list[i]== 1:
            if feature == 0:
                spam_count_table[ind][0]+=1
                #print(spam_count_table)
            if feature ==1:
                spam_count_table[ind][1]+=1

        if labels_list[i]== 0:
                if feature == 0:
                    non_spam_count_table[ind][0]+=1
                if feature == 1:
                   non_spam_count_table[ind][1]+=1
                #print(non_spam_count_table)
for idx in range(12):
    #print(idx)
    probability_spam_table[idx][0] = spam_count_table[idx][0]/(numb_spam)
    probability_spam_table[idx][1] = spam_count_table[idx][1]/(numb_spam)
    probability_non_spam_table[idx][0] = non_spam_count_table[idx][0]/(numb_non_spam)
    probability_non_spam_table[idx][1] = non_spam_count_table[idx][1]/(numb_non_spam)

for ind, el in enumerate(probability_spam_table):
    print("Feature",ind, ": Probabilities for spam, if true = ",round(probability_spam_table[ind][1],2),", if false = ",round(probability_spam_table[ind][0],2),", for non spam, if true = ",round(probability_non_spam_table[ind][1],2),", for non spam, if false =",round(probability_non_spam_table[ind][0],2))

query_list = 0
right_count = 0
flag = False
for i,test_instance in enumerate(test_instances_list):
    print("#"*50)
    print("Instance ",i)
    if len(test_instance) ==13:
        flag = True
        count = predict_labelled(test_instance[:-1])
        right_count +=count
    if len(test_instance)==12:
        predict(test_instance)

if flag:
    acc = right_count /len(test_instances_list)
    print("Accuracy = ",acc)






    #     plt.savefig('fig3_accuracy_with_test.png', dpi=300, bbox_inches='tight')
    # except:
    #     pass
    # # plt.show()
    # # sleep(15)
    # # plt.close('all')