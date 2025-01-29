from direct.showbase.ShowBase import ShowBase
from direct.task.Task import sequence
from panda3d.core import Vec3, CollisionNode, CollisionBox
from pygame.draw import lines


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.cam.setPos(15,-4,54)
        self.taskMgr.add(self.move_camera, 'move_camera')

        self.is_fd = False
        self.is_bd = False
        self.is_right = False
        self.is_left = False
        self.is_up = False
        self.is_down = False

        self.accept('w', lambda : setattr(self, 'is_fd', True))
        self.accept('w-up', lambda : setattr(self, 'is_fd', False))

        self.accept('s', lambda: setattr(self, 'is_bd', True))
        self.accept('s-up', lambda: setattr(self, 'is_bd', False))

        self.accept('d', lambda: setattr(self, 'is_right', True))
        self.accept('d-up', lambda: setattr(self, 'is_right', False))

        self.accept('a', lambda: setattr(self, 'is_left', True))
        self.accept('a-up', lambda: setattr(self, 'is_left', False))

        self.box1 = self.loader.loadModel('models/box')
        self.box1.reparentTo(self.render)
        self.texture = self.loader.loadTexture("128x128/Wood/Wood_19-128x128.png")
        self.box1.setTexture(self.texture)

        

        self.box_2 = self.loader.loadModel('models/box')
        self.box_2.setTexture(self.texture)
        self.box_2.reparentTo(self.render)
        self.build_map('map.txt')


    def move_camera(self, task):

        speed=0.5

        if self.is_fd:
            self.cam.setY(self.cam.getY() + speed)
        if self.is_bd:
            self.cam.setY(self.cam.getY() - speed)

        if self.is_left:
            self.cam.setX(self.cam.getX() - speed)
        if self.is_right:
            self.cam.setX(self.cam.getX() + speed)

        if self.is_up:
            self.cam.setZ(self.cam.getZ() + speed)
        if self.is_down:
            self.cam.setZ(self.cam.getZ() - speed)

        return task.cont

    def build_map(self, map_file):
        with open(map_file, "r") as file:
            content = file.read()
        layers = content.split('---')
        for z, layer in enumerate(layers):
            lines = layer.strip().split('\n')
            for y, line  in enumerate(lines):
                for x, num  in enumerate(line):
                    if num == '1':
                        self.create_block(x, -y, z, '128x128/Grass/Grass_01-128x128.png')
                    if num == '2':
                        self.create_block(x, -y, z, '128x128/Grass/Grass_25-128x128.png')
                    if num == '3':
                        self.create_block(x, -y, z, '128x128/Bricks/Bricks_25-128x128.png')
                    if num == '4':
                        self.create_block(x, -y, z, '128x128/Roofs/Roofs_20-128x128.png')
                    if num == 'p':
                        self.create_panda(x, -y, z, '128x128/Roofs/Roofs_20-128x128.png')


    def create_block(self,x,y,z, texture_path):
        cube =self.loader.loadModel('models/box')
        cube.setPos(x, y, z)
        cube.reparentTo(self.render)
        texture = self.loader.loadTexture(texture_path)
        cube.setTexture(texture, True)

    def create_panda(self,x,y,z, texture_path=None):
        
        self.player.setPos(x, y, z)





app=MyApp()
app.run()
print(app.move_player_d)









