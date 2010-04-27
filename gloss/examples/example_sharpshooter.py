from gloss import *
 
class Target(object):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.sin_val = 0
		self.x_speed = 0
		self.hit_time = -1
 
class Sharpshooter(GlossGame):
	def load_content(self):
		self.sfc_background = Texture("content/sharpshooter.png")
		self.sfc_target = Texture("content/target.png")
		self.targets = []
		self.last_created_time = 0
		self.create_delay = 800
		self.target_speed = 350.0
		self.target_radius = self.sfc_target.half_width
		self.num_targets = 0
		self.num_hit = 0
 
		self.on_mouse_up = self.handle_mouse_clicks
 
	def draw(self):
		self.sfc_background.draw((0, 0))
 
		for target in self.targets:
			if target.hit_time != -1:
				diff = (Gloss.tick_count - target.hit_time) / 150.0
				if (diff > 1): diff = 1
				self.sfc_target.draw((target.x, target.y), origin = None, color = Color(1.0, 1.0, 1.0, Gloss.smooth_step(1.0, 0, diff)), scale = 1.0 - diff)
			else:
				self.sfc_target.draw((target.x, target.y), origin = None, color = Color.WHITE)
 
	def update(self):
		if (self.last_created_time + self.create_delay < Gloss.tick_count):
			action = Gloss.rand_float(0, 10)
 
			if (action < 5):
				self.create_target()
			elif (action < 7):
				self.create_target()
				self.create_target()
			elif (action < 8):
				self.create_target()
				self.create_target()
				self.create_target()
 
		for target in reversed(self.targets):
			if (target.y > Gloss.screen_resolution[1] + self.target_radius):
				self.targets.remove(target)
				continue
 
			if (target.hit_time != -1 and target.hit_time + 150 < Gloss.tick_count):
				self.targets.remove(target)
				continue
 
			target.y += self.target_speed * Gloss.elapsed_seconds
			target.x_speed += math.sin(target.sin_val) * Gloss.elapsed_seconds * 4
			target.x += target.x_speed
			target.sin_val += 1.5 * Gloss.elapsed_seconds
 
	def create_target(self):
		target = Target()
		target.x = Gloss.rand_float(0, Gloss.screen_resolution[0] - 150)
		target.y = -128
		target.sin_val = Gloss.rand_float(0, 36000) / 100
		self.targets.append(target)
 
		self.last_created_time = Gloss.tick_count
		self.create_delay = self.create_delay - 1
		self.target_speed = self.target_speed + 1
		self.num_targets = self.num_targets + 1
 
	def handle_mouse_clicks(self, event):
		for target in self.targets:
			if (target.hit_time != -1): continue
			distance = Point.distance((event.pos[0], event.pos[1]), (target.x, target.y))
 
			if (distance < self.target_radius):
				target.hit_time = Gloss.tick_count
				self.num_hit = self.num_hit + 1
 
game = Sharpshooter("Sharpshooter")
Gloss.screen_resolution = 640,640
game.run()
