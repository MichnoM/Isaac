import pygame

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width = 56, height = 66, scale = 1, colour = (0, 0, 0), rotation_angle = 0):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image = pygame.transform.rotate(image, rotation_angle)
        image.set_colorkey(colour)
    
        return image