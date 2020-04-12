import os.path

class Map :

    def __init__(self, path) :
        # Récuperation du chemin vers le fichier .map
        self.path = os.getcwd() + path
        
        
        self.contenu = []
        

        # Ouverture du fichier
        file = open(self.path, 'r')

        # Boucle qui récupère le contenu du fichier sous forme de tableau qui stock chaque ligne du fichier en une chaine de caractère.
        for ligne in file : 
            self.contenu.append(ligne)

        # Fermeture du fichier lorsque tout est terminé.
        file.close()

