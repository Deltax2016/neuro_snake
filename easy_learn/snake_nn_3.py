import numpy as np

import numpy as np

class SnakeNN:
    def __init__(self, input_dim=(7, 7), hidden_dim=100, output_dim=4, learning_rate=0.01, dropout_rate=0.5):
        self.input_dim = input_dim
        self.weights_input = np.random.randn(np.prod(input_dim), hidden_dim)
        self.weights_hidden1 = np.random.randn(hidden_dim, hidden_dim)
        self.weights_hidden2 = np.random.randn(hidden_dim, hidden_dim)
        self.weights_output = np.random.randn(hidden_dim, output_dim)
        self.bias_input = np.random.randn(1, hidden_dim)
        self.bias_hidden1 = np.random.randn(1, hidden_dim)
        self.bias_hidden2 = np.random.randn(1, hidden_dim)
        self.bias_output = np.random.randn(1, output_dim)
        self.learning_rate = learning_rate
        self.dropout_rate = dropout_rate
        self.scale = np.sqrt(1. - dropout_rate)

    def set_weights(self, weights_input, bias_input, weights_hidden1, bias_hidden1, weights_hidden2, bias_hidden2, weights_output, bias_output):
        self.weights_input = weights_input
        self.weights_hidden1 = weights_hidden1
        self.weights_hidden2 = weights_hidden2
        self.weights_output = weights_output
        self.bias_input = bias_input
        self.bias_hidden1 = bias_hidden1
        self.bias_hidden2 = bias_hidden2
        self.bias_output = bias_output


    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def tanh(self, x):
        return np.tanh(x)

    def tanh_derivative(self, x):
        return 1 - np.tanh(x) ** 2
    

    def relu(self, x):
        return np.maximum(0, x)

    def relu_derivative(self, x):
        return np.where(x <= 0, 0, 1)

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / (e_x.sum(axis=1) + 1e-10)

    def dropout(self, x):
        mask = (np.random.rand(*x.shape) < self.dropout_rate) / self.scale
        return x * mask

    def predict(self, x):
        x = x.reshape(-1, np.prod(self.input_dim))
        layer0 = x @ self.weights_input + self.bias_input
        layer1 = self.tanh(layer0)
        layer1 = self.dropout(layer1)
        layer2 = layer1 @ self.weights_hidden1 + self.bias_hidden1
        layer2 = self.tanh(layer2)
        layer2 = self.dropout(layer2)
        layer3 = layer2 @ self.weights_hidden2 + self.bias_hidden2
        layer3 = self.tanh(layer3)
        layer3 = self.dropout(layer3)
        layer4 = layer3 @ self.weights_output + self.bias_output
        output = self.softmax(layer4)
        return output

    def train(self, x, y):
        # forward propagation
        x = x.reshape(-1, np.prod(self.input_dim))
        layer0 = x @ self.weights_input + self.bias_input
        layer1 = self.tanh(layer0)
        layer1_drop = self.dropout(layer1)
        layer2 = layer1_drop @ self.weights_hidden1 + self.bias_hidden1
        layer2_act = self.tanh(layer2)
        layer2_drop = self.dropout(layer2_act)
        layer3 = layer2_drop @ self.weights_hidden2 + self.bias_hidden2
        layer3_act = self.tanh(layer3)
        layer3_drop = self.dropout(layer3_act)
        layer4 = layer3_drop @ self.weights_output + self.bias_output
        output = self.softmax(layer4)

        # back propagation
        output_error = output - y
        output_delta = layer3_act.T @ output_error

        layer3_error = output_error @ self.weights_output.T
        layer3_delta = layer3_error * self.tanh_derivative(layer3)
        layer2_delta = layer2_act.T @ layer3_delta

        layer2_error = layer3_delta @ self.weights_hidden2.T
        layer1_delta = layer2_error * self.tanh_derivative(layer2)
        layer0_delta = x.T @ layer1_delta

        d_bias_output = np.sum(output_error, axis=0, keepdims=True)
        d_bias_hidden2 = np.sum(layer3_delta, axis=0)
        d_bias_hidden1 = np.sum(layer2_delta, axis=0)
        d_bias_input = np.sum(layer1_delta, axis=0)

        # update weights
        self.weights_input -= self.learning_rate * layer0_delta
        self.weights_hidden1 -= self.learning_rate * layer1_delta
        self.weights_hidden2 -= self.learning_rate * layer2_delta
        self.weights_output -= self.learning_rate * output_delta
        self.bias_input -= self.learning_rate * d_bias_input
        self.bias_hidden1 -= self.learning_rate * d_bias_hidden1
        self.bias_hidden2 -= self.learning_rate * d_bias_hidden2
        self.bias_output -= self.learning_rate * d_bias_output

        return output

