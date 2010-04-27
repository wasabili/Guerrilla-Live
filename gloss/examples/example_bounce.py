from gloss import *

class GlossTest(GlossGame):
	def load_content(self):
		self.tex_gem = Texture("content/gem.png")

		self.gems = []

		for i in range(1, 9):
			gem = Sprite(self.tex_gem, position = (i * 130, 600))
			gem.movetime = -i / 10.0
			self.gems.append(gem)

	def draw(self):
		Gloss.clear(Color.BLACK)

		for gem in self.gems:
			gem.draw()

	def update(self):
		for gem in self.gems:
			gem.movetime += 0.008
			if (gem.movetime > 1.0): gem.movetime = 0.0
			gem.move_to(None, Gloss.bounce_in(500, 200, gem.movetime, 30))

game = GlossTest("Bounce test")
game.run()
