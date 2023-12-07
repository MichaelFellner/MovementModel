

# Set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
import pygame
import numpy as np
import random
import sys
import time
class Game:
    def __init__(self,user_control = False, render = False, action_list = None):

        pygame.init()
        # Initialize other game components here (like screen, square_rect, platforms, etc.)
        # Set the size of the window and some basic parameters
        self.action_list = action_list
        self.size = self.width, self.height = 640, 480
        self.speed = [0, 0]
        self.gravity = 0.5
        self.user_control = user_control
        #if not self.user_control:
        #    os.environ["SDL_VIDEODRIVER"] = "dummy"

        # Colors
        self.black = (0, 0, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)
        self.gold = (255, 215, 0)  # Color for the goal

        # Create a window
        self.screen = pygame.display.set_mode(self.size)

        # Set the title of the window
        pygame.display.set_caption('Pygame Ball Rolling Example')

        # Load an image (square)
        self.square = pygame.Surface((50, 50))
        self.square.fill(self.red)
        self.square_rect = self.square.get_rect()
        #print(square_rect)
        # Define platforms as a list of rectangles
        self.platforms = [
            pygame.Rect(0, self.height - 20, self.width, 20),  # Add ground platform
            pygame.Rect(self.height, 300, 200, 20), #x of top left, y of top left, width, height
            pygame.Rect(350, 200, 150, 20),
            pygame.Rect(200, 100, 200, 20)
            #pygame.Rect(0,0,20,height),
            #pygame.Rect(width-20,0,20,height),
            #pygame.Rect(0,0,width,20),

        ]
        self.goal = pygame.Rect(self.platforms[-1].centerx - 25, self.platforms[-1].y - 50, 50, 50)
        self.ground_platform_top = self.platforms[0].top  # The top of the ground platform
        self.square_rect = self.square.get_rect(midbottom=(self.width // 2, self.ground_platform_top))
        self.init_state = self.square_rect.x , self.square_rect.y
        
    def sample(self):
        x_scale = (np.random.rand()+1)*20
        y_scale = (np.random.rand()+1) * 10
        x = np.random.rand() * random.sample([-1,1],1)[0] * x_scale
        y = np.random.rand() * random.sample([-1,1],1)[0] * y_scale
        return [x,y]
        
    def reset(self):
        self.speed = [0, 0]
        self.gravity = 0.5
        self.square_rect.x = self.init_state[0]
        self.square_rect.y = self.init_state[1]
        #print(self.square_rect.x, self.square_rect.y)
        return (self.square_rect.x, self.square_rect.y)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def action_sample(self):
        x_scale = (np.random.rand()+1)*20
        y_scale = (np.random.rand()+1) * 10
        x = np.random.rand() * random.sample([-1,1],1)[0] * x_scale
        y = np.random.rand() * random.sample([-1,1],1)[0] * y_scale
        return [x,y]

    def update_game_state(self,action):
        # Sample code from your script
        curr_state = [self.square_rect.x, self.square_rect.y]
        #print(curr_state)
        #samp = sample()

        if self.user_control:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.square_rect.x -= 2
            if keys[pygame.K_RIGHT]:
                self.square_rect.x += 2
        else:
            self.square_rect.x += action[0]

        if self.square_rect.left < 0:
            self.square_rect.left = 0
        if self.square_rect.right > self.width:
            self.square_rect.right = self.width

        self.speed[1] += self.gravity
        on_ground = False

        for platform in self.platforms:
            next_rect = self.square_rect.move(self.speed)
            if next_rect.colliderect(platform):
                    # Check if falling (i.e., moving downwards)
                    if self.speed[1] > 0 and next_rect.bottom > platform.top:
                        # Place the square on top of the platform
                        self.square_rect.bottom = platform.top
                        self.speed[1] = 0
                        on_ground = True
                        break  # No need to check other platforms
                    # Check if moving upwards and collides with the bottom of the platform
                    elif self.speed[1] < 0 and next_rect.top < platform.bottom:
                        # Place the square just below the platform
                        self.square_rect.top = platform.bottom
                        self.speed[1] = 0
                        break  # No need to check other platforms            # Rest of your collision and platform logic...

        if not on_ground:
            self.square_rect.y += int(self.speed[1])

        if self.user_control and on_ground and keys[pygame.K_SPACE]:
            self.speed[1] -= 20
        elif not self.user_control and on_ground:
            self.speed[1] = -action[1]
        
        #If goal
        done = False
        if self.square_rect.colliderect(self.goal):
            self.running = False
            done = True

        next_state = [self.square_rect.x, self.square_rect.y]
        distance = (self.square_rect.x - self.goal.x) ** 2 + (self.square_rect.y - self.goal.y) ** 2
        #print(distance)
        #print(curr_state, next_state)
        #time.sleep(0.2)
        reward = -distance
        return next_state, reward, done

    def render(self):
        self.screen.fill(self.blue)
        for p in self.platforms:
            pygame.draw.rect(self.screen, self.green, p)
        pygame.draw.rect(self.screen, self.gold, self.goal)
        self.screen.blit(self.square, self.square_rect)
        pygame.display.flip()

    def step(self,action):
        running = self.handle_events()
        if not running:
            return False

        next_state, reward, done = self.update_game_state(action)
        
        if self.user_control or self.render:
            self.render()

        pygame.time.Clock().tick(60)
        return next_state,reward,done

    def run(self):
        self.running = True
        while self.running:
            self.running = self.step(self.sample())
            if self.running[2]: #if done
                break
        pygame.quit()
        sys.exit()
        
    def showcase(self):
        for i in self.action_list:
            self.step(i)
        pygame.quit()
        sys.exit()
        
