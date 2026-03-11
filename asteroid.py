import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH
from constants import ASTEROID_MIN_RADIUS
from logger import log_event
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
        self.velocity = pygame.Vector2(0, 0)   
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        new_vector1 = self.velocity.rotate(angle)
        new_vector2 = self.velocity.rotate(-angle) 
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        child1 = Asteroid(self.position.x, self.position.y, new_radius)
        child1.velocity = new_vector1 * 1.2
        child2 = Asteroid(self.position.x, self.position.y, new_radius)
        child2.velocity = new_vector2 * 1.2

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH
        )
    
    def update(self, dt):
        self.position += (self.velocity * dt)
