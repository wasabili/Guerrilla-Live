from gloss import *

class GlossTest(GlossGame):
	def load_content(self):
		self.dots = []
		
		# create points for our lines
		for i in range(1, 30):
			self.dots.append(Dot())
	
	def update(self):
		# move all the dots, bouncing off the window edges as needed
		for dot in self.dots:
			dot.X += dot.XSpeed
			dot.Y += dot.YSpeed
			
			if dot.X < 0:
				dot.X = 0
				dot.XSpeed = -dot.XSpeed
			elif dot.X > Gloss.screen_resolution[0]:
				dot.X = Gloss.screen_resolution[0]
				dot.XSpeed = -dot.XSpeed
				
			if dot.Y < 0:
				dot.Y = 0
				dot.YSpeed = -dot.YSpeed
			elif dot.Y > Gloss.screen_resolution[1]:
				dot.Y = Gloss.screen_resolution[1]
				dot.YSpeed = -dot.YSpeed


	def draw(self):
		Gloss.clear(Color.BLACK)
		
		self.colorlerp += 0.002
		if self.colorlerp > 1.0:
			self.colorlerp = 0.0
		
		# draw four edges to the screen
		Gloss.draw_line((0, 0), (Gloss.screen_resolution[0], 0), Color.RED, 40.0)
		Gloss.draw_line((0, Gloss.screen_resolution[1]), (Gloss.screen_resolution[0], Gloss.screen_resolution[1]), Color.RED, 40.0)
		Gloss.draw_line((0, 0), (0, Gloss.screen_resolution[1]), Color.RED, 40.0)
		Gloss.draw_line((Gloss.screen_resolution[0], 0), (Gloss.screen_resolution[0], Gloss.screen_resolution[1]), Color.RED, 40.0)

		# draw the dots to the screen as line connections 
		lines = []
		
		for dot in self.dots:
			lines.append((dot.X, dot.Y))

		# to make things more interesting, let's make the lines color change all the time
		col = color = Color.multi_lerp([Color.WHITE, Color.BLACK, Color.RED, Color.BLACK, Color.GREEN, Color.BLACK, Color.BLUE, Color.BLACK, Color.RED, Color.BLACK, Color.WHITE], self.colorlerp)
		Gloss.draw_lines(lines, col, width = 3.0, join = True)
		
class Dot(object):
	def __init__(self):
		self.X = Gloss.rand_float(0, Gloss.screen_resolution[0])
		self.Y = Gloss.rand_float(0, Gloss.screen_resolution[1])
		self.XSpeed = Gloss.rand_float(-1, 1) * 3
		self.YSpeed = Gloss.rand_float(-1, 1) * 3

game = GlossTest("Lines test")
Gloss.screen_resolution = (1280,720)
game.colorlerp = 0.0
game.run()
