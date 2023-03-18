from snake import Snake, SnakeNN

class Population:
    def __init__(self, load=False, path=None, gen=0, res_file="./result/result.txt"):
        self.snakes = []
        self.gen = 0
        self.result = res_file
        if load:
            self.best_snake = Snake(SnakeNN(5, 3), 0)
            self.best_snake.nn.weights_ih, self.best_snake.nn.weights_hh, self.best_snake.nn.weights_ho = self.load_best_snake_from_gen(gen,path)
        else:
            self.best_snake = None
        self.best_score = 0.0
        self.total_best_score = 0.0

    def create_population(self, size):
        for i in range(size):
            self.snakes.append(Snake(SnakeNN(5, 3), i))
            self.snakes[i].nn.preparation()

        print('Population created')

    def create_from_saved(self, size):
        self.create_population(size)
        for i in range(len(self.snakes)):
                self.snakes[i].reset()
                self.snakes[i].nn.weights_ih, self.snakes[i].nn.weights_hh, self.snakes[i].nn.weights_ho = self.best_snake.nn.weights_ih, self.best_snake.nn.weights_hh, self.best_snake.nn.weights_ho
                if i != 0: self.snakes[i].nn.mutate()
        print('Population copied')

    def find_best_snake(self):
        for snake in self.snakes:
            if snake.score > self.total_best_score:
                self.total_best_score = snake.score
                self.best_snake = snake
        print(f"Best score: {self.total_best_score}, Generation: {self.gen}")

    def update(self, grids):

        for snake in self.snakes:
            if snake.alive:
                grid = snake.update(grids[snake.id])
                grids[snake.id] = grid
            else:
                #reset grid
                grids[snake.id].map = [[" " for i in range(grids[snake.id].width)] for j in range(grids[snake.id].height)]
                
        restart = False
        # if no one is alive, then the generation is over
        if not any([snake.alive for snake in self.snakes]):
            self.gen += 1
            self.find_best_snake()

            for i in range(len(self.snakes)):
                self.snakes[i].reset()
                self.snakes[i].nn.weights_ih, self.snakes[i].nn.weights_hh, self.snakes[i].nn.weights_ho = self.best_snake.nn.weights_ih, self.best_snake.nn.weights_hh, self.best_snake.nn.weights_ho
                if i > 6: self.snakes[i].nn.mutate()
                grids[self.snakes[i].id] = []
            self.save_best_snake()
            restart = True
            self.best_score = 0
    
        
        return grids, restart
    
    # save the best snake of the generation to the file with a dict (where the key is the generation number and the value is weights of the snake)

    def save_best_snake(self):
        f = open(self.result, "r")
        data = eval(f.read())
        f.close()

        '''
        if self.gen not in data:
            data[self.gen] = (self.best_snake.nn.weights_ih, self.best_snake.nn.weights_hh, self.best_snake.nn.weights_ho)
            with open(result_file, "w") as f:
                f.write(str(data))
        '''

        data[0] = (self.best_snake.nn.weights_ih, self.best_snake.nn.weights_hh, self.best_snake.nn.weights_ho)
        with open(self.result, "w") as f:
                f.write(str(data))
    
    def load_best_snake(self):
        f = open(self.result, "r")
        data = eval(f.read())
        f.close()

        return data[max(data.keys())]
    
    def load_best_snake_from_gen(self, gen, file):
        f = open(file, "r")
        data = eval(f.read())
        f.close()

        return data[gen]