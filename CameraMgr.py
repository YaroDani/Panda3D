from direct.showbase.ShowBase import ShowBase
from direct.task.Task import sequence
from panda3d.core import Vec3, CollisionNode, CollisionBox
from pygame.draw import lines

cn = CollisionNode('model_collision')


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.cam.setPos(10, -4, 35)
        self.taskMgr.add(self.move_camera, 'move_camera')

        self.is_fd = False
        self.is_bd = False
        self.is_right = False
        self.is_left = False
        self.is_up = False
        self.is_down = False


        self.accept('d', lambda: setattr(self, 'is_right', True))
        self.accept('d-up', lambda: setattr(self, 'is_right', False))

        self.accept('a', lambda: setattr(self, 'is_left', True))
        self.accept('a-up', lambda: setattr(self, 'is_left', False))

        self.build_map('map2.txt')
        self.move_player_d = {
            'fd': False,
            'bd': False,
            'left': False,
            'right': False,
            'is_jump': False
        }
        self.accept('arrow_up', lambda: self.update_move('fd', True))
        self.accept('arrow_up-up', lambda: self.update_move('fd', False))

        self.taskMgr.add(self.move_player)
        
        self.show_c()

    def show_c(self):
        self.player_coll.show()
        self.player_coll.setColor(1, 1, 0, 1)
        self.player_coll.setRenderModeWireframe()

    def update_move(self, key, value):
        if key in self.move_player_d:
            self.move_player_d[key] = value

    def move_camera(self, task):
        speed = 0.2

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
            for y, line in enumerate(lines):
                for x, num in enumerate(line):
                    if num == '1':
                        self.create_block(x, -y, z, '128x128/Grass/Grass_01-128x128.png')
                    if num == '2':
                        self.create_block(x, -y, z, '128x128/Grass/Grass_25-128x128.png')
                    if num == '3':
                        self.create_block(x, -y, z, '128x128/Bricks/Bricks_25-128x128.png')
                    if num == '4':
                        self.create_block(x, -y, z, '128x128/Roofs/Roofs_20-128x128.png')
                    if num == 'p':
                        self.create_panda(x, -y, z,)

    def create_block(self, x, y, z, texture_path):
        cube = self.loader.loadModel('models/box')
        cube.setPos((x, y, z))
        cube.reparentTo(self.render)
        texture = self.loader.loadTexture(texture_path)
        cube.setTexture(texture, True)

        self.coll_node.addSolid(CollisionBox((x, y, z), 1, 1, 1))
        # показ колізій
        coll_node = CollisionNode('wall_coll')
        coll_node.addSolid(CollisionBox((0, 0, 0), 1, 1, 1))

        coll_np = cube.attachNewNode(coll_node)
        coll_np.show()
        coll_np.setRenderModeWireframe()
        coll_np.setColor(1, 1, 0, 1)

    def create_panda(self, x, y, z, texture_path=None):
        self.player.setPos(x, y, z)

    def move_player(self, task):
        speed = 0.15
        rotation_speed = 1
        moving = False

        if self.mouseWatcherNode.is_button_down(KeyboardButton.left()):
            self.player.setH(self.player.getH() + rotation_speed)
            moving = True
        if self.mouseWatcherNode.is_button_down(KeyboardButton.right()):
            self.player.setH(self.player.getH() - rotation_speed)
            moving = True
        if self.mouseWatcherNode.is_button_down(KeyboardButton.up()):
            self.player.setY(self.player, -speed)
            moving = True
        if self.mouseWatcherNode.is_button_down(KeyboardButton.down()):
            self.player.setY(self.player, speed)
            moving = True

        if moving:
            if not self.player.getCurrentAnim():
                self.player.loop('walk')
        else:
            self.player.stop()

        self.ct.traverse(self.render)

        return task.cont

app = MyApp()
app.run()
print(app.move_player_d)