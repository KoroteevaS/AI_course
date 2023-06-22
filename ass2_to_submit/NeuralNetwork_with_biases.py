import numpy as np


class Neural_Network:
    # Initialize the network
    def __init__(self, num_inputs, num_hidden, num_outputs, hidden_layer_weights, output_layer_weights, learning_rate, output_biases, hidden_biases):
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs

        self.hidden_layer_weights = hidden_layer_weights
        self.output_layer_weights = output_layer_weights

        self.learning_rate = learning_rate
        self.output_biases = output_biases
        self.hidden_biases = hidden_biases


    def sigmoid(self, input):
        output = 1/(1+np.exp(-input))
        return output

    def forward_pass(self, inputs):
        hidden_layer_outputs = []
        for i in range(self.num_hidden):
            weighted_sum = np.dot(self.hidden_layer_weights[:,i],inputs)+self.hidden_biases[i]
            output = self.sigmoid(weighted_sum)
            hidden_layer_outputs.append(output)

        output_layer_outputs = []
        for i in range(self.num_outputs):
            weighted_sum = np.dot(self.output_layer_weights[:,i],hidden_layer_outputs)+self.output_biases[i]
            output = self.sigmoid(weighted_sum)
            output_layer_outputs.append(output)

        return hidden_layer_outputs, output_layer_outputs

    def backward_propagate_error(self, inputs, hidden_layer_outputs, output_layer_outputs, desired_outputs):

        output_layer_betas = np.zeros(self.num_outputs)
        output_layer_betas = np.subtract(desired_outputs, output_layer_outputs)
        print('OL betas: ', output_layer_betas)
        hidden_layer_betas = np.zeros(self.num_hidden)
        for j,hb in enumerate(hidden_layer_betas):

            hid_betta = 0
            for k, oo in enumerate(output_layer_outputs):
                hid_betta += output_layer_betas[k]*output_layer_outputs[k]*(1- output_layer_outputs[k])*self.output_layer_weights[j][k]
            hidden_layer_betas[j] = hid_betta
        print('HL betas: ', hidden_layer_betas)

        delta_output_layer_weights = np.zeros((self.num_hidden, self.num_outputs))
        delta_output_biases = np.zeros((self.num_outputs))
        for j, dowlist in enumerate(delta_output_layer_weights):
            for k, dow in enumerate(dowlist):
                delta_output_layer_weights[j][k]= self.learning_rate*hidden_layer_outputs[j]*output_layer_outputs[k]*(1-output_layer_outputs[k])*output_layer_betas[k]
                delta_output_biases[k] = self.learning_rate*output_layer_outputs[k]*(1-output_layer_outputs[k])*output_layer_betas[k]
        
        delta_hidden_layer_weights = np.zeros((self.num_inputs, self.num_hidden))
        delta_hidden_biases = np.zeros((self.num_hidden))
        for i , dhwlist in enumerate(delta_hidden_layer_weights):
            for j, dhw in enumerate(dhwlist):
                delta_hidden_layer_weights[i][j] = self.learning_rate*inputs[i]*hidden_layer_outputs[j]*(1-hidden_layer_outputs[j]) *hidden_layer_betas[j]
                delta_hidden_biases[j] = self.learning_rate*hidden_layer_outputs[j]*(1-hidden_layer_outputs[j]) *hidden_layer_betas[j]
        return delta_output_layer_weights, delta_hidden_layer_weights, delta_output_biases, delta_hidden_biases

    def update_weights(self, delta_output_layer_weights, delta_hidden_layer_weights, delta_output_biases, delta_hidden_biases):

        self.hidden_layer_weights += delta_hidden_layer_weights
        self.output_layer_weights += delta_output_layer_weights
        self.hidden_biases +=delta_hidden_biases
        self.output_biases +=delta_output_biases

    def predict(self, instances):

        predictions = []
        for instance in instances:
            self.hidden_layer_outputs, self.output_layer_outputs = self.forward_pass(instance)
            predicted_class = np.where(self.output_layer_outputs == np.amax(self.output_layer_outputs))[0]
            predictions.append(predicted_class[0])
        return predictions