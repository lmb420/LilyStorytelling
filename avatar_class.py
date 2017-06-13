import pyglet
from text_to_speech import talk
from win32api import GetSystemMetrics

class LilyAnimation(pyglet.window.Window):
    def __init__(self, fullscreen = True):
        pyglet.window.Window.__init__(self, fullscreen = fullscreen)
        self.lilyIdle = None
        self.lilyTalking = None
        self.lilySprite = None

        self.set_location(0,0)

        #set window background color = r, g, b, alpha
        #each value goes from 0.0 to 1.0
        self.background_color = 0.815, 0.87, 1, 1
        pyglet.gl.glClearColor(*self.background_color)

        self.init_images()
        self.isTalking = False

    def init_images(self):
        self.lilyIdle = pyglet.resource.animation("AvatarGifs/lily_idle.gif")
        self.lilyTalking = pyglet.resource.animation("AvatarGifs/lily_talking.gif")
        self.lilySprite = pyglet.sprite.Sprite(self.lilyIdle)
        self.lilySprite.set_position((GetSystemMetrics(0) - self.lilySprite.width) / 2, (GetSystemMetrics(1) - self.lilySprite.height) / 2)        

    def on_draw(self):
        print("Starting on_draw")
        self.clear()
        self.lilySprite.draw()

    def on_deactivate(self):
        self.minimize()

    def check_talk(self):
        if self.isTalking != talk:
            self.isTalking = talk
            if not talk:
                self.lilySprite.image = self.lilyIdle
            else:
                self.lilySprite.image = self.lilyTalking
            on_draw()

LilyAnimation.register_event_type('on_talk')
