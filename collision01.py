"""Detecting sprite collision using rectangles with PyGame.

A short program which shows how collision detection works with PyGame. 
This collision detection uses the intersection of the rectangles 
of the sprites.
"""
import pygame
from pygame.constants import (
    QUIT, K_ESCAPE, KEYDOWN, KEYUP, K_DOWN, K_UP, K_LEFT, K_RIGHT
)
import os
import random


class Settings:
    """Project global informations.

    This static class contains project global informations 
    like window size and file directories.
    """
    window_width = 600
    window_height = 600
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")


class WarBird(pygame.sprite.Sprite):
    """A warbird sprite class.

    Short sprite example with no other function as showing if
    it collides with other sprites. 
    This class is derived from pygame.sprite.Sprite. 
    """

    def __init__(self):
        """Constructor function.

        Besides all other usual tasks of a constructor this function loads 
        the bitmap and computes a random start position. 
        """
        super().__init__()
        bitmap = pygame.image.load(os.path.join(
            Settings.image_path, "warbird.png"))
        self.image = bitmap.convert_alpha()
        self.rect = self.image.get_rect()
        self.newpos()

    def newpos(self):
        """Computing a new position.

        The horizontal position is a random number limited by the screen width.
        The vertical position is a random number limited by half of screen height.
        """
        self.rect.left = random.randint(
            0, Settings.window_width-self.rect.width)
        self.rect.bottom = random.randint(
            self.rect.height, Settings.window_height//2)


class Fire(pygame.sprite.Sprite):
    """A fire/shoot sprite class.

    Short sprite example which can be moved around
    collides with other warbird sprites. 
    This class is derived from pygame.sprite.Sprite. 
    """

    def __init__(self):
        """Constructor function.

        Besides all other usual tasks of a constructor this function loads 
        the bitmap and sets the start position. 
        """
        super().__init__()
        bitmap = pygame.image.load(
            os.path.join(Settings.image_path, "fire.png"))
        bitmap.set_colorkey((0, 0, 0))
        self.image = bitmap.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = Settings.window_width // 2
        self.rect.bottom = Settings.window_height
        self.speed = 3
        self.hdirection = 0
        self.vdirection = 0

    def update(self):
        """Update the sprite status

        This short update only computes the next position 
        without checking screen borders.
        """
        self.rect.move_ip(self.speed*self.hdirection,
                          self.speed*self.vdirection)

    def set_direction(self, direction):
        """Sets the direction of the move.

        According to the pressed arrow key the 
        vertical or horizontal direction is 
        set. At the beginning all directions are
        set to 0 - so the sprite doesn't move. 
        This will also happend when an unknown
        key was pressed.

        Args:
            direction ([int]): pygame key code
        """
        self.vdirection = 0
        self.hdirection = 0
        if direction == K_LEFT:
            self.hdirection = -1
        elif direction == K_RIGHT:
            self.hdirection = 1
        elif direction == K_DOWN:
            self.vdirection = 1
        elif direction == K_UP:
            self.vdirection = -1


if __name__ == '__main__':
    """Main function

    Starts and runs the the collision example. 

    Hint: This is not a testing main function.
    """

    # Preparation
    os.environ['SDL_VIDEO_WINDOW_POS'] = "50, 100"

#pylint: disable=no-member
    pygame.init()
#pylint: enable=no-member
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(
        (Settings.window_width, Settings.window_height))

    # random positioning of the war birds
    # with avoiding overlapping
    all_warbirds = pygame.sprite.Group()
    for i in range(8):
        maxtries = 100
        bird = WarBird()
        while maxtries >= 0:
            maxtries -= 1
            if pygame.sprite.spritecollide(bird, all_warbirds, False):
                bird.newpos()
            else:
                all_warbirds.add(bird)
                break

    fire = Fire()

    # main loop
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                else:
                    fire.set_direction(event.key)
            elif event.type == KEYUP:
                if event.key != K_ESCAPE:
                    fire.set_direction(0)

        # update
        fire.update()

        # draw
        screen.fill((255, 255, 255))

        t = pygame.sprite.spritecollide(fire, all_warbirds, False)
        if t:
            pygame.draw.rect(screen, (255, 0, 0), t[0].rect)
            pygame.draw.rect(screen, (0, 255, 0), fire.rect)

        all_warbirds.draw(screen)
        screen.blit(fire.image, fire.rect)
        pygame.display.flip()

    # bye bye
#pylint: disable=no-member
    pygame.quit()
#pylint: enable=no-member
