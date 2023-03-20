import math
import random
import pygame
import sys
import time
from snake import Snake

result_file = "result.txt"
    
class World:

    def __init__(self, width, height):
        self.box = 10
        self.width = width
        self.height = height
        self.map = [[" " for i in range(width)] for j in range(height)]
        
    def spawn_food(self, count=1):

        for i in range(count):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            while self.map[y][x] != " ":
                x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            self.map[y][x] = "f"

    def update(self, snake):
        if self.map[snake.y][snake.x] == "f":
            snake.eat()
            self.map[snake.y][snake.x] = " "
            self.spawn_food()
        elif self.map[snake.y][snake.x] == " ":
            snake.move()
        else:
            snake.die()
            return False
        return True
    
    # draw the grid where width * height * box pixels, with lines 1 px wide
    # food is green, snake head is red, snake body is blue, empty is white
    # draw red lines near the snake head for y-2, y+2, x-2, x+2
    # draw world borders self.box 
    def draw(self, snake, screen):
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] == "f":
                    pygame.draw.rect(screen, (0, 255, 0), (j * self.box, i * self.box, self.box, self.box))
                elif self.map[i][j] == " ":
                    pygame.draw.rect(screen, (255, 255, 255), (j * self.box, i * self.box, self.box, self.box))
                else:
                    pygame.draw.rect(screen, (255, 0, 0), (j * self.box, i * self.box, self.box, self.box))
        # draw world borders
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, self.box, self.height * self.box))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, self.width * self.box, self.box))
        pygame.draw.rect(screen, (0, 0, 0), (0, (self.height - 1) * self.box, self.width * self.box, self.box))
        pygame.draw.rect(screen, (0, 0, 0), ((self.width - 1) * self.box, 0, self.box, self.height * self.box))

        
        # draw red lines near the snake head for y-2, y+2, x-2, x+2
        pygame.draw.rect(screen, (255, 0, 0), ((snake.x - 2) * self.box, (snake.y - 2) * self.box, self.box, self.box))
        pygame.draw.rect(screen, (255, 0, 0), ((snake.x - 2) * self.box, (snake.y + 2) * self.box, self.box, self.box))
        pygame.draw.rect(screen, (255, 0, 0), ((snake.x - 2) * self.box, (snake.y - 2) * self.box, self.box, self.box))
        pygame.draw.rect(screen, (255, 0, 0), ((snake.x + 2) * self.box, (snake.y - 2) * self.box, self.box, self.box))

    # draw a mini grid of 5x5 with the snake head in the middle at the right side of the screen
    def draw_mini_grid(self, snake, screen):
        inpt = self.get_inputs(snake)

        pygame.draw.rect(screen, (0, 0, 0), (self.width * self.box, 0, 200, self.height * self.box))
        for i in range(5):
            for j in range(5):
                if inpt[i][j] == "f":
                    pygame.draw.rect(screen, (0, 255, 0), (self.width * self.box + j * self.box, i * self.box, self.box, self.box))
                elif inpt[i][j] == " ":
                    pygame.draw.rect(screen, (255, 255, 255), (self.width * self.box + j * self.box, i * self.box, self.box, self.box))
                elif inpt[i][j] in snake.body:
                    pygame.draw.rect(screen, (0, 0, 255), (self.width * self.box + j * self.box, i * self.box, self.box, self.box))
                elif inpt[i][j] == snake.head:
                    pygame.draw.rect(screen, (255, 0, 0), (self.width * self.box + j * self.box, i * self.box, self.box, self.box))
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (self.width * self.box + j * self.box, i * self.box, self.box, self.box))

    # return a 5x5 grid with the snake head in the middle
    def get_inputs(self, snake):
        inputs = [[" " for i in range(5)] for j in range(5)]
        for i in range(5):
            for j in range(5):
                if snake.x - 2 + j < 0 or snake.x - 2 + j >= self.width or snake.y - 2 + i < 0 or snake.y - 2 + i >= self.height:
                    inputs[i][j] = "w"
                else:
                    inputs[i][j] = self.map[snake.y - 2 + i][snake.x - 2 + j]
        return inputs
    
    def display_direction(self, direction):
        # display up, down, left, right
        # boxes are white with black borders, but the direction is red
        # display up, down, left, right

        pygame.draw.rect(self.screen, (255, 255, 255) if direction!=0 else (255,0,0), (self.width * 10 + 60, self.height * 10 - 100, 50, 50), 2)
        pygame.draw.rect(self.screen, (255, 255, 255) if direction!=1 else (255,0,0), (self.width * 10 + 10, self.height * 10 - 150, 50, 50), 2)
        pygame.draw.rect(self.screen, (255, 255, 255) if direction!=2 else (255,0,0), (self.width * 10 + 130, self.height * 10 - 150, 50, 50), 2)
        pygame.draw.rect(self.screen, (255, 255, 255) if direction!=3 else (255,0,0), (self.width * 10 + 60, self.height * 10 - 200, 50, 50), 2)

        


class Game:

    def __init__(self, width, height, size, load=False, result_file=None):
        self.width = width
        self.height = height
        self.size = size
        self.snake = None
        self.world = World(width, height)
        self.last_direction = [0,0,0,0][random.randint(0,3)] = 1
        
        # create world on the right side of the screen
        # also create a mini grid on the left side of the screen
        # under the mini grid, display the score
        # under the score, display 4 boxes: up, down, left, right with the corresponding arrow, white but with black border
        
        self.screen = pygame.display.set_mode((width * 10 + 200, height * 10))
        self.clock = pygame.time.Clock()
    
    def run(self):
        
        # display world
        self.world.draw(self.snake, self.screen)
        self.world.spawn_food(30)
        # create snake 
        self.snake = Snake()
        # display mini grid
        self.world.draw_mini_grid(self.snake, self.screen)

        self.last_direction = self.snake.feedforward(self.world.get_inputs(self.snake))
        self.world.display_direction(self.last_direction)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # inputs is 5x5 grid with the snake head in the middle
                    inputs = self.world.get_inputs(self.snake)

                    # wasd
                    if event.key == pygame.K_W:
                        self.snake.update(inputs, [1, 0, 0, 0])
                    if event.key == pygame.K_S:
                        self.snake.update(inputs, [0, 0, 1, 0])
                    if event.key == pygame.K_A:
                        self.snake.update(inputs, [0, 0, 0, 1])
                    if event.key == pygame.K_D:
                        self.snake.update(inputs, [0, 1, 0, 0])
            
                    # update world
                    self.world.update(self.snake)
                    # display world
                    self.world.draw(self.snake, self.screen)
                    self.last_direction = self.snake.feedforward(self.world.get_inputs(self.snake))

                    # display mini grid
                    self.world.draw_mini_grid(self.snake, self.screen)
                    self.world.display_direction(self.last_direction)
                    # display score
                    font = pygame.font.SysFont("comicsansms", 30)
                    text = font.render(f"Score: {self.snake.score}", True, (0, 0, 0))
                    self.screen.blit(text, (self.width * 10 + 10, self.height * 10 - 50))

                    self.screen.fill((255,255,255))
                    pygame.display.update()
            self.clock.tick(30)

if __name__ == "__main__":
    # now is timestamp in seconds
    now = int(time.time())
    result_file = f"./results/results_{now}.txt"
    with open(result_file, "w") as f:
        f.write("{}")
    game = Game(80, 80, result_file = result_file)
    game.run()