from pygame import image, Rect
from gameRole import Player, Enemy

class Pool(object):
	""" Creation/obtaining new game objects. """
	def __init__(self):
		self.plane = image.load('resources/image/shoot.png')

	def create_player(self, position):
		player_rect = []
		player_rect.append(Rect(0, 99, 102, 126))        # Player sprite picture area
		player_rect.append(Rect(165, 360, 102, 126))
		player_rect.append(Rect(165, 234, 102, 126))     # Player explodes sprite image area
		player_rect.append(Rect(330, 624, 102, 126))
		player_rect.append(Rect(330, 498, 102, 126))
		player_rect.append(Rect(432, 624, 102, 126))
		return Player(self.plane, player_rect, position)

	def create_enemy(self, position):
		enemy1_rect = Rect(534, 612, 57, 43)
		enemy1_img = self.plane.subsurface(enemy1_rect)
		enemy1_down_imgs = []
		enemy1_down_imgs.append(self.plane.subsurface(Rect(267, 347, 57, 43)))
		enemy1_down_imgs.append(self.plane.subsurface(Rect(873, 697, 57, 43)))
		enemy1_down_imgs.append(self.plane.subsurface(Rect(267, 296, 57, 43)))
		enemy1_down_imgs.append(self.plane.subsurface(Rect(930, 697, 57, 43)))
		return Enemy(enemy1_img, enemy1_down_imgs, position)