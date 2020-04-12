from src.core.Game import Game
#from src.interface.Sounds import Sounds
import os
import pygame

pygame.mixer.init()
pygame.mixer.music.load("src/interface/Sounds/main_theme2.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)
game = Game("Takenoko")
game.loop()
pygame.mixer.music.stop()