import random
import math


def sum_in_range(state,value):
    if state + value < -1:
        return 0
    elif state + value > 1:
        return 1
    else:
        return state + value

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
        self.mutation_rate = 0.1

    def relu(self, x):
        return max(0, x)

    def softmax(self, input):
        return [math.exp(x) / sum([math.exp(x) for x in input]) for x in input]

    def tanh(self, x):
        return math.tanh(x)
    
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
                self.hidden_nodes_1[i][j] = self.tanh(sum([self.input_nodes[i][k] * self.weights_ih[k][j] for k in range(self.input_size)]))
        for i in range(self.hidden_size):
            for j in range(self.hidden_size):
                self.hidden_nodes_2[i][j] = self.relu(sum([self.hidden_nodes_1[i][k] * self.weights_hh[k][j] for k in range(self.hidden_size)]))
        # weights ho is 4x9
        # hidden nodes 2 is 9x1
        hn_to_vector = [self.hidden_nodes_2[i][j] for i in range(self.hidden_size) for j in range(self.hidden_size)]
        #print(hn_to_vector)
        self.output_nodes = self.softmax([sum([hn_to_vector[i] * self.weights_ho[i][j] for i in range(self.hidden_size**2)]) for j in range(4)])

        # use argmax to get the index of the highest value in the output_nodes list
        return self.output_nodes.index(max(self.output_nodes))

    def mutate(self):
        for i in range(self.input_size):
            for j in range(self.hidden_size):
                if random.random() < self.mutation_rate:
                    #self.weights_ih[i][j] = sum_in_range(self.weights_ih[i][j], random.uniform(-0.1, 0.1))
                    self.weights_ih[i][j] = random.random()
        
        for i in range(self.hidden_size):
            for j in range(self.hidden_size):
                if random.random() < self.mutation_rate:
                    #self.weights_hh[i][j] = sum_in_range(self.weights_hh[i][j], random.uniform(-0.1, 0.1))
                    self.weights_hh[i][j] = random.random()
        
        for i in range(self.hidden_size):
            for j in range(4):
                if random.random() < self.mutation_rate:
                    #self.weights_ho[i][j] = sum_in_range(self.weights_ho[i][j], random.uniform(-0.1, 0.1))
                    self.weights_ho[i][j] = random.random()


class Snake:

    def __init__(self, nn, id):
        self.nn = nn
        self.x = 10
        self.y = 10
        self.direction = 0
        self.body = []
        self.alive = True
        self.fitness = 0
        self.score = 0.0
        self.world_size = 100
        self.age = 0
        self.id = id
        self.feeded = False
        self.visited = []
    
    def update(self, grid):

        inputs = []
        cnt = 0
        for i in range(-2, 3):
            inputs.append([])
            for j in range(-2, 3):
                if self.x + i < 0 or self.x + i >= grid.width or self.y + j < 0 or self.y + j >= grid.height:
                    inputs[cnt].append(-1)
                elif [self.x + i, self.y + j] in self.body:
                    inputs[cnt].append(-1)
                elif grid.map[self.y + j][self.x + i] == "f":
                    inputs[cnt].append(0.5)
                else:
                    inputs[cnt].append(0)
        
            cnt += 1

        try:
            if grid.map[self.y][self.x] == "f":
                self.score += 16
                self.fitness += 1
                self.feeded = True
                grid.map[self.y][self.x] = " "
                grid.spawn_food()
        except Exception as e:
            print(f'Exception: {e}')
            print(f'x: {self.x}, y: {self.y}')
        
        self.direction = self.nn.feedforward(inputs)
        self.body.append((self.x, self.y))
        if self.direction == 0:
            self.y -= 1
            if self.y <= 0:
                self.alive = False
        elif self.direction == 1:
            self.x += 1
            if self.x >= grid.width:
                self.alive = False
        elif self.direction == 2:
            self.y += 1
            if self.y >= grid.height:
                self.alive = False
        elif self.direction == 3:
            self.x -= 1
            if self.x <= 0:
                self.alive = False
    
        if [self.x, self.y] in self.body:
            self.alive = False
        elif self.age >= 100:
            self.alive = False

        if self.alive:
            # if the snake is alive, remove the first element of the body
            if self.feeded == False:
                self.body.pop(0)
            else:
                self.feeded = False

            if [self.x, self.y] not in self.visited:
                self.visited.append([self.x, self.y])
                self.score += 1
            else:
                self.score += 0.1
            self.age += 1

        return grid
    
    def reset(self):
        self.x = 10
        self.y = 10
        self.direction = 0
        self.body = []
        self.alive = True
        self.fitness = 0
        self.score = 0
        self.age = 0