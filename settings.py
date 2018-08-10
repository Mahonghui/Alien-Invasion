class Settings():
	'''存储《外星人入侵》的所有设置的类'''

	def __init__(self):

		self.width=1200
		self.height=800
		self.bg_color = (230, 230, 230)
		

		
		self.bullet_width = 100
		self.bullet_height = 15
		self.bullet_color = 255, 0 , 100
		self.bullets_allowed = 3

		
		self.fleet_drop_speed = 20
		self.ship_limit = 3

		self.speed_scale = 1.1
		self.score_scale = 1.5

		self.init_dynamic_setting()

	def init_dynamic_setting(self):
		self.ship_speed_factor = 4
		self.bullet_speed_factor = 5
		self.alien_speed_factor = 2
		self.alien_points = 50

		self.fleet_direction = 1

	def increase_speed(self):
		self.ship_speed_factor *= self.speed_scale
		self.bullet_speed_factor *= self.speed_scale
		self.alien_speed_factor *= self.speed_scale

		self.alien_points = int(self.score_scale*self.alien_points)





