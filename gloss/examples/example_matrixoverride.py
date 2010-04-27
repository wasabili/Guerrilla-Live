from gloss import *

class GlossTest(GlossGame):
	def draw(self):
		Gloss.clear(Color.BLACK)
		
		# by default, Gloss uses the identity matrix for all drawing
		# you can override that if you want, as shown below
		glLoadIdentity()
		glTranslatef(256, 256, 0)
		glScalef(self.scale * 2, self.scale * 2, 1.0)
		glRotatef(self.scale * 360, 0, 0, 1)
		
		# the rest of this code is straight from example_boxes.py
		Gloss.draw_box(position = (256, 256), width = 256, height = 128, scale = Gloss.smooth_step2(1.0, 2.0, self.scale), rotation = self.rot * 5, color = Color(1.0, 0.0, 0.0, 0.5), origin = None)		
		Gloss.draw_box(position = (256, 256), width = 256, height = 128, scale = Gloss.smooth_step2(1.0, 2.0, self.scale), rotation = self.rot * 4, color = Color(0.0, 1.0, 0.0, 0.5), origin = None)
		Gloss.draw_box(position = (256, 256), width = 256, height = 128, scale = Gloss.smooth_step2(1.0, 2.0, self.scale), rotation = self.rot * 3, color = Color(0.0, 0.0, 1.0, 0.5), origin = None)
		Gloss.draw_box(position = (256, 256), width = 256, height = 128, scale = Gloss.smooth_step2(1.0, 2.0, self.scale), rotation = self.rot * 2, color = Color(1.0, 1.0, 0.0, 0.5), origin = None)
		Gloss.draw_box(position = (256, 256), width = 256, height = 128, scale = Gloss.smooth_step2(1.0, 2.0, self.scale), rotation = self.rot, color = Color(0.0, 1.0, 1.0, 0.5), origin = None)
		Gloss.draw_box(position = (256, 256), width = 256, height = 128, scale = Gloss.smooth_step2(1.0, 2.0, self.scale), rotation = self.rot * 0.5, color = Color(1.0, 0.0, 1.0, 0.5), origin = None)
		
		self.rot += 0.3
		self.scale += 0.01
		if self.scale > 1.0:
			self.scale = 0
		
game = GlossTest("Matrix override")
game.rot = 0.0
game.scale = 0.0
Gloss.screen_resolution = (512, 512)
game.run()
