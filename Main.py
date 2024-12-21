from direct.showbase.ShowBase import ShowBase


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.model = self.loader.loadModel("models/environment")
        self.model.setScale(0.5)
        self.model.setPos(0, 0, 0)
        self.model.reparentTo(self.render)

        self.human = self.loader.loadModel("Base Humanoid Mesh/Humanoid.fbx")
        self.human.reparentTo(self.render)
        self.human.setPos(0, 0, 50)

        self.teapot = self.loader.loadModel("models/teapot")
        self.teapot.reparentTo(self.render)
        self.teapot.setPos(0, 0, 60)

        self.texture = self.loader.loadTexture("128x128/Wood/Wood_19-128x128.png")
        self.human.setTexture(self.texture)

        self.cam.setPos(110, -400, 0)

        self.accept('w', self.move_forward)

        self.accept('a', self.move_left)
        self.accept('d', self.move_right)
        self.accept('s', self.move_backward)

        self.accept('arrow_up', self.move_upward)
        self.accept('arrow_down', self.move_down)
        self.accept('arrow_left', self.turn_right)
        self.accept('arrow_right', self.turn_left)

        self.camera_angle = 0
        self.pitch_angle = 0

        # додавання подіїї до ігрового цикла(кожну ітерацію обробляється)
        self.taskMgr.add(self.spin_human, 'spin_human')
        #self.taskMgr.add(self.move, 'move')
        #self.is_fd = False
        #self.accept('w', lambda: setattr(self, 'is_fd', True))

    def spin_human(self, task):
        angle = task.time * 100
        pitch_angle = task.time * 100
        roll_angle = task.time * 100
        self.human.setHpr(angle , pitch_angle, roll_angle)
        return task.cont

    #def move(self, task):
        #if self.is_fd:
            #self.cam.setY(self.cam.getY() + 1)
        #return task.cont

    def move_forward(self):
        self.cam.setY(self.cam.getY() + 100)
    def move_backward(self):
        self.cam.setY(self.cam.getY() - 100)

    def move_left(self):
        self.cam.setX(self.cam.getX() - 10)
    def move_right(self):
        self.cam.setX(self.cam.getX() + 10)

    def move_upward(self):
        self.cam.setZ(self.cam.getZ()+15)
    def move_down(self):
        self.cam.setZ(self.cam.getZ()-10)

    def turn_left(self):
        self.camera_angle -= 10
        self.update_camera()
    def turn_right(self):
        self.camera_angle+=10
        self.update_camera()
    def update_camera(self):
        self.cam.setHpr(self.camera_angle, self.pitch_angle, 0)



app = MyApp()
app.run()