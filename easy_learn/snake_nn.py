import numpy as np

class SnakeNN:
    def __init__(self):
        self.weights_input = np.random.randn(49, 100)
        self.weights_hidden = np.random.randn(100, 4)
        self.bias_input = np.random.randn(1,100)
        self.bias_hidden = np.random.randn(1,4)
        self.learning_rate = 0.001

    def set_weights(self, weights_input, bias_input, weights_hidden, bias_hidden):
        self.weights_input = weights_input
        self.weights_hidden = weights_hidden
        self.bias_input = bias_input
        self.bias_hidden = bias_hidden

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def tanh(self, x):
        return np.tanh(x)
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        return np.where(x <= 0, 0, 1)
    
    def tanh_derivative(self, x):
        return 1 - np.tanh(x) ** 2
    
    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / (e_x.sum(axis=0) + 1e-10)

    
    def softmax_derivative(self, x):
        return self.softmax(x) * (1 - self.softmax(x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def predict(self, x):
        layer0 = x @ self.weights_input + self.bias_input
        layer1 = self.relu(layer0)

        #print(layer1)
        layer = layer1 @ self.weights_hidden + self.bias_hidden
        layer2 = self.softmax(layer)
        return layer2
    
    def train(self, x, y):
        # forward propagation

        layer0 = x @ self.weights_input + self.bias_input
        layer1 = self.relu(layer0)

        #print(layer1)
        layer = layer1 @ self.weights_hidden + self.bias_hidden
        layer2 = self.softmax(layer)

        
        #print(layer2)

        # back propagation
        layer2_error = layer2 - y

        print(layer2_error)

        layer2_delta = layer1.T @ layer2_error
        d_bias_hidden = layer2_error
        layer1_error = layer2_error @ self.weights_hidden.T 
        layer1_delta = layer1_error * self.relu_derivative(layer0)

        layer0_delta = x.T @ layer1_delta
        d_bias_input = layer1_delta

        # update weights
        self.weights_input -= self.learning_rate * layer0_delta
        self.weights_hidden -= self.learning_rate * layer2_delta
        self.bias_input = self.bias_input - self.learning_rate * d_bias_input
        self.bias_hidden = self.bias_hidden-  self.learning_rate * d_bias_hidden

        return layer2


# # initialize snake neural network
# snake_nn = SnakeNN()