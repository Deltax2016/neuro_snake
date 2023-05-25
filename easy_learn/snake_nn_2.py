import numpy as np

class SnakeNN:
    def __init__(self, input_dim=(7, 7), hidden_dim=100, output_dim=4, learning_rate=0.001):
        self.input_dim = input_dim
        self.weights_input = np.random.randn(np.prod(input_dim), hidden_dim)
        self.weights_hidden = np.random.randn(hidden_dim, output_dim)
        self.bias_input = np.random.randn(1, hidden_dim)
        self.bias_hidden = np.random.randn(1, output_dim)
        self.learning_rate = learning_rate

    def set_weights(self, weights_input, bias_input, weights_hidden, bias_hidden):
        self.weights_input = weights_input
        self.weights_hidden = weights_hidden
        self.bias_input = bias_input
        self.bias_hidden = bias_hidden

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
        return e_x / (e_x.sum(axis=0) + 1e-10)

    def predict(self, x):
        x = x.reshape(-1, np.prod(self.input_dim))
        layer0 = x @ self.weights_input + self.bias_input
        layer1 = self.relu(layer0)
        layer = layer1 @ self.weights_hidden + self.bias_hidden
        layer2 = self.softmax(layer)
        return layer2
    
    def train(self, x, y):
        # forward propagation
        x = x.reshape(-1, np.prod(self.input_dim))
        layer0 = x @ self.weights_input + self.bias_input
        layer1 = self.tanh(layer0)
        layer = layer1 @ self.weights_hidden + self.bias_hidden
        layer2 = self.softmax(layer)

        # back propagation
        layer2_error = layer2 - y
        layer2_delta = layer1.T @ layer2_error

        layer1_error = layer2_error @ self.weights_hidden.T
        layer1_delta = layer1_error * self.tanh_derivative(layer0)
        layer0_delta = x.T @ layer1_delta

        d_bias_hidden = np.sum(layer2_error, axis=0, keepdims=True)
        d_bias_input = np.sum(layer1_delta, axis=0)

        # update weights
        self.weights_input -= self.learning_rate * layer0_delta
        self.weights_hidden -= self.learning_rate * layer2_delta
        self.bias_input -= self.learning_rate * d_bias_input
        self.bias_hidden -= self.learning_rate * d_bias_hidden

        return layer2




# # initialize snake neural network
# snake_nn = SnakeNN()