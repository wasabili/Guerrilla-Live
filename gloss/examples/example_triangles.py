from gloss import *

class GlossTest(GlossGame):
	def draw(self):
		Gloss.clear(Color.lerp2(Color.CORNFLOWER_BLUE, Color.BLACK, game.bgshift))
				
		for i in range(0, 360, 20):
			xmoveleft = math.cos((i - 5) * math.pi / 180) * 800
			ymoveleft = math.sin((i - 5) * math.pi / 180) * 800

			xmoveright = math.cos((i + 5) * math.pi / 180) * 800
			ymoveright = math.sin((i + 5) * math.pi / 180) * 800

			Gloss.draw_triangle(points = [(0, 0), (xmoveleft, ymoveleft), (xmoveright, ymoveright)], position = (640, 360), rotation = game.rot, color = Color(1.0, 1.0, 1.0, 0.1))
		
		Gloss.draw_triangle(points = [(0,0), (100, 200), (-100, 200)], position = (200,200), color = Color.RED, rotation = -game.rot / 2, origin = None)
		Gloss.draw_triangle(points = [(0,0), (100, 200), (-100, 200)], position = (200,520), color = Color.RED, rotation = -game.rot / 2, origin = None)
		Gloss.draw_triangle(points = [(0,0), (100, 200), (-100, 200)], position = (1080,200), color = Color.RED, rotation = game.rot / 2, origin = None)
		Gloss.draw_triangle(points = [(0,0), (100, 200), (-100, 200)], position = (1080,520), color = Color.RED, rotation = game.rot / 2, origin = None)

		
		game.rot += 0.2
		game.bgshift += 0.0025
		
		if (game.bgshift > 1):
			game.bgshift = 0.0

game = GlossTest("Triangles test")
game.rot = 0.0
game.bgshift = 0.0
game.run()
