"""Snake Game - jednoducha implementace klasicke hry Snake v Pygame.

Modul obsahuje hernu logiku (pohyb hada, detekce kolizi, generovani jablek)
i vykreslovaci funkce. Pri spusteni jako skript (`python snakebase.py`)
zobrazi uvodni menu a spusti hlavni hernu smycku.

Ovladani:
    W / A / S / D : pohyb nahoru / doleva / dolu / doprava
    Q             : ukoncit hru
    R             : restart po Game Over

Konstanty:
    Cell_Size   : velikost jedne bunky v pixelech
    Grid_Width  : sirka mrizky v bunkach
    Grid_Height : vyska mrizky v bunkach
"""

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
# Nastaveni okna
screen = pygame.display.set_mode((Width, Height))
# Nazev okna
pygame.display.set_caption("Snake Game")
# Pocatecni skore
score = 0
# Pismo pro text
font = pygame.font.SysFont(None, 30)
# Hodiny pro spravu snimku za sekundu
clock = pygame.time.Clock()


def show_start_menu():
    """Zobrazi uvodni menu s nazvem hry a instrukcemi.

    Ceka na stisk klavesy Space (spusti hru) nebo Q (ukonci program).
    Funkce blokuje, dokud uzivatel jednu z klaves nestiskne.
    """
    # Nastaveni pozadi na cerne
    screen.fill("Black")
    # Vytvoreni textu "Snake Game" a pokynu
    title = font.render("Snake Game", True, (0, 255, 0))
    prompt = font.render("Press Spacebar to start", True, (255, 255, 255))
    prompt_q = font.render("Press Q to quit", True, (255, 255, 255))
    # Zobrazeni textu ve stredu obrazovky
    screen.blit(title, title.get_rect(center=(Width // 2, Height // 4 - 20)))
    screen.blit(prompt, prompt.get_rect(center=(Width // 2, Height // 2 - 20)))
    screen.blit(prompt_q, prompt_q.get_rect(center=(Width // 2, Height // 2 + 20)))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


def snake_movement(snake, direction, grow=False):
    """Posune hada o jeden krok ve smeru `direction`.

    Args:
        snake: Seznam tuplu (x, y) reprezentujici telo hada.
               Prvni prvek je hlava.
        direction: Tuple (dx, dy) urcujici smer pohybu, napr. (1, 0) doprava.
        grow: Pokud True, had po pohybu o jeden clanek prodlouzi (snedl jablko).

    Returns:
        Aktualizovany seznam clanku hada s novou hlavou na zacatku.
    """
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    snake.insert(0, new_head)
    if not grow:
        snake.pop()
    return snake


def snake_render(snake):
    """Vykresli vsechny clanky hada na obrazovku.

    Args:
        snake: Seznam tuplu (x, y) reprezentujici telo hada v jednotkach mrizky.
    """
    for i, piece in enumerate(snake):
        rect = pygame.Rect(
            piece[0] * Cell_Size, piece[1] * Cell_Size, Cell_Size, Cell_Size
        )
        # Barvy pro jednotlive casti hada (hlava nejsvetlejsi)
        if i == 0:
            color = "YELLOW"
        elif i == 1:
            color = "YELLOW1"
        elif i == 2:
            color = "YELLOW2"
        else:
            color = "YELLOW3"
        pygame.draw.rect(screen, color, rect)


def check_wall_collision(head):
    """Zjisti, zda hlava hada narazila do zdi.

    Args:
        head: Souradnice hlavy jako (x, y) nebo [x, y].

    Returns:
        True pokud je hlava mimo mrizku (kolize), jinak False.
    """
    x, y = head
    return x < 0 or x >= Grid_Width or y < 0 or y >= Grid_Height


def check_self_collision(snake):
    """Zjisti, zda se had srazil sam se sebou.

    Args:
        snake: Seznam tuplu reprezentujici telo hada (hlava na indexu 0).

    Returns:
        True pokud se hlava nachazi take ve zbytku tela, jinak False.
    """
    return snake[0] in snake[1:]


def apple_spawn(snake):
    """Vygeneruje nahodnou pozici pro nove jablko mimo telo hada.

    Args:
        snake: Seznam soucasnych pozic clanku hada, kterym se musi vyhnout.

    Returns:
        Tuple (x, y) - nova pozice jablka v souradnicich mrizky.
    """
    while True:
        x = random.randint(0, Grid_Width - 1)
        y = random.randint(0, Grid_Height - 1)
        if (x, y) not in snake:
            return x, y


def apple_render(apple):
    """Vykresli jablko jako modry ctverec na zadane pozici.

    Args:
        apple: Tuple (x, y) udavajici pozici jablka v souradnicich mrizky.
    """
    circ = (apple[0] * Cell_Size, apple[1] * Cell_Size, Cell_Size, Cell_Size)
    pygame.draw.rect(screen, "BLUE", circ)


def draw_grid():
    """Vykresli mrizku (vodorovne a svisle cary) pres celou obrazovku."""
    for x in range(0, Width, Cell_Size):
        pygame.draw.line(screen, (50, 150, 50), (x, 0), (x, Height))
    for y in range(0, Height, Cell_Size):
        pygame.draw.line(screen, (50, 150, 50), (0, y), (Width, y))


def game_over():
    """Zobrazi obrazovku Game Over a ceka na stisk R (restart) nebo Q (konec).

    Funkce blokuje, dokud uzivatel jednu z klaves nestiskne.
    """
    font = pygame.font.SysFont(None, 30)
    text = font.render(
        "GAME OVER, PRESS R TO RESTART OR Q TO QUIT", False, (255, 0, 0)
    )
    rect = text.get_rect(center=(Width // 2, Height // 2))
    screen.blit(text, rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False


def game_over_flash():
    """Provede vizualni efekt blikajici obrazovky (3x cervena/zelena) pri prohre."""
    for _ in range(3):
        screen.fill("RED")
        pygame.display.flip()
        pygame.time.wait(100)
        screen.fill("GREEN")
        pygame.display.flip()
        pygame.time.wait(100)


def reset_game():
    """Resetuje hru do pocatecniho stavu.

    Returns:
        Tuple (snake, direction, apple, score) - pocatecni hodnoty:
        had ze 3 clanku, smer doprava, nahodne jablko, skore 0.
    """
    initial_snake = [(5, 5), (4, 5), (3, 5)]
    return initial_snake, (1, 0), apple_spawn(initial_snake), 0


if __name__ == '__main__':
    # Hlavni program
    show_start_menu()
    snake, direction, apple, score = reset_game()
    running = True

    # Hlavni herni smycka
    while running:
        screen.fill("GREEN")
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_s and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_a and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_d and direction != (-1, 0):
                    direction = (1, 0)

        # Kontrola, zda had snedl jablko
        grow = (snake[0][0] + direction[0], snake[0][1] + direction[1]) == apple
        snake = snake_movement(snake, direction, grow)

        if grow:
            apple = apple_spawn(snake)
            score += 1

        # Kontrola kolize sam se sebou nebo se zdi
        if check_wall_collision(snake[0]) or check_self_collision(snake):
            game_over_flash()
            game_over()
            snake, direction, apple, score = reset_game()

        apple_render(apple)
        snake_render(snake)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(10)
