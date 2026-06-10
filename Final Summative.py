#Matteo Cirstea
#June 12, 2026
#ICS3U0
#Mr Farooqi
#Platform jumping game. Start the game for instructions





import pygame
import random
import sys

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60


PLAYER_COLOR = ("#154CE3")
ISLAND_COLOR = ("#07B516") 
HEAL_COLOR = ("#FFCC00")
BOMB_COLOR = ('#000000')
TEXT_COLOR = ('#000000')

GRAVITY = 0.6
JUMP_STRENGTH = -14
PLAYER_SPEED = 8
SCROLL_SPEED = 2   

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Island Jumper")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 40)
background = pygame.image.load("BackgroundImage.png").convert()


hpgain = pygame.mixer.Sound('sounds/hpgain.wav')
hploss = pygame.mixer.Sound('sounds/hploss.wav')
death = pygame.mixer.Sound('sounds/death.wav')
jump = pygame.mixer.Sound('sounds/jump.wav')



game_state = "MENU"

def reset_game():
    global player_rect, player_change_x, player_change_y, player_lives, player_on_ground
    global islands, items, score, game_over
    
    player_rect = pygame.Rect(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 220, 40, 40)
    player_change_x = 0
    player_change_y = 0
    player_lives = 3
    player_on_ground = False
    
    islands = []
    items = []
    
    start_width = random.randint(100, 150)
    start_island = {
        "rect": pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 170, start_width, 20),
        "speed": 1
    }
    islands.append(start_island)
    
    score = 0
    game_over = False

reset_game()
pygame.time.set_timer(pygame.USEREVENT, 1500) 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.USEREVENT and game_state == "PLAYING" and not game_over:
            spawn_x = random.randint(0, SCREEN_WIDTH - 120)
            isl_width = random.randint(100, 150)
            new_island = {
                "rect": pygame.Rect(spawn_x, -20, isl_width, 20),
                "speed": SCROLL_SPEED
            }
            islands.append(new_island)
            
            if random.random() < 0.3:
                item_type = random.choice(["heart", "bomb"])
                item_rect = pygame.Rect(0, 0, 15, 15)
                item_rect.centerx = new_island["rect"].centerx
                item_rect.bottom = new_island["rect"].top
                new_item = {
                    "rect": item_rect,
                    "type": item_type,
                    "island": new_island
                }
                items.append(new_item)
                
            score += 1 

        if event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                
                if event.key == pygame.K_SPACE:
                    reset_game()
                    game_state = "PLAYING"
            elif game_state == "PLAYING" and game_over:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_m:
                    game_state = "MENU"

    keys = pygame.key.get_pressed()
    
    if game_state == "PLAYING" and not game_over:
        
        if keys[pygame.K_LEFT]:
            player_change_x = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT]:
            player_change_x = PLAYER_SPEED
        else:
            player_change_x = 0
            
        if keys[pygame.K_UP] and player_on_ground:
            jump.play()
            player_change_y = JUMP_STRENGTH
            player_on_ground = False

    if game_state == "PLAYING" and not game_over:
        player_change_y += GRAVITY
        player_rect.x += player_change_x
        
        if player_rect.left > SCREEN_WIDTH:
            player_rect.right = 0
        elif player_rect.right < 0:
            player_rect.left = SCREEN_WIDTH
        
        player_rect.y += player_change_y

        for island in islands[:]:
            island["rect"].y += island["speed"]
            if island["rect"].top > SCREEN_HEIGHT:
                islands.remove(island)

        for item in items[:]:
            item["rect"].bottom = item["island"]["rect"].top
            if item["rect"].top > SCREEN_HEIGHT or item["island"] not in islands:
                items.remove(item)

        player_on_ground = False
        if player_change_y >= 0:
            for island in islands:
                if player_rect.colliderect(island["rect"]):
                    if player_rect.bottom <= island["rect"].top + player_change_y + island["speed"]:
                        player_rect.bottom = island["rect"].top
                        player_change_y = island["speed"]
                        player_on_ground = True

        for item in items[:]:
            if player_rect.colliderect(item["rect"]):
                if item["type"] == "heart":
                    player_lives += 1
                    hpgain.play()
                elif item["type"] == "bomb":
                    player_lives -= 1
                    hploss.play()
                    if player_lives <= 0:
                        game_over = True
                        
                items.remove(item)

        if player_rect.top > SCREEN_HEIGHT:
            game_over = True

    screen.blit(background,(0,0))

    if game_state == "MENU":
        title_text = title_font.render("ISLAND JUMPER", True, TEXT_COLOR)
        instr1 = font.render("How to Play:", True, TEXT_COLOR)
        instr2 = font.render("- Use LEFT / RIGHT arrows to move", True, TEXT_COLOR)
        instr3 = font.render("- Use UP arrow to jump", True, TEXT_COLOR)
        instr4 = font.render("- Collect yellow blocks for extra lives", True, TEXT_COLOR)
        instr5 = font.render("- Avoid black blocks and falling down", True, TEXT_COLOR)
        start_text = title_font.render("Press SPACE to Start", True, TEXT_COLOR)
        
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))
        screen.blit(instr1, (SCREEN_WIDTH // 2 - 150, 280))
        screen.blit(instr2, (SCREEN_WIDTH // 2 - 150, 320))
        screen.blit(instr3, (SCREEN_WIDTH // 2 - 150, 360))
        screen.blit(instr4, (SCREEN_WIDTH // 2 - 150, 400))
        screen.blit(instr5, (SCREEN_WIDTH // 2 - 150, 440))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 580))

    elif game_state == "PLAYING":
        for island in islands:
            pygame.draw.rect(screen, ISLAND_COLOR, island["rect"])

        for item in items:
            color = HEAL_COLOR if item["type"] == "heart" else BOMB_COLOR
            pygame.draw.rect(screen, color, item["rect"])

        if not game_over:
            pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        lives_text = font.render(f"Lives: {player_lives}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))

        if game_over:
            
            over_text = font.render("GAME OVER", True, BOMB_COLOR)
            restart_text = font.render("Press 'R' to Restart", True, TEXT_COLOR)
            menu_text = font.render("Press 'M' for Main Menu", True, TEXT_COLOR)
            screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
            screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(FPS)