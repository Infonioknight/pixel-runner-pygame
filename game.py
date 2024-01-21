import pygame
from sys import exit
from random import randint, choice
import player, obstacle

def display_score():
    current_time = pygame.time.get_ticks()
    calculated = (current_time - start_time) // 1000
    score_surf = pixel_font.render(f'Score: {calculated}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return calculated

def collision_sprite():
    global score, highscores
    if pygame.sprite.spritecollide(player_instance.sprite, obstacle_group, False):
        obstacle_group.empty()
        highscores.append(score)
        highscores.sort(reverse=True)
        highscores = highscores[:8] if len(highscores) > 8 else highscores

        leaderboard = open('scores.txt', 'w')
        for index, record in enumerate(highscores):
            leaderboard.write(str(record))
            if index != len(highscores) - 1:
                leaderboard.write('\n')
        leaderboard.close()
        return False
    else: return True

# Run before everything, initiates all subparts of pygame.
pygame.init()
screen = pygame.display.set_mode((800, 400)) 
pygame.display.set_caption('First Game!')
clock = pygame.time.Clock()

pixel_font = pygame.font.Font('./font/PixelType.ttf', 50) 
pixel_font_hs = pygame.font.Font('./font/PixelType.ttf', 45)
pixel_font_exit = pygame.font.Font('./font/PixelType.ttf', 30)

game_active = False
highscore_screen = False
start_time = 0
score = 0

bg_music = pygame.mixer.Sound('./audio/music.wav')
bg_music.set_volume(0.25)
bg_music.play(loops= -1)

sky_surface = pygame.image.load('./graphics/Sky.png').convert()
ground_surface = pygame.image.load('./graphics/Ground.png').convert()

player_instance = pygame.sprite.GroupSingle()
player_instance.add(player.Player())

obstacle_group = pygame.sprite.Group()

# Intro Screen
player_stand = pygame.image.load('./graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 165))

title_text = pixel_font.render('Pixel Runner', False, (111, 196, 169))
title_rect = title_text.get_rect(center = (400, player_stand_rect.top - 30))

instruction_text = pixel_font.render('Press Space to begin!', False, (111, 196, 169))
instruction_rect = instruction_text.get_rect(center = (400, player_stand_rect.bottom + 40))

highscore_instructions = pixel_font.render('Press  H  to  get  the  leaderboards', False, (111, 196, 169))
highscore_instructions_rect = highscore_instructions.get_rect(center = (400, instruction_rect.bottom + 40))

# Highscore screen
hs_title = pixel_font.render('Highscores', False, (111, 196, 169))
hs_title_rect = hs_title.get_rect(center = (400, 80))
highscores = [int(score) for score in open('scores.txt', 'r').read().split('\n')]

exit_key = pixel_font_exit.render('Esc', False, (111, 196, 169))
exit_key_rect = exit_key.get_rect(center = (50, 30))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:          
            if event.type == obstacle_timer:
                obstacle_group.add(obstacle.Obstacle(choice(['fly', 'snail', 'snail'])))
        
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and highscore_screen == False:
                    game_active = True
                    start_time = pygame.time.get_ticks()
                
                if event.key == pygame.K_h:
                    highscore_screen = True
                
                if event.key == pygame.K_ESCAPE and highscore_screen == True:
                    highscore_screen = False
               

    # Block img transfer (placing one image on the other)
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        player_instance.draw(screen)
        player_instance.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collisions
        game_active = collision_sprite()

        # Score
        score = display_score()
    
    elif game_active == False and highscore_screen == False:
        screen.fill((94, 129, 162))
        screen.blit(title_text, title_rect)

        score_message = pixel_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, player_stand_rect.bottom + 50))
        screen.blit(player_stand, player_stand_rect)

        if score == 0: screen.blit(instruction_text, instruction_rect)
        else: screen.blit(score_message, score_message_rect)

        screen.blit(highscore_instructions, highscore_instructions_rect)
    
    elif game_active == False and highscore_screen == True:
        screen.fill((94, 129, 162))
        screen.blit(hs_title, hs_title_rect)
        screen.blit(exit_key, exit_key_rect)
        pygame.draw.rect(screen, (111, 196, 169), exit_key_rect.inflate(10, 10), 2, border_radius=5)
        for index, record in enumerate(highscores):
            record_text = pixel_font_hs.render(f'{index+1}. {record}', False, (111, 196, 169))
            record_text_rect = record_text.get_rect(bottomleft = (378, hs_title_rect.bottom + (35 * (index + 1))))
            screen.blit(record_text, record_text_rect)
            
    pygame.display.update()
    clock.tick(60) # Loop shouldn't run faster than 60 times per second.