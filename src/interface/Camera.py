

class Camera:

    def __init__(self,width,height):
        self.widthScreen = width
        self.heightScreen = height
        self.min_zoom = 5.0
        self.max_zoom = 1.0
        self.zoom = self.max_zoom
        self.x = 0
        self.y = 0
        self.base_size = 10
        self.real_tile_size = self.base_size * self.zoom
        self.offset = [0,0]

    def addZoom(self, z):
        self.zoom += z
        if self.zoom < self.max_zoom : 
            self.zoom =  self.max_zoom
        elif self.zoom > self.min_zoom : 
            self.zoom =  self.min_zoom

        # TOUT EST TILE !!!
        self.real_tile_size = int(self.base_size * self.zoom)


    def resetOffset(self):
        self.offset = [0,0]


    def calculOffsetCenter(self):
        self.offset[0] += int((self.widthScreen - self.real_tile_size)/2) 
        self.offset[1] += int((self.heightScreen - self.real_tile_size)/2)

    def move(self,x,y):
        self.x += x 
        self.y += y

    def getPosition(self):
        return (self.x,self.y)

    def setPosition(self,x,y):
        self.x = x
        self.y = y