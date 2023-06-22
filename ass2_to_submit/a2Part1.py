import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from time import sleep


from NeuralNetwork import Neural_Network



def encode_labels(labels):

    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(labels)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoder = OneHotEncoder(sparse=False)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)

    return label_encoder, integer_encoded, onehot_encoder, onehot_encoded


if __name__ == '__main__':

    #Preparing training data
    data = pd.read_csv('penguins307-train.csv')
    labels = data.iloc[:, -1]
    instances = data.iloc[:, :-1]
    scaler = MinMaxScaler()
    instances = scaler.fit_transform(instances)
    label_encoder, integer_encoded, onehot_encoder, onehot_encoded = encode_labels(labels)
    #Preparing testing data
    pd_data_ts = pd.read_csv('penguins307-test.csv')
    accuracy_test = []
    test_labels = pd_data_ts.iloc[:, -1]
    test_instances = pd_data_ts.iloc[:, :-1]
    test_instances = scaler.transform(test_instances)
    test_label_encoder, test_integer_encoded, test_onehot_encoder, test_onehot_encoded = encode_labels(test_labels)


#Giving parameters of NN
    n_in = 4
    n_hidden = 2
    n_out = 3
    learning_rate = 0.2
    epochs = 100
#Giving initial weight
    initial_hidden_layer_weights = np.array([[-0.28, -0.22], [0.08, 0.20], [-0.30, 0.32], [0.10, 0.01]])
    initial_output_layer_weights = np.array([[-0.29, 0.03, 0.21], [0.08, 0.13, -0.36]])

    nn = Neural_Network(n_in, n_hidden, n_out, initial_hidden_layer_weights, initial_output_layer_weights,
                        learning_rate)
    print('First instance has label {}, which is {} as an integer, and {} as a list of outputs.\n'.format(
        labels[0], integer_encoded[0], onehot_encoded[0]))

    instance1_prediction = nn.predict([instances[0]])
    if instance1_prediction is None:
        instance1_predicted_label = "???"
    else:
        instance1_predicted_label = label_encoder.inverse_transform(instance1_prediction)
    print('Predicted label for the first instance is: {}\n'.format(instance1_predicted_label))
    delta_output_layer_weights, delta_hidden_layer_weights = nn.backward_propagate_error(instances[0], nn.hidden_layer_outputs, nn.output_layer_outputs, onehot_encoded[0])
    
    nn.update_weights(delta_output_layer_weights, delta_hidden_layer_weights)
    print('Weights after performing BP for first instance only:')
    print('Hidden layer weights:\n', nn.hidden_layer_weights)
    print('Output layer weights:\n', nn.output_layer_weights)

    epoches_list = []
    accuracy = []
    for epoch in range(epochs):
        count = 0
        count_right = 0
        count_test = 0
        count_right_test = 0
        print("#"*70)
        print("Epoch: ",epoch)
        print("#"*70)
        #Run training process for all the instances of training set
        for i, instance in enumerate(instances):
            print("-"*50)
            print(i)
            count +=1
            hidden_layer_outputs, output_layer_outputs = nn.forward_pass(instances[i])
            predicted_class = np.where(output_layer_outputs == np.amax(output_layer_outputs))[0]
            
            if predicted_class ==integer_encoded[i]:
                count_right+=1
          
            delta_output_layer_weights, delta_hidden_layer_weights = nn.backward_propagate_error(instances[i], hidden_layer_outputs, output_layer_outputs, onehot_encoded[i])
            nn.update_weights(delta_output_layer_weights, delta_hidden_layer_weights)
            print('Hidden layer weights \n', nn.hidden_layer_weights)
            print('Output layer weights  \n', nn.output_layer_weights)

        #running test data with previously set parameters
        for i, test_instance in enumerate(test_instances):
                count_test +=1
                hidden_layer_outputs, output_layer_outputs = nn.forward_pass(test_instance)
                predicted_class = np.where(output_layer_outputs == np.amax(output_layer_outputs))[0]
                if predicted_class ==integer_encoded[i]:
                    count_right_test+=1
        acc_test = round(count_right_test/count_test*100,2)
        
        acc = round(count_right/count*100,2)

        print("ACCURACY:", acc, "%")   
        print("ACCURACY for Test dataset:", acc_test, "%")

        #Preparing data for plot

        epoches_list.append(epoch)
        accuracy.append(acc)
        accuracy_test.append(acc_test)


    print("!!!!!!!!FINAL WEIGHTS!!!!!!!!!!!!!!!!!!!!!!!!")
    print('\nAfter training:')
    print('Hidden layer weights:\n', nn.hidden_layer_weights)
    print('Output layer weights:\n', nn.output_layer_weights)

    #Building plot

    plt.plot(accuracy, epoches_list)
    plt.plot(accuracy_test, epoches_list)
    plt.xlabel("accuracy")
    plt.ylabel("epochs")

    try:
        plt.savefig('fig3_accuracy_with_test.png', dpi=300, bbox_inches='tight')
    except:
        pass
    # plt.show()
    # sleep(15)
    # plt.close('all')