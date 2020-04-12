

from src.interface.Sprite import Sprite
from src.interface.Camera import Camera
import pygame


class Graphics:

    
    def __init__(self, name="Nom du jeu"):

        # on charges ici les sprites nécessaires au jeu
        # on peut en ajouter sans problème
        self.sprites = {
            "grass": Sprite("grass"),
            "basica": Sprite("basic", "basic0.png"),
            "basicb": Sprite("basic", "basic1.png"),
            "wall": Sprite("wall"),
            "door": Sprite("door")
        }

        # taille de l'écran
        self.width = 1080
        self.height = 720
        self.size = (self.width, self.height)

        # base size définit la taille de TOUS les éléments
        # elle bouge en fonction du zoom (géré par la caméra)
        self.camera  = Camera(self.width,self.height)

        # on initialise l'écran graphique
        self.screen = pygame.display.set_mode(self.size)

        # permet de renseigner le nom de l'application
        pygame.display.set_caption(name)
        
        # créé une surface de la taille de la fenetre
        self.background = pygame.Surface(self.size)
        self.background.fill(pygame.Color(40, 40, 40)) # changer la couleur du background ici



    # ******************************************
    # fonctions d'aide pour simplifier
    def blitTileSurface(self, surface, x, y, scale_factor=1.0):
        self.screen.blit(self.scaleTileSurface(surface, scale_factor), [x, y])
    def clear(self):
        self.screen.blit(self.background, [0, 0])
    def scaleTileSurface(self, surface, factor):
        return pygame.transform.scale(surface, (int(self.camera.real_tile_size*factor), int(self.camera.real_tile_size*factor)))
    def blitSurface(self, surface, x, y, scale_factor=1.0):
        self.screen.blit(self.scaleSurface(surface, scale_factor), [x, y])
    def scaleSurface(self, surface, factor):
        w, h = surface.get_size()
        return pygame.transform.scale(surface, (int(w*factor), int(h*factor)))
    # ******************************************


    #permet un affichage du plateau de jeu correcte
    def displayBoard(self, board):

        
        
        # on récupère la distance entre le centre de l'écran et un bord (horizontal)
        # EN NOMBRE DE TILES !
        dX = int((self.width/self.camera.real_tile_size)/2)
        
        # définit la range des tiles affichages sur l'axe x
        # self.camera.x = numéro de tiles (axe x) sur lequel on est centrer actuellement (et donc la caméra)
        displayableX = [self.camera.x-dX-1, self.camera.x+dX+1]
        
        #on limite à gauche
        if(displayableX[0] < 0): 
            displayableX[0] = 0

        #on limite a droite
        if(displayableX[1] > board.size[0]):
            displayableX[1] = board.size[0]

        # on récupère la distance entre le centre de l'écran et un bord (vertical)
        dY = int((self.height/self.camera.real_tile_size)/2)

        # définit la range des tiles affichages sur l'axe y
        displayableY = [self.camera.y-dY-1, self.camera.y+dY+1]

        #on limite en haut
        if(displayableY[0] < 0): 
            displayableY[0] = 0
        
        #on limite en bas
        if(displayableY[1] > board.size[1]):
            displayableY[1] = board.size[1]
        


        #affichage du plateau de jeu
        for x in range(displayableX[0] , displayableX[1]) :
            for y in range(displayableY[0] , displayableY[1]) :
                #si on a un mur on laffiche
                if board.walls[x][y] == True:
                    self.blitTileSurface(
                        surface=self.sprites['wall'].getSprite(),
                        x=self.camera.offset[0] + (x - self.camera.x) * (self.camera.real_tile_size),
                        y=self.camera.offset[1] + (y - self.camera.y) * (self.camera.real_tile_size),
                        scale_factor=1)
                #sinon on affiche de l'herbe
                else :
                    self.blitTileSurface(
                        surface=self.sprites['grass'].getSprite(),
                        x=self.camera.offset[0] + (x - self.camera.x) * (self.camera.real_tile_size),
                        y=self.camera.offset[1] + (y - self.camera.y) * (self.camera.real_tile_size),
                        scale_factor=1)
        #affichage des characters sur le plateau de jeu
        for c in board.characters:
            if c.health > 0 and displayableX[0] <= c.position[0]< displayableX[1] and displayableY[0]<= c.position[1]< displayableY[1]:
                self.blitTileSurface(
                    surface=self.sprites['basic'+str(c.team)].getSprite(),
                    x=self.camera.offset[0] + (c.position[0] - self.camera.x) * (self.camera.real_tile_size),
                    y=self.camera.offset[1] + (c.position[1] - self.camera.y) * (self.camera.real_tile_size),
                    scale_factor=1)
    


    
    #permet de gèrer les étapes pour bien afficher ce que l'on veut
    def display_combat(self, board) :
        
        # efface l'écran
        self.clear()

        #on remet le decalage camera à zero
        self.camera.resetOffset()
        #puis on le recentre ( permet de gerer le zoom plus facilement )
        self.camera.calculOffsetCenter()
        self.displayBoard(board)
        # affiche le prochain écran (buffer swap)
        pygame.display.flip()



    # gère le zoom de la caméra
    # est appellé dans game.py
    def cameraAddZoom(self, z):
        self.camera.addZoom(z)

