from src.interface.Graphics import Graphics
from src.core.Board import Board
from src.core.Map import Map
import pygame

#classe representant le jeu et faisant le lien entre le plateau de jeu et l'affichage et la gestion de évenement
class Game:
    camera_move  = 0
    
    def __init__(self, name):
        self.name = name
        self.graphics = Graphics(name)

        # Ajout de la création de map et du passage en argument sur Board()
        #map0 = Map("/res/Map/petite.map")
        map0 = Map("/res/Map/open-field.map")
        #map0 = Map("/res/Map/labyrinthe.map")
        #map0 = Map("/res/Map/custom-nico.map")
        self.board = Board(map0)

        self.auto = False #variable pour mettre le jeu en automatique
        pygame.time.set_timer(pygame.USEREVENT+1, 50)#timer qui creer un event toute les 50 ms
        self.fin = False #permet de savoir quand le jeu est fini
        
    

    #fonction gerant les évènements claviers , souris et un evenement cyclique toute les x temps
    def events_combat(self):
        mouse = pygame.mouse.get_pos() #permet d'obtenir la position de la souris
        

        for event in pygame.event.get():  
                   
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()

            # évènement de zoom: gère le zoom/dezoom caméra
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 :
                    self.graphics.cameraAddZoom(-1)
                elif event.button == 5 :
                    self.graphics.cameraAddZoom(1)

            # évènement clavier : gère la caméra , la pause et le fait de passer un tour
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP :
                    self.graphics.camera.move(0,-1)
                elif event.key == pygame.K_DOWN :
                    self.graphics.camera.move(0,1)
                elif event.key == pygame.K_LEFT :
                    self.graphics.camera.move(-1,0)
                elif event.key == pygame.K_RIGHT :
                    self.graphics.camera.move(1,0)
                elif event.key == pygame.K_o:
                    if self.auto == True:
                        self.auto = False
                    else:
                        self.auto = True
                elif event.key == pygame.K_SPACE :
                    if self.fin == False:
                        self.fin = self.board.nextCharacterTurn()


            #evenement cyclique grace à un timer qui permet de deplacer la camera si la souris est sur un bord de la fenetre
            elif event.type == pygame.USEREVENT+1 and pygame.mouse.get_focused():
                if self.fin == False and self.auto == True:
                    self.fin = self.board.nextCharacterTurn()

                if 0 <= mouse[1] <= 20 :
                    self.graphics.camera.move(0,-1)
                elif self.graphics.height-20 <= mouse[1] <= self.graphics.height:
                    self.graphics.camera.move(0,1)
                elif 0 <= mouse[0] <= 20 :
                    self.graphics.camera.move(-1,0)
                elif self.graphics.width-20 <= mouse[0] <= self.graphics.width :
                    self.graphics.camera.move(1,0)

            






    def update(self):
        self.events_combat()



    def display(self):
        self.graphics.display_combat(self.board)


    def loop(self):
        #boucle du jeu qui regarde si on fait une mise à jour puis qui fait la mise à jour graphique
        while(self.fin is False):
            self.update()
            self.display()
        print("L'équipe ",self.fin, " a gagné !")

            
            
            
