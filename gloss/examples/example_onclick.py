from gloss import *
import time

class GlossTest(GlossGame):
	def get_target_position(self):
		return (Gloss.rand_float(0, Gloss.screen_resolution[0] - self.tex_target.width), Gloss.rand_float(0, Gloss.screen_resolution[1] - self.tex_target.height))

	def load_content(self):
		self.background = Texture("content/background.jpg")
		self.tex_target = Texture("content/target.png")
		self.sprite_target = Sprite(self.tex_target, self.get_target_position())
		self.sprite_target.on_click = self.target_clicked

	def draw(self):
		Gloss.fill(self.background)

		self.sprite_target.draw()

	def target_clicked(self, target):
		pos = self.get_target_position()
		self.sprite_target.move_to(pos[0], pos[1])

game = GlossTest("On click test")
Gloss.screen_resolution = (1280,720)
game.run()
