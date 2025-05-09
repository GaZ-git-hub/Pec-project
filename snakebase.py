import pygame
import sys
import random

# Inicializace Pygame
pygame.init()

# Velikost bunky, rozmery mrizky a obrazovky
Cell_Size = 20
Grid_Height = 20
Grid_Width = 30
Width = Cell_Size * Grid_Width
Height = Cell_Size * Grid_Height
screen = pygame.display.set_mode((Width, Height))  # Nastaveni okna
pygame.display.set_caption("Snake Game")  # Nazev okna
score = 0  # Pocatecni skore
font = pygame.font.SysFont(None, 30)  # Pismo pro text

clock = pygame.time.Clock()  # Hodiny pro spravu snimku za sekundu

# Funkce pro zobrazeni uvodni obrazovky s nazvem a instrukcemi
def show_start_menu():
    screen.fill("Black")  # Nastaveni pozadi na cerne
    title = font.render("Snake Game", True, (0, 255, 0))  # Vytvoreni textu "Snake Game"
    prompt = font.render("Press Spacebar to start", True, (255, 255, 255))  # Pokyn pro start
    prompt_q = font.render("Press Q to quit", True, (255, 255, 255))  # Pokyn pro quit
    screen.blit(title, title.get_rect(center=(Width // 2, Height // 4 - 20)))  # Zobrazeni nazvu ve stredu obrazovky
    screen.blit(prompt, prompt.get_rect(center=(Width // 2, Height // 2 - 20)))  # Zobrazeni pokynu na start
    screen.blit(prompt_q, prompt_q.get_rect(center=(Width // 2, Height // 2 + 20)))  # Zobrazeni pokynu na quit
    pygame.display.flip()  # Aktualizace obrazovky

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # Kdyz stisknuto Q
                pygame.quit()  # Ukonci Pygame
                sys.exit()  # Ukonci program
            if event.type == pygame.QUIT:  # Pokud uzivatel zavre okno
                pygame.quit()
                sys.exit()  # Ukonci program
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Kdyz stisknuto Space
                waiting = False  # Zavre uvodni obrazovku a spusti hru

# Funkce pro pohyb hada
def snake_movement(snake, direction, grow=False):
    head_x, head_y = snake[0]  # Pozice hlavy hada
    dx, dy = direction  # Smer pohybu hada
    new_head = (head_x + dx, head_y + dy)  # Nova pozice hlavy hada
    snake.insert(0, new_head)  # Pridani nove hlavy na zacatek seznamu
    if not grow:  # Pokud had neji, odstrani posledni clanek tela
        snake.pop()
    return snake

# Funkce pro vykresleni hada
def snake_render(snake):
    for i, piece in enumerate(snake):
        rect = pygame.Rect(piece[0] * Cell_Size, piece[1] * Cell_Size, Cell_Size, Cell_Size)  # Vytvoreni obdelniku pro kazdy clanek hada
        color = "YELLOW" if i == 0 else "YELLOW1" if i == 1 else "YELLOW2" if i == 2 else "YELLOW3"  # Barvy pro jednotlivé casti hada
        pygame.draw.rect(screen, color, rect)  # Vykresleni obdelniku

# Funkce pro kontrolu, zda se had neudelal do zdi
def check_wall_collision(head):
    x, y = head  # Ziskani souradnic hlavy hada
    return x < 0 or x >= Grid_Width or y < 0 or y >= Grid_Height  # Pokud hlava vyboči z mrizky

# Funkce pro kontrolu, zda se had nesrazi sám se sebou
def check_self_collision(snake):
    return snake[0] in snake[1:]  # Pokud se hlava hada nachazi v tele hada

# Funkce pro vytvoreni noveho jablka na nahodne pozici, ktera neni obsazena hadem
def apple_spawn(snake):
    while True:
        x = random.randint(0, Grid_Width - 1)  # Generovani nahodne x
        y = random.randint(0, Grid_Height - 1)  # Generovani nahodne y
        if (x, y) not in snake:  # Pokud pozice neni obsazena hadem
            return x, y

# Funkce pro vykresleni jablka
def apple_render(apple):
    circ = (apple[0] * Cell_Size, apple[1] * Cell_Size, Cell_Size, Cell_Size)  # Nastaveni obdelniku pro jablko
    pygame.draw.rect(screen, "BLUE", circ)  # Vykresleni jablka modrou barvou

# Funkce pro vykresleni mrizky
def draw_grid():
    for x in range(0, Width, Cell_Size):
        pygame.draw.line(screen, (50, 150, 50), (x, 0), (x, Height))  # Vodorovne cary
    for y in range(0, Height, Cell_Size):
        pygame.draw.line(screen, (50, 150, 50), (0, y), (Width, y))  # Svisle cary

# Funkce pro zobrazeni obrazovky pri prohre
def game_over():
    font = pygame.font.SysFont(None, 30)  # Pismo pro text
    text = font.render(f"GAME OVER, PRESS R TO RESTART OR Q TO QUIT", False, (255,0,0))  # Text pro konec hry
    rect = text.get_rect(center=(Width//2, Height//2))  # Nastaveni pozice textu
    screen.blit(text, rect)  # Zobrazeni textu na obrazovce
    pygame.display.flip()  # Aktualizace obrazovky
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Pokud uzivatel zavre okno
                pygame.quit()
                sys.exit()  # Ukonci program
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # Pokud stisknuto Q
                pygame.quit()
                sys.exit()  # Ukonci program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Pokud stisknuto R, restartuje hru
                    waiting = False

# Funkce pro blikani obrazovky pri prohre
def game_over_flash():
    for _ in range(3):
        screen.fill("RED")  # Cervene pozadi
        pygame.display.flip()  # Aktualizace obrazovky
        pygame.time.wait(100)  # Cekani 100ms
        screen.fill("GREEN")  # Zelené pozadi
        pygame.display.flip()  # Aktualizace obrazovky
        pygame.time.wait(100)  # Cekani 100ms

# Funkce pro resetovani hry
def reset_game():
    return [(5, 5), (4, 5), (3, 5)], (1, 0), apple_spawn([(5, 5), (4, 5), (3, 5)]), 0  # Resetovani hada, smeru, jablka a skore

if __name__ == '__main__':
    # Hlavni program
    show_start_menu()  # Zobrazeni uvodni obrazovky
    snake, direction, apple, score = reset_game()  # Resetovani herniho stavu
    snake = [(5, 5), (4, 5),(3, 5)]  # Pocatecni pozice hada
    direction = (1, 0)  # Pocatecni smer hada (vpravo)
    apple = apple_spawn(snake)  # Generovani jablka
    score = 0  # Pocatecni skore
    running = True  # Spusteni hry

    # Hlavni herni smycka

    while running:
        screen.fill(("GREEN"))  # Vyplneni obrazovky zelenou barvou

        draw_grid()  # Vykresleni mrizky

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Pokud uzivatel zavre okno
                    running = False
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and direction != (0, 1):  # Pohyb nahoru
                    direction = (0, -1)
                elif event.key == pygame.K_s and direction != (0, -1):  # Pohyb dolu
                    direction = (0, 1)
                elif event.key == pygame.K_a and direction != (1, 0):  # Pohyb doleva
                    direction = (-1, 0)
                elif event.key == pygame.K_d and direction != (-1, 0):  # Pohyb doprava
                    direction = (1, 0)

        grow = (snake[0][0] + direction[0], snake[0][1] + direction[1]) == apple  # Kontrola, zda had snedl jablko
        snake = snake_movement(snake, direction, grow)  # Pohyb hada

        if grow:  # Pokud had snedl jablko
            apple = apple_spawn(snake)  # Generovani noveho jablka
            score += 1  # Zvyseni skore

        if check_wall_collision(snake[0]) or check_self_collision(snake):  # Kontrola kolize sam se sebou nebo se zdi
            game_over_flash()  # Blikani obrazovky pri prohre
            game_over()  # Zobrazeni obrazovky "GAME OVER"
            snake, direction, apple, score = reset_game()  # Resetovani stavu hry

        apple_render(apple)  # Vykresleni jablka
        snake_render(snake)  # Vykresleni hada

        score_text = font.render(f"Score: {score}", True, (255,255,255))  # Zobrazeni skore
        screen.blit(score_text, (10, 10))  # Zobrazeni skore na obrazovce

        pygame.display.flip()  # Aktualizace obrazovky

        clock.tick(10)  # Omezeni poctu snimku za sekundu na 10
