from  heapq import heappush, heappop
import math


class PathFinding():

    class SearchNode:

        def __init__(self, data, gscore=float('inf'), fscore=float('inf')):
            self.data = data
            self.gscore = gscore
            self.fscore = fscore
            self.closed = False
            self.out_openset = True
            self.came_from = None

        def __lt__(self, b):
            #Comparaison pour la liste de priorité
            return self.fscore < b.fscore

    class SearchNodeDict(dict):

        def __missing__(self, k):
            #Creer un noeud si le noeud ciblé n'existe pas
            v = PathFinding.SearchNode(k)
            self.__setitem__(k, v)
            return v

    def __init__(self, map = None , start = None  , end = None ):

        if map is not None or start is not None or end is not None:
            self.map = map
            temp = self.astar(start, end)
            if temp is not None :
                self.path = list(temp)
            else:
                self.path = None
        else:
            self.path = None

    def heuristic_cost_estimate(self, n1, n2):
        (x1, y1) = n1
        (x2, y2) = n2
        return math.hypot(x2 - x1, y2 - y1)

    def distance_between(self, n1, n2):
        #On défini que le cout d'un deplacement entre 2 positions coute 1 point de déplacemnt a l'unité
        return 1

    def neighbors(self, node):
        #Retourne le coordonnées [x,y] des voisins possible autours, càd Haut, Gauche, Bas, Droite, les diagonales ne sont pas utilisé ici
        #Et qui ne sont pas des murs ou en dehors de la map
        x, y = node
        l=[]
        for nx, ny in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
            if 0 <= nx < len(self.map) and 0 <= ny < len(self.map[0]) and self.map[nx][ny] == False:
                l.append((nx,ny))
        return l

    def is_goal_reached(self, current, goal):
        return current == goal

    def reconstruct_path(self, last, reversePath=False):
        def _gen():
            current = last
            while current:
                yield current.data
                current = current.came_from
        #Génération de la liste qui compose le chemin que va utiliser l'unité
        if reversePath:
            return _gen()
        else:
            return reversed(list(_gen()))

    def astar(self, start, goal, reversePath=False):
        if self.is_goal_reached(start, goal):
            return [start]
        searchNodes = PathFinding.SearchNodeDict()
        startNode = searchNodes[start] = PathFinding.SearchNode(start, gscore=.0, fscore=self.heuristic_cost_estimate(start, goal))
        openSet = []
        heappush(openSet, startNode)
        while openSet:
            current = heappop(openSet)
            if self.is_goal_reached(current.data, goal):
                return self.reconstruct_path(current, reversePath)
            current.out_openset = True
            current.closed = True
            for neighbor in map(lambda n:searchNodes[n], self.neighbors(current.data)):
                if neighbor.closed:
                    continue
                tentative_gscore = current.gscore + self.distance_between(current.data, neighbor.data)
                if tentative_gscore >= neighbor.gscore:
                    continue
                neighbor.came_from = current
                neighbor.gscore = tentative_gscore
                neighbor.fscore = tentative_gscore + self.heuristic_cost_estimate(neighbor.data, goal)
                if neighbor.out_openset:
                    neighbor.out_openset = False
                    heappush(openSet, neighbor)
        return None


    def calculPath(self, map, start, end):
        if map is not None or start is not None or end is not None:
            self.map = map
            temp = self.astar(start, end)
            if temp is not None:
                self.path = list(temp)
            else:
                self.path = None
        else:
            self.path = None