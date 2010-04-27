from gloss import *
import time

class GlossTest(GlossGame):
	def preload_content(self):
		self.background = Texture("content/background.jpg")
		self.font = SpriteFont("content/freesans.ttf", 60)

	def draw_loading_screen(self):
		self.background.draw()

		size = self.font.measure_string("Please wait...")
		self.font.draw("Please wait...", (Gloss.screen_resolution[0] - size[0] - 20, Gloss.screen_resolution[1] - size[1] - 20))

	def load_content(self):
		time.sleep(3)

	def draw(self):
		Gloss.clear(Color.BLACK)

game = GlossTest("Loading screen test")
Gloss.screen_resolution = (1280,720)
game.run()
