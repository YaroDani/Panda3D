from direct.showbase.ShowBase import ShowBase
from direct.task.Task import sequence
from panda3d.core import Vec3, CollisionNode, CollisionBox, Point3, CollisionTraverser, CollisionHandlerPusher, \
    CollisionSphere
from panda3d.core import KeyboardButton
from direct.actor.Actor import Actor
from direct.gui.DirectGui import DirectButton, DirectFrame, DirectSlider, DirectLabel
from panda3d.core import TextNode

class MenuDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.s_game = False
        # Background frame (Menu panel)
        self.menu_frame = DirectFrame(frameColor=(0, 0, 0, 0.7),  # Dark background
                                      frameSize=(-1, 1, -0.8, 0.8),
                                      pos=(0, 0, 0))
        # "Start" Button
        self.play_button = DirectButton(text="Start",
                                        scale=0.2,
                                        pos=(0, 0, 0.2),
                                        command=self.start_game)
        # "Exit" Button
        self.exit_button = DirectButton(text="Exit",
                                        scale=0.2,
                                        pos=(0, 0, -0.1),
                                        command=self.exit_game)
        # Volume label
        self.volume_label = DirectLabel(text="Volume",
                                        scale=0.06,
                                        pos=(0, 0, -0.2),
                                        text_fg=(1, 1, 1, 1),  # White text
                                        text_align=TextNode.ACenter)
        # Volume slider
        self.volume_slider = DirectSlider(range=(0, 1),
                                          value=0.5,
                                          pos=(0, 0, -0.3),
                                          scale=0.3,
                                          command=self.change_volume)
        try:
            self.sound = self.loader.loadSfx("china_town.mp3")
            self.sound.setLoop(True)
            self.sound.play()
        except:
            self.sound = None
            print("Sound file not found!")

    def init_game(self):
        self.level = 1
        self.level_label = DirectLabel(text=f"Level: {self.level}", scale=0.09, pos=(0, 0, 0.9))
        self.cam.setPos(10, -4, 35)
        self.cam.setHpr(0, -90, 0)

        self.player = Actor('models/panda', {"walk": "models/panda-walk"})
        self.player.reparentTo(self.render)
        self.player.setScale(0.1)
        self.player_angle = 0

        # колізії гравця
        coll_node_player = CollisionNode('player_coll')
        coll_node_player.add_solid(CollisionSphere(0, 0, 0, 4))
        self.player_coll = self.player.attachNewNode(coll_node_player)

        # колізії стін
        self.coll_node = CollisionNode('walls')
        self.coll_node.setIntoCollideMask(1)
        self.coll_node_group = self.render.attachNewNode(self.coll_node)

        # система колізій
        self.ct = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        # колізії фінішу

        coll_node_player_finish = CollisionNode('player_coll_finish')
        coll_node_player_finish.add_solid(CollisionSphere(0, 0, 0, 4))
        self.player_coll_finish = self.player.attachNewNode(coll_node_player)

        self.coll_node_finish = CollisionNode('finish')
        self.coll_node_finish.setIntoCollideMask(1)
        self.coll_node_group_finish = self.render.attachNewNode(self.coll_node_finish)
        self.accept('player_coll_finish-into-finish', self.on_finish)

        self.ct.addCollider(self.player_coll, self.pusher)
        self.pusher.addCollider(self.player_coll, self.player)

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
        #self.show_c()

    def show_c(self):
        pass
        '''self.player_coll.show()
        self.player_coll.setColor(1, 1, 0, 1)
        self.player_coll.setRenderModeWireframe()'''

    def on_finish(self):
        print('НА фініші')
        if self.level < 3:
            self.level += 1
            self.level_label['text'] = "Level: " + str(self.level)

            self.build_map('map2.txt')

    def update_move(self, key, value):
        if key in self.move_player_d:
            self.move_player_d[key] = value
    '''
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

        return task.cont'''

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
                        self.create_block(x, -y, z, '128x128/Wood/Wood_10-128x128.png')
                    if num == '5':
                        self.create_block(x, -y, z, '128x128/Grass/Grass_19-128x128.png')
                    if num == 'F':
                        self.create_finish(x, -y, z, '128x128/Wood/Wood_10-128x128.png')
                    if num == 'p':
                        self.create_panda(x, -y, z,)

    def create_block(self, x, y, z, texture_path):
        cube = self.loader.loadModel('models/box')
        cube.setPos((x, y, z))
        cube.reparentTo(self.render)
        texture = self.loader.loadTexture(texture_path)
        cube.setTexture(texture, True)

        self.coll_node.addSolid(CollisionBox((x + 0.5, y + 0.5, z + 0.5), 0.6, 0.6, 0.6))
        # показ колізій
        #self.ct.showCollisions(self.render)

    def create_finish(self, x, y, z, texture_path):
        cube = self.loader.loadModel('models/box')
        cube.setPos((x, y, z))
        cube.reparentTo(self.render)
        texture = self.loader.loadTexture(texture_path)
        cube.setTexture(texture, True)

        self.coll_node_finish.addSolid(CollisionBox((x + 0.5, y + 0.5, z + 0.5), 0.6, 0.6, 0.6))
        # показ колізій
        #self.ct.showCollisions(self.render)

    def create_panda(self, x, y, z, texture_path=None):
        self.player.setPos(x + 0.5, y+ 0.5, z+ 0.5)

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

        self.cam.setX(self.player.getX())
        self.cam.setY(self.player.getY())
        self.cam.setZ(self.player.getZ()+20)

        if moving:
            if not self.player.getCurrentAnim():
                self.player.loop('walk')
        else:
            self.player.stop()

        self.ct.traverse(self.render)

        return task.cont

    def start_game(self):
        self.menu_frame.hide()
        self.play_button.hide()
        self.volume_slider.hide()
        self.volume_label.hide()
        self.exit_button.hide()
        self.init_game()

    def exit_game(self):
        print("Exiting game...")
        self.userExit()

    def change_volume(self):
        if self.sound:
            volume = self.volume_slider['value']
            self.sound.setVolume(volume)


app = MenuDemo()
app.run()
