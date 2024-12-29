from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.model = self.loader.loadModel("models/environment")
        self.model.setScale(0.5)
        self.model.setPos(300, 0, 0)
        self.model.reparentTo(self.render)
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

        self.accept('arrow_up', lambda: setattr(self, 'is_up', True))
        self.accept('arrow_up-up', lambda: setattr(self, 'is_up', False))

        self.accept('arrow_down', lambda: setattr(self, 'is_down', True))
        self.accept('arrow_down-up', lambda: setattr(self, 'is_down', False))

        self.box1 = self.loader.loadModel('models/box')
        self.box1.reparentTo(self.render)
        self.texture = self.loader.loadTexture("128x128/Wood/Wood_19-128x128.png")
        self.box1.setTexture(self.texture)

        

        self.box_2 = self.loader.loadModel('models/box')
        self.box_2.setTexture(self.texture)
        self.box_2.reparentTo(self.render)
        self.build_map('map.txt')


    def move_camera(self, task):

        speed=1

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
            lines = file.readlines()
        z = 0
        for y, line  in enumerate(lines):
            for x, num  in enumerate(line):
                if num == '1':
                    self.place_box(x, -y, z)
                if num == '2':
                    self.place_cube(x, -y, z)


    def place_box(self,x,y,z):
        cube = self.box1.copyTo(self.render)
        cube.setPos(Vec3(x,y,z))

    def place_cube(self,x,y,z):
        cube = self.box_2.copyTo(self.render)
        cube.setPos(x,y,z)



app=MyApp()
app.run()