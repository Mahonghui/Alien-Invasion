import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien

def get_number_alien(ai_setting, alien_width):

	available_x = ai_setting.width - (2*alien_width)
	number_alien = int(available_x /(2*alien_width))
	return number_alien

def create_alien(aliens, number_alien, row_numer, alien_width, ai_setting,  screen):

	for number in range(number_alien):
		alien = Alien(ai_setting, screen)
		alien.x = alien_width + 2*alien_width * number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2*alien.rect.height*row_numer
		aliens.add(alien)


def create_fleet(ai_setting, screen, aliens, ship):

	alien = Alien(ai_setting, screen)
	alien_width = alien.rect.width

	number_alien = get_number_alien(ai_setting, alien_width)
	number_rows = get_number_rows(ai_setting, ship.rect.height, alien.rect.height)

	for row_number in range(number_rows):
		create_alien(aliens, number_alien, row_number, alien_width, ai_setting, screen)

def get_number_rows(ai_setting, ship_height, alien_height):
	available_y = (ai_setting.height - 3*alien_height - ship_height)
	number_rows = int(available_y / (2*alien_height))

	return number_rows


def key_up_event(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def key_down_event(ai_setting, event, ship, screen, bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_setting, screen, ship, bullets)

def check_events(ai_setting, screen, aliens, ship, bullets, play_button, stats):

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYUP:
			key_up_event(event, ship)
		elif event.type == pygame.KEYDOWN:
			key_down_event(ai_setting, event, ship, screen, bullets)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_setting, screen, stats, ship, aliens, bullets, play_button, mouse_x, mouse_y)


def check_play_button(ai_setting, screen, stats, ship, aliens, bullets, play_button, mouse_x, mouse_y):

	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active = True

		aliens.empty()
		bullets.empty()

		create_fleet(ai_setting, screen, aliens, ship)
		ship.center_ship()

def fire_bullet(ai_setting, screen, ship, bullets):
	if len(bullets) < ai_setting.bullets_allowed:
		new_bullet = Bullet(ai_setting, screen, ship)
		bullets.add(new_bullet)

def update_bullets(ai_setting, screen, bullets, aliens, ship, stats, sb):
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_collision(ai_setting, screen, aliens, bullets, ship, stats, sb)

	

def check_collision(ai_setting, screen, aliens, bullets, ship, stats, sb):
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

	if collisions:
		for aliens in collisions.values():
			stats.score += ai_setting.alien_points*len(aliens)
			sb.prep_score()
			check_high_score(stats, sb)

	if len(aliens) == 0:
		bullets.empty()
		ai_setting.increase_speed()
		create_fleet(ai_setting, screen, aliens, ship)


def update_screen(ai_setting, screen, ship, aliens, bullets, stats, play_button, sb):


	screen.fill(ai_setting.bg_color)

	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	sb.show_score()
	if not stats.game_active:
		play_button.draw_button()
	pygame.display.flip()



def update_aliens(ai_setting, stats, screen, aliens, ship, bullets):
	check_fleet_edge(ai_setting, aliens)
	aliens.update()

	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_setting, stats, screen, aliens, ship, bullets)

def ship_hit(ai_setting, stats, screen, aliens, ship, bullets):
	if stats.ship_left >0:
		stats.ship_left -=1

		aliens.empty()
		bullets.empty()

		create_fleet(ai_setting, screen, aliens, ship)
		ship.center_ship()

		sleep(2)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		ai_setting.init_dynamic_setting()


def check_fleet_edge(ai_setting, aliens):
	for alien in aliens.sprites():
		if alien.check_edge():
			change_fleet_direction(ai_setting, aliens)
			break

def change_fleet_direction(ai_setting, aliens):
	for alien in aliens:
		alien.rect.y += ai_setting.fleet_drop_speed
	ai_setting.fleet_direction *=-1
	

def check_high_score(stats, sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()



