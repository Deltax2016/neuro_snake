# create simple snake game using pygame using only rectangles

import pygame
import random
import time
import sys
import numpy as np
import math

from snake_nn_3 import SnakeNN

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((1200, 600))

# title and icon
pygame.display.set_caption("Snake Game")

# snake class
snake_len = 3
snake_list = [[200, 200], [220, 200], [240, 200]]
food_list = []

# draw screen with grid

def draw_screen():
    for i in range(0, 800, 20):
        pygame.draw.line(screen, (255, 255, 255), (i, 0), (i, 600), 1)
    for i in range(0, 600, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, i), (800, i), 1)

def draw_snake():
    pygame.draw.rect(screen, (255, 0, 0), (snake_list[-1][0], snake_list[-1][1], 20, 20))
    for x in snake_list[:-1]:
        pygame.draw.rect(screen, (255, 255, 255), (x[0], x[1], 20, 20))

def draw_food():
    for x in food_list:
        pygame.draw.rect(screen, (0, 255, 0), (x[0], x[1], 20, 20))

def add_food():
    x = random.randint(0, 39) * 20
    y = random.randint(0, 29) * 20
    if [x, y] not in snake_list and [x, y] not in food_list:
        food_list.append([x, y])

def draw_head(X):
    # draw 5x5 grid at the right side of the screen
    # in this grid, draw the snake's head and 5x5 grid around it
    # this will be the snake's vision
    x, y = snake_list[-1][0], snake_list[-1][1]

    # np array to list
    X = X.tolist()[0]

    size = int(math.sqrt(len(X)))

    # draw grid

    for i in range(size):
        for j in range(size):
            pygame.draw.rect(screen, (255, 255, 255), (840 + 20 * j, 80 + 20 * i, 20, 20), 1)

            if X[i*size+j] == -1:
                pygame.draw.rect(screen, (255, 255, 255), (840 + 20 * j, 80 + 20 * i, 20, 20))
            elif X[i*size+j] == 1:
                pygame.draw.rect(screen, (0, 255, 0), (840 + 20 * j, 80 + 20 * i, 20, 20))
            elif X[i*size+j] == 0.5:
                pygame.draw.rect(screen, (255, 0, 0), (840 + 20 * j, 80 + 20 * i, 20, 20))

nn = SnakeNN()

def get_input():
    inputs = []
    for i in range(-3, 4):
        for j in range(-3, 4):
            x, y = (snake_list[-1][0] + 20 * j) % 800, (snake_list[-1][1] + 20 * i) % 600
            if [x, y] in snake_list:
                if [x, y] == snake_list[-1]:
                    inputs.append(0.5)
                else:
                    inputs.append(-1)
            elif [x, y] in food_list:
                inputs.append(1)
            else:
                inputs.append(0)

    result = np.array([inputs])
    return result

def print_class(y):
    i = np.argmax(y)
    classes = ["left", "right", "up", "down"]
    print(classes[i])

def load_model():
    # def set_weights(self, weights_input, bias_input, weights_hidden1, bias_hidden1, weights_hidden2, bias_hidden2, weights_output, bias_output):
    # loading weight and bias from files npy
    nn.set_weights(np.load("/saved/weights_input.npy"), np.load("/saved/bias_input.npy"), np.load("/saved/weights_hidden1.npy"), np.load("/saved/bias_hidden1.npy"), np.load("/saved/weights_hidden2.npy"), np.load("/saved/bias_hidden2.npy"), np.load("/saved/weights_output.npy"), np.load("/saved/bias_output.npy"))

for i in range(20):
    add_food()

load_model()

direction = "right"
# game loop
running = True

while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    draw_screen()
    draw_snake()
    draw_food()
    X = get_input()
    draw_head(X)
    pygame.display.update()

    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # check for key presses
    keys = pygame.key.get_pressed()

    i = np.argmax(nn.predict(X))
    classes = ["left", "right", "up", "down"]
    print(classes[i])

    if classes[i] == "left":
        if direction != "right":
            direction = "left"
            snake_list.append([snake_list[-1][0] - 20, snake_list[-1][1]])
    elif classes[i] == "right":
        if direction != "left":
            direction = "right"
            snake_list.append([snake_list[-1][0] + 20, snake_list[-1][1]])
    elif classes[i] == "up":
        if direction != "down":
            direction = "up"
            snake_list.append([snake_list[-1][0], snake_list[-1][1] - 20])
    elif classes[i] == "down":
        if direction != "up":
            direction = "down"
            snake_list.append([snake_list[-1][0], snake_list[-1][1] + 20])

    # add food
    if len(food_list) < 20:
        add_food()

    # check if snake is eating food
    for x in food_list:
        if x[0] == snake_list[-1][0] and x[1] == snake_list[-1][1]:
            food_list.remove(x)
            snake_len += 1

    # check if snake is out of bounds
    if snake_list[-1][0] < 0 or snake_list[-1][0] > 780 or snake_list[-1][1] < 0 or snake_list[-1][1] > 580:
        if snake_list[-1][0] < 0:
            snake_list[-1][0] = 780
        elif snake_list[-1][0] > 780:
            snake_list[-1][0] = 0
        elif snake_list[-1][1] < 0:
            snake_list[-1][1] = 580
        elif snake_list[-1][1] > 580:
            snake_list[-1][1] = 0

    # check if snake is eating itself
    for x in snake_list[:-1]:
        if x[0] == snake_list[-1][0] and x[1] == snake_list[-1][1]:
            running = False

    # check if snake is too long
    if len(snake_list) > snake_len:
        snake_list.pop(0)

    # add delay
    time.sleep(0.5)

pygame.quit()