import os	

class GameStats():

	def __init__(self, ai_setting):
		self.ai_setting = ai_setting
		self.reset_stats()
		self.high_score = self.load_high_score('./high_score.txt')
		

	def reset_stats(self):
		self.ship_left = self.ai_setting.ship_limit
		self.score = 0
		self.game_active = False
		self.level = 1


	def load_high_score(self, filename):
		if not os.path.exists(filename):
			open(filename, 'w')
			
		if os.path.getsize(filename) == 0:
			high_score = 0
		else:
			with open('./high_score.txt', 'r') as f_obj:
				high_score = int(f_obj.readlines()[-1].split()[-1])
				f_obj.close()

		return high_score
