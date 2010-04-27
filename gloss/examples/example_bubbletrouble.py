from pygame.locals import *

from gloss import *

class BubbleTrouble_Bubble:
	pass


class BubbleTroubleGame(GlossGame):
	max_number = 0 # the highest bubble number already used
	direction_pos = 0 # the last direction used from the list

	bubbles = [] # all the active bubbles right now

	def load_content(self):
		self.bubble_types = []

		self.bubble_types.append(Texture("content/marble_blue.png"))
		self.bubble_types.append(Texture("content/marble_green.png"))
		self.bubble_types.append(Texture("content/marble_purple.png"))
		self.bubble_types.append(Texture("content/marble_red.png"))
		self.bubble_types.append(Texture("content/marble_yellow.png"))

		self.texWrong = Texture("content/red_cross.png")

		self.bubble_size = self.bubble_types[0].width
		self.bubble_half_size = self.bubble_size / 2

		self.directions = []

		self.font_main = SpriteFont("content/freesans.ttf", 40)

		for i in range(360):
			if (i < 10): continue
			if (i >= 350): continue
			if (i > 80 and i < 100): continue
			if (i > 170 and i < 190): continue
			if (i > 260 and i < 280): continue

			self.directions.append(i)

		random.shuffle(self.directions)

		for i in range(15):
			self.create_bubble(False)
	
	def create_bubble(self, offscreen):
		self.max_number += random.randint(1, 4)
		bubble = BubbleTrouble_Bubble()

		bubble.popped_time = -1
		bubble.last_wrong = -1000

		# pick a random bubble texture
		tex = random.randint(0, len(self.bubble_types) - 1)
		bubble.sprite = Sprite(self.bubble_types[tex])

		# the easy way to implement bubble clicking is to use on_click for sprites, but:
		#	a) that's slow and for last resort use only
		#	 and
		#	b) it's just not accurate - we're dealing with circles here!
		#
		# here's what the on_click assignment would have looked like:
		# bubble.sprite.on_click = self.click_bubble
		#
		# but instead we're using own function that's faster and more accurate - look for the on_mouse_up event
		# assignment near the bottom of this script

		# this next bit works fine with on_click or with the custom method
		bubble.sprite.parent = bubble # so when the sprite is clicked when can refer to the bubble it belongs to

		if (offscreen):
			if random.randint(0, 1) == 0:
				# coming in from the top or bottom
				bubble.sprite.move_to(random.randint(0, Gloss.screen_resolution[0]), -self.bubble_types[0].height)
			else:
				# come in from the left or right
				bubble.sprite.move_to(-self.bubble_types[0].width, random.randint(0, Gloss.screen_resolution[1]))
		else:
			bubble.sprite.move_to(random.randint(0, Gloss.screen_resolution[0]), random.randint(0, Gloss.screen_resolution[1]))

		bubble.speed = random.randint(70, 120)

		bubble.number = self.max_number
		bubble.direction = self.choose_bubble_direction()

		bubble.number_string = str(bubble.number)
		self.bubbles.append(bubble)

		self.last_created_time = Gloss.tick_count

	def choose_bubble_direction(self):
		self.direction_pos += 1

		if self.direction_pos == len(self.directions):
			self.direction_pos = 0

		return self.directions[self.direction_pos]

	def draw(self):
		Gloss.clear(Color(0.2, 0.2, 0.9))

		for bubble in self.bubbles:
			pos = self.font_main.measure_string(bubble.number_string)

			if bubble.popped_time != -1:
				diff = (Gloss.tick_count - bubble.popped_time) / 150.0
				if (diff > 1): diff = 1
				bubble.sprite.draw(color = Color(1, 1, 1, Gloss.lerp(0.9, 0, diff)))
				self.font_main.draw(bubble.number_string, position = ((bubble.sprite.position[0] + self.bubble_half_size) - (pos[0] / 2.0), (bubble.sprite.position[1] + self.bubble_half_size) - (pos[1] / 2.0)), color = Color(0, 0, 0, Gloss.lerp(210, 0, diff)))
			else:
				bubble.sprite.draw(color = Color(1, 1, 1, 0.9))
				self.font_main.draw(bubble.number_string, position = ((bubble.sprite.position[0] + self.bubble_half_size) - (pos[0] / 2.0), (bubble.sprite.position[1] + self.bubble_half_size) - (pos[1] / 2.0)), color = Color.BLACK)

				if (bubble.last_wrong + 250 > Gloss.tick_count):
					self.texWrong.draw(position = (bubble.sprite.position[0], bubble.sprite.position[1]))

	def update(self):
		if self.last_created_time + 8000 < Gloss.tick_count:
			self.create_bubble(True)

		for bubble in self.bubbles:
			xmove = (math.cos(bubble.direction * math.pi / 180) * bubble.speed) * Gloss.elapsed_seconds
			ymove = (math.sin(bubble.direction * math.pi / 180) * bubble.speed) * Gloss.elapsed_seconds

			bubble.sprite.move(xmove, ymove)

			if bubble.sprite.position[0] > Gloss.screen_resolution[0]:
				bubble.sprite.move_to(-self.bubble_size, None)
			elif bubble.sprite.position[0] < -self.bubble_size:
				bubble.sprite.move_to(Gloss.screen_resolution[0], None)

			if bubble.sprite.position[1] > Gloss.screen_resolution[1]:
				bubble.sprite.move_to(None, -self.bubble_size)
			elif bubble.sprite.position[1] < -self.bubble_size:
				bubble.sprite.move_to(None, Gloss.screen_resolution[1])

		self.clean_up_bubbles()

	def clean_up_bubbles(self):
		for bubble in reversed(self.bubbles):
			if bubble.popped_time != -1 and bubble.popped_time + 150 < Gloss.tick_count:
				self.bubbles.remove(bubble)


	def click_bubble(self, clicked):
		for bubble in reversed(self.bubbles):
			if bubble.number < clicked.parent.number:
				clicked.parent.last_wrong = Gloss.tick_count

				if len(self.bubbles) > 20:
					# we already have lots of bubbles - don't create any more!
					return

				self.create_bubble(True)

				# now make the correct bubble change direction to help the player out
				bubble.direction = self.choose_bubble_direction()

				return

		# if we're still here, this bubble was the correct one!
		clicked.parent.popped_time = Gloss.tick_count

	def handle_mouse_clicks(self, event):
		# because we're dealing with circles, the fastest and most accurate way to spot clicks on bubbles is to use Pythagoras's theorem
		# we need to loop over every variable in order (lowest first to avoid player annoyance)
		for bubble in self.bubbles:
			# 1: calculate the bubble's centre
			bubble_cx = bubble.sprite.position[0] + self.bubble_half_size
			bubble_cy = bubble.sprite.position[1] + self.bubble_half_size
        
			# 2: now see how far away our click was
			dist_x = bubble_cx - event.pos[0]
			dist_y = bubble_cy - event.pos[1]
        
			# 3: calculate the hypotenuse squared
			dist = dist_x * dist_x + dist_y * dist_y
        
			# 4: if the distance is less than our radius squared, it was clicked!
			if dist < self.bubble_size * self.bubble_size:
				# this bubble was clicked - check whether it was correct then stop checking other bubbles
				self.click_bubble(bubble.sprite)
				return


random.seed()
game = BubbleTroubleGame("Bubble Trouble - click the lowest-numbered bubbles!")
Gloss.screen_resolution = 1280,720
# uncomment the next line to turn on multisampling - not all GPUs support it, though!
#Gloss.enable_multisampling = True
game.on_mouse_up = game.handle_mouse_clicks
game.run()
