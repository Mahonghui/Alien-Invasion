# coding: utf-8

import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

import game_functions as gf

def run_game():
	'''初始化游戏并创建一个对象'''
	pygame.init()

	ai_setting = Settings()
	screen = pygame.display.set_mode((ai_setting.width, ai_setting.height))
	pygame.display.set_caption('Alien Invasion')
	stats = GameStats(ai_setting)
	sb = ScoreBoard(ai_setting, screen, stats)

	play_button = Button(ai_setting, screen, 'Play')

	ship = Ship(ai_setting, screen)
	bullets = Group()
	aliens = Group()


	gf.create_fleet(ai_setting, screen, aliens, ship)

	while True:

		gf.check_events(ai_setting, screen, aliens, ship, bullets, play_button, stats)

		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_setting, screen, bullets, aliens, ship, stats, sb)
			gf.update_aliens(ai_setting, stats, screen, aliens, ship, bullets)
		gf.update_screen(ai_setting, screen, ship, aliens, bullets, stats, play_button, sb)


run_game()