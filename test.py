import pytest
from snakebase import check_self_collision
from snakebase import check_wall_collision

def test_check_self_collision_true():
    snake = [(5,5), (6,5), (5,5)]
    assert check_self_collision(snake) == True
def test_check_self_collision_false():
    snake = [(5,5), (4,5), (3,5)]
    assert check_self_collision(snake) == False
def test_check_wall_collision_true():
    head = [500,500]
    assert check_wall_collision(head) == True
def test_check_wall_collision_false():
    head = [5,5]
    assert check_wall_collision(head) == False
if __name__ == "__main__":
    test_check_self_collision_true()
    test_check_self_collision_false()
    test_check_wall_collision_true()
    test_check_wall_collision_false()
    print("Test passed")
