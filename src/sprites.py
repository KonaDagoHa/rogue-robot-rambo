import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 40))

        self.pos = pygame.Vector2(self.rect.center)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        self.friction = -0.12  # Make sure friction is ALWAYS negative

        self.can_jump = True
        self.last_jump_time = pygame.time.get_ticks()

        self.score = 0

        # Constants
        self.BASE_ACC = 0.5
        self.JUMP_VEL = -18
        self.JUMP_DELAY = 500

    def check_collisions(self):
        # Check and apply collisions with platforms
        self.rect.y += 1
        collisions = pygame.sprite.spritecollide(self, self.game.platform_sprites, False)
        self.rect.y -= 1
        if self.vel.y > 0 and collisions:  # Only applies collision if player is falling
            self.pos.y = collisions[0].rect.top
            self.vel.y = 0
        return collisions

    def update(self):
        keys = pygame.key.get_pressed()
        self.acc = pygame.Vector2(0, GRAVITY_ACC)
        collisions = self.check_collisions()
        current_time = pygame.time.get_ticks()

        # Change friction depending on platform
        if collisions:
            self.friction = collisions[0].friction  # Set player friction equal to platform friction
        else:
            self.friction = -0.12  # If player is in air, set back to base friction

        # Jump controls
        if collisions and keys[pygame.K_w] and self.can_jump \
                and self.vel.y >= 0 and current_time - self.last_jump_time >= self.JUMP_DELAY:
            # Get rid of "collisions and" to allow player to jump in the air (may be smoother gameplay)
            self.vel.y = self.JUMP_VEL
            self.can_jump = False
            self.last_jump_time = current_time
        elif collisions:
            self.can_jump = True

        # Horizontal controls
        if keys[pygame.K_a]:
            self.acc.x += -self.BASE_ACC
        if keys[pygame.K_d]:
            self.acc.x += self.BASE_ACC

        self.acc.x += self.vel.x * self.friction  # Apply friction
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)  # Kinematic equation

        # Wrap around sides of screen
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0

        # Calculated position will always represent midbottom of player sprite
        self.rect.midbottom = self.pos

    def reset(self):
        # Use this method to reset player's stats and stuff for new game
        self.__init__(self.game)  # placeholder


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), size=(16, 16), friction=-0.12):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=pos)

        self.friction = friction

