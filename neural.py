import math
import random
import pygame
import sys
import time
from population import Population, PopulationOneLayer

result_file = "result.txt"
    
class Grid:

    def __init__(self, width, height, id):
        self.box = 8
        self.width = width
        self.height = height
        self.map = [[" " for i in range(width)] for j in range(height)]
        self.id = id
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()
        
    def spawn_food(self):
        x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        while self.map[y][x] != " ":
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        self.map[y][x] = "f"
    
    # draw the grid where there are 6x4 grids on the screen, if id == 0 x and y offset equals 0
    # each grid is width * height * box pixels
    # each grid should have borders 8 pixels wide and 1 px grid lines
    def draw(self, snake, screen):
        x_offset = self.width * self.box * (self.id%6) + 8
        y_offset = self.height * self.box * (int(self.id/6)) + 8

        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] == "f":
                    pygame.draw.rect(screen, (0, 255, 0), (x_offset + j * self.box, y_offset + i * self.box, self.box, self.box))
                elif self.map[i][j] == " ":
                    pygame.draw.rect(screen, (255, 255, 255), (x_offset + j * self.box, y_offset + i * self.box, self.box, self.box))
                else:
                    pygame.draw.rect(screen, (255, 0, 0), (x_offset + j * self.box, y_offset + i * self.box, self.box, self.box))
        
        for i in range(self.height + 1):
            pygame.draw.rect(screen, (0,0,0), (x_offset, y_offset + i * self.box, self.width * self.box, 1))
        for i in range(self.width + 1):
            pygame.draw.rect(screen, (0,0,0), (x_offset + i * self.box, y_offset, 1, self.height * self.box))
        
        # draw the snake, head (snake.x, snake.y) is red, each body part is blue
        pygame.draw.rect(screen, (255, 0, 0), (x_offset + snake.x * self.box, y_offset + snake.y * self.box, self.box, self.box))
        for i in range(len(snake.body)):
            pygame.draw.rect(screen, (0, 0, 255), (x_offset + snake.body[i][0] * self.box, y_offset + snake.body[i][1] * self.box, self.box, self.box))

        pygame.draw.rect(screen, (0,0,0), (x_offset, y_offset, self.width * self.box, self.height * self.box), 8)


class Game:

    def __init__(self, width, height, size, load=False, result_file=None):
        self.width = width
        self.height = height
        self.size = size
        self.grids = []
        if load:
            self.population = PopulationOneLayer(load=True,path="results_1679178498.txt", gen=0, res_file=result_file)
            self.population.create_from_saved(size)
        else:
            self.population = PopulationOneLayer(res_file=result_file)
            self.population.create_population(size)
        
        self.screen = pygame.display.set_mode(((width) * 8 * 6 + 8, height * 8 * 4 + 50))
        self.clock = pygame.time.Clock()
    
    def run(self):
        for i in range(self.size):
            self.grids.append(Grid(self.width, self.height, i))
            self.grids[i].spawn_food()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill((255,255,255))
            self.grids, res = self.population.update(self.grids)


            if res:
                self.grids = []
                for i in range(self.size):
                    self.grids.append(Grid(self.width, self.height, i))
                    self.grids[i].spawn_food()

            if self.population.gen % 50 == 0:

                for grid in self.grids:
                    grid.draw(self.population.snakes[grid.id], self.screen)
                pygame.font.init()
                # print the generation number and the best snake score
                font = pygame.font.SysFont('comicsansms', 30)
                text = font.render("Generation: " + str(self.population.gen), True, (0, 0, 0))
                self.screen.blit(text, (20, self.height * 8 * 4 + 10))
                text = font.render("Best score: " + str(self.population.total_best_score), True, (0, 0, 0))
                self.screen.blit(text, (300, self.height * 8 * 4 + 10))
                pygame.display.update()
                self.clock.tick(10)

if __name__ == "__main__":
    # now is timestamp in seconds
    now = int(time.time())
    result_file = f"./results/results_{now}.txt"
    with open(result_file, "w") as f:
        f.write("{}")
    game = Game(30, 30, 24,load=True, result_file = result_file)
    game.run()