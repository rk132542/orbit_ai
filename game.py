import pygame
import numpy as np


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)

    def display_board(self, window):
        for obj in self.objects:
            obj.display(window)


max_fire_particle_num = 30


class GameObject:
    def __init__(self, x, y, width, height, angle=0, velocity=None, acceleration=None, mass=1):
        self.position = np.array([x, y])
        self.width = width
        self.height = height
        self.angle = angle
        self.mass = mass
        self.level = 0
        self.rect = pygame.Rect(0, 0, 0, 0)

        if velocity is None:
            self.velocity = np.array([0.0, 0.0])
        else:
            self.velocity = velocity

        if acceleration is None:
            self.acceleration = np.array([0.0, 0.0])
        else:
            self.acceleration = acceleration

    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

    def apply_force(self, force: np.array):
        self.acceleration += force / self.mass

    def get_corners(self):
        corners = np.array([
            [-self.width / 2, -self.height / 2],  # top-left
            [self.width / 2, -self.height / 2],   # top-right
            [self.width / 2, self.height / 2],    # bottom-right
            [-self.width / 2, self.height / 2]    # bottom-left
        ])

        rotation = np.array([
            [np.cos(self.angle), -np.sin(self.angle)],
            [np.sin(self.angle), np.cos(self.angle)]
        ])

        rotated_corners = []
        for corner in corners:
            rotated_corner = np.dot(rotation, corner) + self.position
            rotated_corners.append(rotated_corner)

        return np.array(rotated_corners)

    def get_particle_center(self):
        x = self.width/2 - 3
        y = self.height
        
        rotation = np.array([
            [np.cos(self.angle), -np.sin(self.angle)],
            [np.sin(self.angle), np.cos(self.angle)]
        ])
        
        return np.dot(rotation, np.array([x, y])) + self.position

    def display(self, window):
        corners = self.get_corners()
        self.rect = pygame.draw.polygon(window, (255, 255, 255), corners)

        particle_center = self.get_particle_center()
        for i in range(int(max_fire_particle_num*self.level)):
            x = np.random.randint(-5, 5)
            y = np.random.randint(-5, 5)
            pygame.draw.circle(window, (255, 0, 0), (int(particle_center[0] + x), int(particle_center[1] + y)), 2)
            

        pygame.display.update()

    def get_rect(self):
        return self.rect
    
    def __str__(self):
        return f"Position: {self.position}, Velocity: {self.velocity}, Acceleration: {self.acceleration}"
