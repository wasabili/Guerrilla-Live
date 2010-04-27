from gloss import *

class GlossTest(GlossGame):
	def load_content(self):
		self.tex_gem = Texture("content/gem.png")

		self.gems = []

		for i in range(1, 10):
			gem = Sprite(self.tex_gem, position = (i * 130, 600))
			gem.movetime = -i / 10.0
			gem.wobbletime =  gem.movetime
			self.gems.append(gem)

	def draw(self):
		Gloss.clear(Color.BLACK)

		for gem in self.gems:
			wobble = Gloss.smooth_step2(0, 60, gem.wobbletime)
			gem.draw(origin = None, rotation = 30 - wobble)

	def update(self):
		for gem in self.gems:
			gem.movetime += 0.005
			if (gem.movetime > 1.0): gem.movetime = 0.0

			gem.wobbletime += 0.009
			if (gem.wobbletime > 1.0): gem.wobbletime = 0.0

			gem.move_to(None, Gloss.smooth_step2(600, 100, gem.movetime))

game = GlossTest("Smooth step test")
game.run()
