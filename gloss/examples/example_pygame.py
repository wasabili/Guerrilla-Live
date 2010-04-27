from pygame import *
from gloss import *

class GlossTest(GlossGame):
	def load_content(self):
		img = image.load("content/target.png")
		self.target = Texture(img)
		
	def draw(self):
		Gloss.clear(Color.BLACK)

		mousepos = mouse.get_pos()
		display.set_caption("Pygame Example - " + str(mousepos))

		self.target.draw(mousepos, origin = None)
		
game = GlossTest("Pygame Example")
game.run()
