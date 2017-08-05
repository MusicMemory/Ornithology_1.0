import pygame

from base.Singleton import Singleton

class ImageRepository(metaclass=Singleton):

    def __init__(self, folder_images):
        self.__folder_images = folder_images

    def load_image(self, filename):
        return pygame.image.load(self.__folder_images + "/" + filename)
