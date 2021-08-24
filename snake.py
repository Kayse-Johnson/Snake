from typing import List
import pygame
from pygame import display
from pygame.locals import *
from random import randint
import os

class Snake:
    x_dir : int=1
    y_dir : int=0
    step : float=10
    speed : float=1
    updateCount: int=0

    def __init__(self, surface, length:int=3, radius:int=6) -> None:
        self.surface = surface
        self.length = length
        self.r = radius
        self.x_pos = [256-self.r*2*i for i in range(self.length)]
        self.y_pos = [256 for _ in range(self.length)]
        self.rect = [pygame.draw.circle(self.surface, "Green", (self.x_pos[i],self.y_pos[i]), 1) for i in range(self.length)]
        self.rect[0][2] = self.rect[0][3] = self.r
        self.rect[-1][2] = self.rect[-1][3] = 3
    def __len__(self):
        return self.length
    
    def clear_slate(self,surface):
        self.surface.blit(surface, (0,0))
    
    def draw_snake(self): 
        for i in range(self.length):
            pygame.draw.circle(self.surface, "Green", (self.x_pos[i],self.y_pos[i]), self.r)
        
        return
    def movement(self):
        self.x_pos[0] += self.step*self.speed*self.x_dir
        self.y_pos[0] += self.step*self.speed*self.y_dir
        self.rect[0][0]=self.x_pos[0]
        self.rect[0][1]=self.y_pos[0]

    def adjust_body(self):
        key_input = pygame.key.get_pressed()
        self.updateCount +=1
        if self.updateCount>=2:
            for i in range(self.length-1,0,-1):
                self.x_pos[i] = self.x_pos[i-1] 
                self.y_pos[i] = self.y_pos[i-1]
                self.rect[i][0]=self.x_pos[i]
                self.rect[i][1]=self.y_pos[i]
            self.check_keys(key_input)
            self.movement()
            self.updateCount = 0
            
    def check_borders(self, display_size):
        for i in range(self.length):
            if self.x_pos[i]<self.r:
                self.x_pos[i] = display_size[0]-self.r
            elif self.x_pos[i]>display_size[0]-self.r:
                self.x_pos[i] = self.r
        for i in range(self.length):
            if self.y_pos[i]<self.r:
                self.y_pos[i] = display_size[1]-self.r
            elif self.y_pos[i]>display_size[1]-self.r:
                self.y_pos[i] = self.r
    
    def eat_apple(self):
        self.length += 1
        self.rect[-1][2] = self.rect[-1][3] = 2
        self.rect.append(pygame.draw.circle(self.surface, "Green", (self.x_pos[-1],self.y_pos[-1]), 3))
        self.x_pos.append(self.x_pos[-1])
        self.y_pos.append(self.y_pos[-1])

    def check_keys(self, key_input):
        if key_input[pygame.K_LEFT]:
            if self.x_dir == 1:
                pass
            else:
                self.x_dir = -1
                self.y_dir = 0
        elif key_input[pygame.K_UP]:
            if self.y_dir == 1:
                pass
            else:
                self.y_dir = -1
                self.x_dir = 0
        elif key_input[pygame.K_RIGHT]:
            if self.x_dir == -1:
                pass
            else:
                self.x_dir = 1
                self.y_dir = 0
        elif key_input[pygame.K_DOWN]:
            if self.y_dir == -1:
                pass
            else:
                self.y_dir = 1
                self.x_dir = 0



class Apple:
    colour :str='Red'
    def __init__(self, surface, x_pos:int, y_pos:int, radius :int=7):
        self.x = x_pos
        self.y = y_pos
        self.surface = surface
        self.radius = radius
        self.rect = pygame.draw.circle(self.surface, self.colour, (self.x,self.y), self.radius)

    def draw(self):
        pygame.draw.circle(self.surface, self.colour, (self.x,self.y), self.radius)

    @staticmethod
    def generate_apple(display, display_size, radius):
        x = randint(0+radius, display_size[0]-radius)
        y = randint(0+radius, display_size[1]-radius)
        apple = Apple(display, x, y, radius)
        return apple

def check_snake_apple_collision(snake, apple):
    if snake.rect[0].colliderect(apple.rect):
        snake.eat_apple()
        return (0,1)
    else:
        return (1,0)

def check_snake_self_collision(snake, apple_counter, highscore):
    for rect in snake.rect[1:]:
        if snake.rect[0].colliderect(rect):
            if apple_counter > highscore:
                with open('Snake/save.txt','w') as f:
                    f.write(str(apple_counter))
            main()

def display_message(screen, score_font, win_msg, dimensions, location:str='top'):
    message_surf = score_font.render(win_msg, False,(64,64,64))
    if location is 'top':
        message_rect = message_surf.get_rect(center = (dimensions[0]//2,dimensions[1]//20))
    elif location is 'midtop':
        message_rect = message_surf.get_rect(center = (dimensions[0]//2,dimensions[1]//4))
    else:
        message_rect = message_surf.get_rect(center = (dimensions[0]//2,dimensions[1]//2))
    screen.blit(message_surf, message_rect)


def main():
    pygame.init()
    window_size = (1024,1024)
    display_size = (512,512)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    display = pygame.Surface(display_size)
    blank = pygame.Surface(display_size)
    title_font = pygame.font.Font('Snake/font/ARCADE_N.TTF', 40)
    message_font = pygame.font.Font('Snake/font/ARCADE_N.TTF', 10)
    snake = Snake(display)
    apple_radius = 5
    apple_generated_count = 0
    apple_counter = 0
    game_navigation = 0
    with open('Snake/save.txt','r') as f:
        highscore = int(f.read())

    while True:
        if game_navigation:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
            snake.clear_slate(blank)
            snake.check_borders(display_size)
            if not apple_generated_count:
                apple = Apple.generate_apple(display, display_size, apple_radius)
                apple_generated_count +=1
            apple_tuple = check_snake_apple_collision(snake, apple)
            apple_generated_count = apple_tuple[0]
            apple_counter += apple_tuple[1]
            if apple:
                apple.draw()
            check_snake_self_collision(snake, apple_counter, highscore)
            snake.draw_snake()
            snake.adjust_body()
            display_message(display, title_font, str(apple_counter), display_size)
            screen.blit(pygame.transform.scale(display,window_size),(0,0))
            pygame.display.update()
            clock.tick(30)
        else:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                        if event.key == pygame.K_SPACE:
                            game_navigation = 1
            display_message(display, title_font, 'SNAKE', display_size, 'midtop')
            display_message(display, message_font, f'The highscore is {highscore}', display_size, 'center')
            screen.blit(pygame.transform.scale(display,window_size),(0,0))
            pygame.display.update()
            clock.tick(30)
    return

if __name__=="__main__":
    main()

