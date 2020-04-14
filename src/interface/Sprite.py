import pathlib
import pygame


class Sprite:

    resourcesFolder = str(pathlib.Path(__file__).parent.parent.parent.absolute().joinpath("res")) + str(pathlib.PurePath('/'))

    name = ""
    filename = ""
    sprite = None
    width = 0
    height = 0

    
    def __init__(self, name, filename=""):
        if filename == "":
            self.filename = name + ".png"
        else:
            self.filename = filename
        
        self.name = name

        try:
            self.sprite = pygame.image.load(self.resourcesFolder + self.filename)
            self.width, self.heigth = self.sprite.get_size()
        except:
            print("Exeption occured in loading sprite " + name)



    
    def getSprite(self):
        return self.sprite
    

    
    


