from src.game_objects import Player, Chip, Goose, WarGoose, HonkGoose
from src.casino_game import Casino
import random

def test_player_deposit_and_withdraw():
    """Проверяет пополнение и снятие средств игрока"""
    p = Player('Alice', 100)
    p.deposit(50)
    assert p.balance == 150
    assert p.withdraw(30)
    assert p.balance == 120
    assert not p.withdraw(200)
    assert p.balance == 120

def test_chip_addition():
    """Проверяет операцию сложения фишек"""
    c1 = Chip(5)
    c2 = Chip(10)
    c3 = c1 + c2
    assert c3.value == 15

def test_goose_merge():
    """Проверяет объединение гусей"""
    g1 = Goose('A', honk_volume=1)
    g2 = Goose('B', honk_volume=2)
    merged = g1 + g2
    assert merged.name == 'A-B'
    assert merged.honk_volume == 3

def test_wargoose_attack():
    """Проверяет атаку WarGoose на игрока"""
    casino = Casino()
    p = Player('Victim', balance=100)
    casino.register_player(p)
    g = WarGoose('Gus', honk_volume=1)
    casino.register_goose(g)
    
    random.seed(1)
    old_balance = p.balance
    g.interact(casino)
    new_balance = p.balance
    
    assert new_balance < old_balance
    assert casino.balances.get(g.name, 0) > 0
