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

    def start_game(self):
        app1 = MyApp()
        app1.run()

    def exit_game(self):
        print("Exiting game...")
        self.userExit()

    def change_volume(self):
        if self.sound:
            volume = self.volume_slider['value']
            self.sound.setVolume(volume)


app = MenuDemo()
app.run()
