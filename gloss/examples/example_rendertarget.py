import pygame
from pygame.locals import *

from gloss import *

class GlossTest(GlossGame):
	def load_content(self):
		self.tex_balloon = Texture("content/gem.png")
		self.background = Texture("content/background.jpg")
		self.Balloon = Sprite(self.tex_balloon)

		self.RT = RenderTarget(1024, 1024)

		self.spinner = 0.0
		self.on_key_up = self.handle_key_presses

	def update(self):
		self.spinner += 0.0025
		if (self.spinner > 1.0):
			self.spinner = 0.0

	def draw(self):
		Gloss.fill(top = Color.lerp(Color.WHITE, Color.BLACK, self.spinner), bottom = Color.lerp(Color.BLACK, Color.WHITE, self.spinner), vertical = False)

		self.RT.activate()
		Gloss.fill(self.background)
		self.Balloon.draw(position = (100, 100), scale = 3.0, color = Color(1.0, 1.0, 1.0, 0.5))
		self.RT.deactivate()

		self.RT.draw(position = (512, 384), width = 512, height = 512, rotation = self.spinner * 360, origin = None)
		
	# as an added bonus, add a sepia tint when spacebar is pressed
	def handle_key_presses(self, event):
		if event.key is K_SPACE:
			Gloss.set_scene_tint(Color.from_bytes(250, 210, 140, 255))


game = GlossTest("RenderTarget example - press Spacebar to add a sepia tint")
Gloss.screen_resolution = 1024,768
#enable this if you really want to push older GPUs to the limit!
#Gloss.enable_multisampling = True
game.run()
