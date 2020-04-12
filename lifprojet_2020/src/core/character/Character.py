
from src.core.character.Pathfinder import PathFinding
import math
import queue
from copy import deepcopy


class Character:
    def __init__(self, name, health, x, y, id):
        self.position = [x, y]
        self.name = name
        self.health = health
        self.range = None
        self.attak = None
        self.defense = None
        self.movement_point_max = None
        self.action_point_max = None
        self.movement_point = None
        self.action_point = None
        self.initiative = None
        self.skill = None
        self.target = None
        self.team = id
        self.path = PathFinding()
        self.pathAdvancement = 0
        self.message = queue.Queue()


    #permet de trouver une nouvelle cible
    def searchNewTarget(self, characters):
        #si on a un message on decide que la nouvelle cible est celle du premier message avec une cible valide ( en vie )
        while not self.message.empty():
            self.target = self.message.get()
            if self.target.health > 0:
                return



        distance = None
        self.target = None
        #sinon on cherche parmis les characters d'une equipe adverse et encore en vie , le plus proche devient la nouvelle cible
        for c in characters:
            if c.team != self.team and c.health > 0:
                if self.target is None:

                    self.target = c
                    distance = math.hypot(self.position[0] - c.position[0], self.position[1] - c.position[1])
                else:
                    d = math.hypot(self.position[0] - c.position[0], self.position[1] - c.position[1])
                    if d < distance:
                        self.target = c
                        distance = d


        #si il n'existe pas d'ennemie valide on quitte
        if self.target is None:
            return

        distance = None
        help = None
        #sinon on envoie à l'allier le plus proche un message pour venir aider à tuer l'ennemie que l'on a ciblé
        for c in characters:
            if c.team == self.team and c.health > 0:
                if help is None:

                    help = c
                    distance = math.hypot(self.position[0] - c.position[0], self.position[1] - c.position[1])
                else:
                    d = math.hypot(self.position[0] - c.position[0], self.position[1] - c.position[1])
                    if d < distance:
                        help = c
                        distance = d
        #si on a effectivement trouver un allier on lui envoie le message conteant la cible
        if help is not None:
            help.message.put(self.target)

    #à utiliser quand il y a un nouveau tour , réinitialise les point de mouvement et d'action
    def newTurn(self):
        self.movement_point = self.movement_point_max
        self.action_point = self.action_point_max

    #permet de gerer comment on prend des dégats
    def takeDamage(self, x):
        after_defense = x - self.defense
        if after_defense < 0:
            after_defense = 0
        self.health -= after_defense

    #permet de calculer le chemin pour aller à la cible pour cela on fait du pathfinding A*
    def calculPathToTarget(self, characters, walls):

        map = deepcopy(walls)
        for c in characters:
            map[c.position[0]][c.position[1]] = c.health > 0
        map[self.position[0]][self.position[1]] = False
        map[self.target.position[0]][self.target.position[1]] = False
        self.path.calculPath(map, (self.position[0], self.position[1]),
                             (self.target.position[0], self.target.position[1]))
        self.pathAdvancement = 1

    #permet de savoir si on est à porter de la cible pour pouvoir lattaquer
    def rangeTarget(self):
        return math.hypot(self.position[0] - self.target.position[0],
                          self.position[1] - self.target.position[1]) <= self.range

    # on déroule un tour complet pour un character
    def turn(self, characters, walls):
        if self.target is None or (self.target is not None and self.target.health <= 0):
            self.searchNewTarget(characters)
            if self.target is None:
                return
            print(self.name, " New target -> ", self.target.name)

        # on regarde si on est à porter pour attaquer
        outOfRange = not (self.rangeTarget())

        self.calculPathToTarget(characters, walls)
        if self.path.path is None and outOfRange:
            return


        # tant que l'on est trop loin de la cible et que l'on a des point de mouvements ou qu'on est assez pres de la cible et que lon a des points d'action
        while (self.movement_point > 0 and outOfRange == True) or (self.action_point > 0 and outOfRange == False):

            # si on a plus de target ou que que notre target na plus de vie
            if self.target is None or (self.target is not None and self.target.health <= 0):
                # on cherche une nouvelle target
                self.searchNewTarget(characters)
                # si pas de nouvelle target on quitte
                if self.target is None:
                    return
                print(self.name, " New target -> ", self.target.name)
                # sinon on calcul le trajet jusqu'à la target
                self.calculPathToTarget(characters, walls)
                # on regarde si on est à porter pour attaquer
                outOfRange = not (self.rangeTarget())

                # si on a pas de trajet jusqu'à la target et que l'on est pas à porter de la target on quitte
                if self.path.path is None and outOfRange:
                    return

            # si on a une target et qu'elle est encore en vie
            if self.target is not None and self.target.health > 0:
                # on regarde si on est à porter pour attaquer
                outOfRange = not (self.rangeTarget())
                if self.action_point > 0 and outOfRange == False:

                    self.target.takeDamage(self.attak)
                    self.action_point -= 1
                    print(self.name, " Attaque -> ", self.target.name, "Vie restante : ", self.target.health,
                          "   Point d'action restant  -> ", self.action_point)
                    if self.target.health <= 0:
                        self.target = None
                        continue

                if self.movement_point > 0 and outOfRange == True:
                    self.move(characters, walls)

    #gere les mouvements le long du chemin preetablie par path
    def move(self, characters, walls):

        if self.path.path is not None:
            if self.pathAdvancement < len(self.path.path) - 1:
                self.position = self.path.path[self.pathAdvancement]
                self.pathAdvancement += 1
                self.movement_point -= 1
                print(self.name, " Deplacement à la position ->", self.position, " Point de mouvement restant -> ",
                      self.movement_point)
            # print("FinPath")
        else:
            self.target = None
