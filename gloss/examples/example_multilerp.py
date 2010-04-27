from gloss import *

class GlossTest(GlossGame):
	def load_content(self):
		self.target = Texture("content/target.png")
	
	def draw(self):
		Gloss.clear(Color.BLACK)
		
		self.target.draw(position = Point.multi_lerp([(100, 100), (500, 100), (500, 500), (100, 500), (100, 100)], game.moveamount), origin = None)
		
		game.moveamount += 0.005
		
		if (game.moveamount > 1):
			game.moveamount = 0.0

game = GlossTest("Multi-lerp test")
game.moveamount = 0.0
Gloss.screen_resolution = 640,640
game.run()
