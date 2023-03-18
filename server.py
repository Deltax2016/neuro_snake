import math
import random
import pygame
import sys
import time
from population import Population, PopulationOneLayer
    
class Grid:

    def __init__(self, width, height, id):
        self.width = width
        self.height = height
        self.map = [[" " for i in range(width)] for j in range(height)]
        self.id = id
        
    def spawn_food(self, count=1):

        for i in range(count):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            while self.map[y][x] != " ":
                x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            self.map[y][x] = "f"
    

class GameEngine:
    def __init__(self, width, height, size, load=False, result_file=None):
        self.width = width
        self.height = height
        self.size = size
        self.grids = []
        if load:
            self.population = PopulationOneLayer(load=True,path="./results/results_1679173828.txt", gen=0, res_file=result_file)
            self.population.create_from_saved(size)
        else:
            self.population = PopulationOneLayer(res_file=result_file)
            self.population.create_population(size)

    def run(self):

        for i in range(self.size):
            self.grids.append(Grid(self.width, self.height, i))
            self.grids[i].spawn_food()

        while True:
            self.grids, res = self.population.update(self.grids)

            if res:
                self.grids = []
                for i in range(self.size):
                    self.grids.append(Grid(self.width, self.height, i))
                    self.grids[i].spawn_food(count=14)

                if self.population.gen % 50 == 0:
                    print(f"Generation: {self.population.gen}, Best score: {self.population.total_best_score}")

if __name__ == "__main__":
    # now is timestamp in seconds
    now = int(time.time())
    result_file = f"./results/results_{now}.txt"
    with open(result_file, "w") as f:
        f.write("{}")
    
    game = GameEngine(30, 30, 30, result_file = result_file)
    game.run()