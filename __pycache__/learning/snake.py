import random
import math
import numpy as np

class SnakeNN:
    def __init__(self, input_size, hidden_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.input_nodes = [[0 for i in range(input_size)] for x in range(input_size)]
        self.hidden_nodes_1 = [[0 for i in range(hidden_size)] for x in range(hidden_size)]
        self.hidden_nodes_2 = [[0 for i in range(hidden_size)] for x in range(hidden_size)]
        self.output_nodes = [0,0,0,0]
        self.weights_ih = []
        self.weights_hh = []
        self.weights_ho = []
        self.learning_rate = 0.2

    def relu(self, x):
        return max(0, x)
    
    def d_relu(self, x):
        if x > 0:
            return 1
        else:
            return 0

    def softmax(self, input):
        return [math.exp(x) / sum([math.exp(x) for x in input]) for x in input]
    
    def preparation(self):
        for i in range(self.input_size):
            self.weights_ih.append([])
            for j in range(self.hidden_size):
                self.weights_ih[i].append(random.random())
        
        for i in range(self.hidden_size):
            self.weights_hh.append([])
            for j in range(self.hidden_size):
                self.weights_hh[i].append(random.random())
        
        for i in range(self.hidden_size**2):
            self.weights_ho.append([])
            for j in range(4):
                self.weights_ho[i].append(random.random())   

    def feedforward(self, inputs):
        for i in range(self.input_size):
            for j in range(self.input_size):
                self.input_nodes[i][j] = inputs[i][j]
        for i in range(self.hidden_size):
            for j in range(self.hidden_size):
                self.hidden_nodes_1[i][j] = self.relu(sum([self.input_nodes[i][k] * self.weights_ih[k][j] for k in range(self.input_size)]))
        for i in range(self.hidden_size):
            for j in range(self.hidden_size):
                self.hidden_nodes_2[i][j] = self.relu(sum([self.hidden_nodes_1[i][k] * self.weights_hh[k][j] for k in range(self.hidden_size)]))
        # weights ho is 4x9
        # hidden nodes 2 is 9x1
        hn_to_vector = [self.hidden_nodes_2[i][j] for i in range(self.hidden_size) for j in range(self.hidden_size)]
        #print(hn_to_vector)
        self.output_nodes = self.softmax([sum([hn_to_vector[i] * self.weights_ho[i][j] for i in range(self.hidden_size**2)]) for j in range(4)])

        # use argmax to get the index of the highest value in the output_nodes list
        return self.output_nodes

    def backpropagation(self, inputs, target):

        result = self.feedforward(input)
        print(result)

        # calculate the error
        grad_output = [x - y for x, y in zip(result, target)]

        # δ_hidden2 = (δ_output * W_output.T) * ReLU'(z_hidden2)
        np_grad_output = np.array(grad_output)
        np_weights_ho = np.array(self.weights_ho)

        grad_hidden2 = np.zeros((self.hidden_size, self.hidden_size))

        # creating a 2d array of gradients
        for i in range(self.hidden_size):
            for j in range(self.hidden_size):
                grad_hidden2[i][j] = np.dot(np_grad_output*np_weights_ho.T) * self.d_relu(self.hidden_nodes_2[i][j])

        # δ_hidden1 = (δ_hidden2 * W_hidden2.T) * ReLU'(z_hidden1)

        np_weights_hh = np.array(self.weights_hh)

        grad_hidden1 = np.zeros((self.hidden_size, self.hidden_size))

        # creating a 2d array of gradients
        for i in range(self.hidden_size):
            for j in range(self.hidden_size):
                grad_hidden1[i][j] = np.dot(grad_hidden2*np_weights_hh.T) * self.d_relu(self.hidden_nodes_1[i][j])

        # update the weights
        self.weights_ho += self.learning_rate * np.dot(grad_output, self.hidden_nodes_2.T)

        print(self.weights_ho)
        self.weights_hh += self.learning_rate * np.dot(grad_hidden2, self.hidden_nodes_1.T)
        print(self.weights_hh)

        # update the weights
        self.weights_ih += self.learning_rate * np.dot(grad_hidden1, self.input_nodes.T)
        print(self.weights_ih)

        return result
    
    def save(self, filename):
        with open(filename, 'w') as f:
            data = {}
            data[0] = (self.weights_ih, self.weights_hh, self.weights_ho)
            f.write(str(data))

    def load(self, filename):
        with open(filename, 'r') as f:
            data = eval(f.read())
            self.weights_ih, self.weights_hh, self.weights_ho = data[0]
    

class Snake:

    def __init__(self):
        self.nn = SnakeNN(5, 3)
        self.x = 40
        self.y = 40
        self.direction = random.randint(0, 4)
        self.body = [(self.x, self.y+1), (self.x, self.y + 2), (self.x, self.y + 3)]
        self.alive = True
        self.fitness = 3
        self.score = 0.0
        self.age = 0
        self.world_size = (80, 80)

    def move(self, direction):
        if direction == 0:
            self.x += 1
        elif direction == 1:
            self.x -= 1
        elif direction == 2:
            self.y += 1
        elif direction == 3:
            self.y -= 1
        self.body.insert(0, (self.x, self.y))
        self.body.pop(-1)

    def eat(self):
        self.body.append((self.x, self.y))
        self.fitness += 1

    def good_inputs(self, inputs):

        good_inputs = []
        cnt = 0
        for i in range(0, 5):
            good_inputs.append([])
            for j in range(0, 5):
                if self.x + i < 0 or self.x + i >= self.world_size[0] or self.y + j < 0 or self.y + j >= self.world_size[1]:
                    good_inputs[cnt].append(-1)
                elif [self.x + i, self.y + j] in self.body:
                    good_inputs[cnt].append(-1)
                elif inputs[self.y + j][self.x + i] == "f":
                    good_inputs[cnt].append(0.5)
                else:
                    good_inputs[cnt].append(0)

        return good_inputs
    
    def get_direction(self,inputs):
        # max index of the output nodes
        self.direction = np.argmax(self.nn.feedforward(self.good_inputs(inputs)))
        return self.direction
    



    

    
