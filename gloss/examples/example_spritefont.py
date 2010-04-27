from gloss import *
import time

class GlossTest(GlossGame):
	def load_content(self):
		self.background = Texture("content/background.jpg")
		self.font = SpriteFont("content/freesans.ttf", 60)

		# this is the string we'll be using for all the drawing
		self.textstring = "He thrusts his fists\nagainst the posts\nand still insists\nhe sees the ghosts"

		# calculate the size of our string so we can centre it
		self.stringsize = self.font.measure_string(self.textstring)
		self.stringpos = (640 - (self.stringsize[0] / 2), 360 - (self.stringsize[1] / 2))

		# this number will be incremented to let us wobble the text and scale it
		self.textwobble = 0

	def draw(self):
		Gloss.clear(Color.BLACK)

		wobble = Gloss.smooth_step2(0, 60, self.textwobble)
		scale = Gloss.smooth_step2(0.8, 1.2, self.textwobble)

		# choose only a few letters from the total string, depending on how much time has passed
		num_letters = int(Gloss.smooth_step(0, len(self.textstring), self.textwobble))
		letters = self.textstring[0:num_letters + 1]

		self.font.draw(letters, self.stringpos, rotation = 30 - wobble, scale = scale)

	def update(self):
		self.textwobble += 0.005
		if (self.textwobble > 1.0): self.textwobble = 0.0

game = GlossTest("SpriteFont test")
Gloss.screen_resolution = (1280,720)
game.run()
