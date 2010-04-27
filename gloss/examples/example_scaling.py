from gloss import *
import time

class GlossTest(GlossGame):
	def load_content(self):
		self.tex_target = Texture("content/target.png")

	def draw(self):
		Gloss.clear(Color.BLACK)

		self.tex_target.draw(position = (256, 256), scale = Gloss.smooth_step2(1.0, 2.0, self.scale), origin = None)
		
		self.scale += 0.01
		
		if (self.scale > 1.0):
			self.scale = 0.0

	def target_clicked(self, target):
		pos = self.get_target_position()
		self.sprite_target.move_to(pos[0], pos[1])

game = GlossTest("Scaling test")
game.scale = 0.0
Gloss.screen_resolution = (512,512)
game.run()
