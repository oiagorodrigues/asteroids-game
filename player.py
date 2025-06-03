import pygame

from circleshape import CircleShape
from shot import Shot

from constants import (
    PLAYER_RADIUS,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN,
)


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        """ Handle player input for movements """
        # move up with W or UP ARROW
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)

        # move down with S or DOWN ARROW
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)

        # rotate left with A or LEFT ARROW
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)

        # rotate right with D or RIGHT ARROW
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)

        """ Handle player input for shooting """
        if keys[pygame.K_SPACE]:
            self.shoot()

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return
        shoot = Shot(self.position.x, self.position.y)
        shoot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
