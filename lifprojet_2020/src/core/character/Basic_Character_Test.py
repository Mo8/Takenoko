from src.core.character.Character import Character


#permet juste d'avoir un character avec des stats prédéfinis
class Basic_Character_Test(Character):

    def __init__(self, name, health,x,y,id):
        Character.__init__(self,name,health,x,y,id)
        self.attak = 4
        self.defense = 1
        self.movement_point_max = 3
        self.action_point_max = 5
        self.action_point = self.action_point_max
        self.movement_point = self.movement_point_max
        self.initiative = 0
        self.range = 3










