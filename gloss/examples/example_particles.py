from gloss import *

class GlossTest(GlossGame):
	def load_content(self):
		self.tex_cloud = Texture("content/cloud.png")
		self.tex_fire = Texture("content/fire.png")
		self.tex_gem = Texture("content/gem_green.png")
		self.tex_marble = Texture("content/marble_yellow.png")
		self.tex_smoke = Texture("content/smoke.tga")
		self.tex_star = Texture("content/star.png")

		self.part_cloud = ParticleSystem(self.tex_cloud, onfinish = self.particle_system_finished, position = self.random_position(), name = "cloud", initialparticles = 0, creationspeed = 100, lifespan = 10000, drag = 3)
		self.part_fire = ParticleSystem(self.tex_fire, onfinish = self.particle_system_finished, position = self.random_position(), name = "fire", initialparticles = 250, particlelifespan = 750, drag = 8, minspeed = 50, maxspeed = 300)
		self.part_gem = ParticleSystem(self.tex_gem, onfinish = self.particle_system_finished, position = self.random_position(), name = "gem", initialparticles = 15, growth = -1.0, particlelifespan = 10000, maxspeed = 20, minspeed = 8)
		self.part_marble = ParticleSystem(self.tex_marble, onfinish = self.particle_system_finished, position = self.random_position(), name = "marble", minspeed = 200, maxspeed = 200)
		self.part_smoke = ParticleSystem(self.tex_smoke, onfinish = self.particle_system_finished, position = self.random_position(), name = "smoke", initialparticles = 0, lifespan = 30000, creationspeed = 10, growth = 4.0, wind = (50,0), minspeed = 5, maxspeed = 50)
		self.part_star = ParticleSystem(self.tex_star, onfinish = self.particle_system_finished, position = self.random_position(), name = "star", maxrotation = 360, minscale = 0.1, maxscale = 1.0, drag = 1, particlelifespan = 1300)
		
		self.part_smoke.additive = True
		self.part_fire.additive = True

	def draw(self):
		Gloss.clear(Color.BLACK)
		self.part_cloud.draw()
		self.part_fire.draw()
		self.part_gem.draw()
		self.part_marble.draw()
		self.part_smoke.draw()
		self.part_star.draw()

	def random_position(self):
		return (Gloss.rand_float(0, 1280), Gloss.rand_float(0, 720))

	def particle_system_finished(self, ps):
		new = ParticleSystem(texture = ps.texture, position = self.random_position(), lifespan = ps.lifespan, creationspeed = ps.creation_speed, initialparticles = ps.initial_particles, particlelifespan = ps.particle_lifespan, minspeed = ps.particle_speed_min, maxspeed = ps.particle_speed_max, minrotation = ps.particle_rotation_min, maxrotation = ps.particle_rotation_max, minscale = ps.particle_scale_min, maxscale = ps.particle_scale_max, growth = ps.particle_growth, wind = ps.particle_wind, drag = ps.particle_drag, startcolor = ps.start_color, endcolor = ps.end_color, onfinish = self.particle_system_finished, name = ps.name)

		if ps.name == "cloud":
			self.part_cloud = new
		if ps.name == "fire":
			self.part_fire = new
			new.additive = True
		if ps.name == "gem":
			self.part_gem = new
		if ps.name == "marble":
			self.part_marble = new
		if ps.name == "smoke":
			self.part_smoke = new
			new.additive = True
		if ps.name == "star":
			self.part_star = new


game = GlossTest("Particle system test")
game.run()
