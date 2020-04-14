
from src.core.character.Basic_Character_Test import Basic_Character_Test
import random


#classe representant le plateau de jeu
class Board:

   

    def __init__(self, mapObject):
        self.loadBoard(mapObject)


        for c in self.characters:
                c.initiative = random.randint(0, 100)

        self.calculSequence()
        self.counterSequence = 0
        self.counterTurn = 0

    def calculSequence(self):
        self.sequence = []
        for c in range(len(self.characters)):
            self.sequence.append((self.characters[c].initiative, c))
        self.sequence.sort()

    def moreThanOneTeam(self):
        b = None
        for c in self.characters:
            if c.health > 0:
                if b is None:
                    b = c.team
                if c.team != b :
                    return True
        return b





    def loadBoard(self, mapObject):
        
        self.walls = []
        self.characters = []

        # Boucle d'initialisation et remplissage de self.walls sur le modèle du fichier grace à la variable qui a récupéré son contenu. 
        #On en profite pour calculer le maximum de caractère par ligne pour remseigner self.size
        self.size = (len(mapObject.contenu[0].rstrip('\n')),len(mapObject.contenu) )
        for x in range(0, self.size[0]):
            self.walls.append([])
            for y in range(0, self.size[1]):
                self.walls[x].append(False)

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if mapObject.contenu[y][x] == '1' :
                    self.walls[x][y] = True
                elif mapObject.contenu[y][x] != '0' :
                    self.characters.append(Basic_Character_Test(mapObject.contenu[y][x]+" "+str(x),20,x,y,mapObject.contenu[y][x]))


#defile le tour du prochain character à jouer et retourne False si aucune équipe n'a gagné et l'id de l'équipe qui a gagné sinon
    def nextCharacterTurn(self):

        while self.characters[self.sequence[self.counterSequence][1]].health <= 0:


            self.counterSequence += 1


            if self.counterSequence == len(self.sequence)   :
                self.counterTurn += 1
                print("Tour numero ", self.counterTurn)
                self.counterSequence = 0
                for c in self.characters:
                    c.newTurn  ()




        self.characters[self.sequence[self.counterSequence][1]].turn(self.characters, self.walls)

        self.counterSequence += 1

        if self.counterSequence == len(self.sequence):
            self.counterTurn += 1
            print("Tour numero ", self.counterTurn)
            self.counterSequence = 0
            for c in self.characters:
                c.newTurn()

        t = self.moreThanOneTeam()
        if t is not True:
            return t

        return False


