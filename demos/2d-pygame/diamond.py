import sys

from common import *

DIAMOND_POS_OFFSET_X = 0
DIAMOND_POS_OFFSET_Y = 0

SCALE_DOWN = 8

DIAMOND_ANIM_PERIOD = 1/18

TEXTURE_PATH = "assets/blends/diamond-COLOR/diamond-COLORNNNN.png" # COLOR = either red, blue or yellow
                                                                   # NNNN from 0001 to 0017

#---- Import Mini Python Game Engine -----
MINI_PY_GE_DIR = "../../minipyge"
sys.path.append(MINI_PY_GE_DIR)
from minipyge import *

class Diamond(MiniPyGENode):
  diamond_n = 1
  textures_red = []
  textures_blue = []
  textures_yellow = []

  def __init__(self, color, position):
    super().__init__("Diamond_" + str(Diamond.diamond_n))
    Diamond.diamond_n += 1
    self.position = position
    self.color = color

    if color == "red":
      self.textures = Diamond.textures_red
    elif color == "blue":
      self.textures = Diamond.textures_blue
    elif color == "yellow":
      self.textures = Diamond.textures_yellow
    else:
      print("Bad color " + color)
      sys.exit(1)
    
    self.num_textures = 0
    self.animation_timer = MiniGESingleTimer(DIAMOND_ANIM_PERIOD)
    self.texture_idx = 0


  def load_diamond_textures(self, color, texture_list):
    if len(texture_list) > 0:
      return len(texture_list) # already loaded by other instance

    p = TEXTURE_PATH.replace("COLOR", color)
    for i in range(1, 18):
      i_txt = "%04d" % i
      pp = p.replace("NNNN", i_txt)
      print("texture path: " + pp)
      img= load_image(pp)
      txt = load_texture_from_image(img)
      texture_list.append(txt)
    len(texture_list)


  def on_draw_canvas(self, timestamp):
    pass

  def on_init(self):
    self.num_textures = self.load_diamond_textures(self.color, self.textures)

  def on_slice(self, timestamp):
    if self.animation_timer.has_expired() == True:
      self.animation_timer.preset(DIAMOND_ANIM_PERIOD)
      self.texture_idx += 1
      if self.texture_idx >= len(self.textures):
        self.texture_idx = 0

  def on_draw_2d(self, timestamp):
    diamond_texture = self.textures[self.texture_idx]

    diamond_source = Rectangle(0,0, diamond_texture.width, diamond_texture.height)
    diamond_dest = Rectangle( self.position.x + DIAMOND_POS_OFFSET_X, 
      self.position.y + DIAMOND_POS_OFFSET_Y, 
      diamond_texture.width/SCALE_DOWN, diamond_texture.height/SCALE_DOWN)

    diamond_ori = Vector2(diamond_texture.width/8, diamond_texture.height/8)
    draw_texture_pro(diamond_texture, diamond_source,  diamond_dest, diamond_ori, 0, WHITE)

# def test():
#   init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Raylib Python game")
#   set_target_fps(60)
#   d = Diamond("blue", None)
