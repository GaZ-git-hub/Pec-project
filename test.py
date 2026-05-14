"""Testy pro modul snakebase.

Pokryva funkce pro detekci kolizi (se zdi i sebou samym) a generovani jablek.
Pousti se prikazem `pytest test.py`.
"""

import pytest
from snakebase import (
    check_self_collision,
    check_wall_collision,
    snake_movement,
    apple_spawn,
    Grid_Width,
    Grid_Height,
)


# --- check_self_collision -----------------------------------------------------

def test_self_collision_when_head_touches_body():
    """Had se srazil sam se sebou - hlava na pozici tela."""
    snake = [(5, 5), (6, 5), (5, 5)]
    assert check_self_collision(snake) is True


def test_no_self_collision_on_straight_snake():
    """Rovny had bez prekryvu nesmi vyhlasit kolizi."""
    snake = [(5, 5), (4, 5), (3, 5)]
    assert check_self_collision(snake) is False


def test_no_self_collision_minimal_snake():
    """Had o jednom clanku nikdy nemuze byt v kolizi sam se sebou."""
    snake = [(0, 0)]
    assert check_self_collision(snake) is False


def test_self_collision_when_head_equals_tail():
    """Hlava na pozici posledniho clanku = sebekolize."""
    snake = [(2, 2), (3, 2), (4, 2), (2, 2)]
    assert check_self_collision(snake) is True


# --- check_wall_collision -----------------------------------------------------

@pytest.mark.parametrize("head", [
    (-1, 5),                   # vlevo za mrizkou
    (Grid_Width, 5),           # vpravo za mrizkou
    (5, -1),                   # nad mrizkou
    (5, Grid_Height),          # pod mrizkou
    (500, 500),                # hluboko mimo
])
def test_wall_collision_outside_grid(head):
    """Vsechny pozice mimo mrizku musi vyhlasit kolizi."""
    assert check_wall_collision(head) is True


@pytest.mark.parametrize("head", [
    (0, 0),                    # levy horni roh
    (Grid_Width - 1, 0),       # pravy horni roh
    (0, Grid_Height - 1),      # levy dolni roh
    (Grid_Width - 1, Grid_Height - 1),  # pravy dolni roh
    (5, 5),                    # uprostred
])
def test_no_wall_collision_inside_grid(head):
    """Vsechny pozice uvnitr mrizky (vcetne hranicnich) nesmi byt kolize."""
    assert check_wall_collision(head) is False


# --- snake_movement -----------------------------------------------------------

def test_movement_right_without_growing():
    """Pohyb doprava posune hlavu o (1, 0), telo zustane stejne dlouhe."""
    snake = [(5, 5), (4, 5), (3, 5)]
    result = snake_movement(snake, (1, 0), grow=False)
    assert result[0] == (6, 5)
    assert len(result) == 3


def test_movement_grow_extends_snake():
    """Pri grow=True se had prodlouzi o jeden clanek."""
    snake = [(5, 5), (4, 5), (3, 5)]
    result = snake_movement(snake, (1, 0), grow=True)
    assert result[0] == (6, 5)
    assert len(result) == 4


def test_movement_up_changes_only_y():
    """Pohyb nahoru zmeni jen y-souradnici hlavy."""
    snake = [(5, 5), (5, 6), (5, 7)]
    result = snake_movement(snake, (0, -1), grow=False)
    assert result[0] == (5, 4)


# --- apple_spawn --------------------------------------------------------------

def test_apple_spawn_not_on_snake():
    """Vygenerovane jablko nesmi byt na pozici nektereho clanku hada."""
    snake = [(5, 5), (4, 5), (3, 5)]
    for _ in range(50):  # opakujeme, protoze pozice je nahodna
        apple = apple_spawn(snake)
        assert apple not in snake


def test_apple_spawn_inside_grid():
    """Jablko musi byt vzdy uvnitr mrizky."""
    snake = [(5, 5)]
    for _ in range(50):
        x, y = apple_spawn(snake)
        assert 0 <= x < Grid_Width
        assert 0 <= y < Grid_Height


if __name__ == "__main__":
    # Umoznuje spustit i prikazem `python test.py`, nejen pytestem.
    pytest.main([__file__, "-v"])
