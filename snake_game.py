import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('Poppins-Medium.ttf', 24)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
white = (250, 245, 225)
red = (200,0,10)
blue = (0, 100, 250)
black = (5,10,15)

block_size = 20

class SnakeGame:
    
    def __init__(self, w=1280, h=800):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x - block_size, self.head.y),
                      Point(self.head.x - (2 * block_size), self.head.y)]
        
        self.score = 0
        self.speed = 5
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint(0, (self.w - block_size) // block_size) * block_size 
        y = random.randint(0, (self.h - block_size) // block_size) * block_size
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += block_size
        elif direction == Direction.LEFT:
            x -= block_size
        elif direction == Direction.DOWN:
            y += block_size
        elif direction == Direction.UP:
            y -= block_size
            
        self.head = Point(x, y)

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - block_size or self.head.x < 0 or self.head.y > self.h - block_size or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False

    def _update_ui(self):
        self.display.fill(black)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, blue, pygame.Rect(pt.x, pt.y, block_size, block_size))
            pygame.draw.rect(self.display, white, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, red, pygame.Rect(self.food.x, self.food.y, block_size, block_size))
        
        text = font.render("Score: " + str(self.score), True, white)
        self.display.blit(text, [20, 20])
        pygame.display.flip()

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self.speed += .6
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(self.speed)
        # 6. return game over and score
        return game_over, self.score
        
            
if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
        
        
    pygame.quit()