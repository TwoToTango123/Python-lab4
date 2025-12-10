from src.game_objects import Player, WarGoose, HonkGoose
from src.casino_game import Casino, run_simulation
import random

def test_casino_simulation_runs():
    """Запускает небольшую детерминированную симуляцию казино"""
    run_simulation(steps=5, seed=42)

def test_casino_register_and_events():
    """Проверяет регистрацию игроков/гусей и выполнение событий"""
    casino = Casino()
    p1 = Player('Alice', balance=100)
    p2 = Player('Bob', balance=50)
    casino.register_player(p1)
    casino.register_player(p2)
    
    g1 = WarGoose('Gus', honk_volume=2)
    g2 = HonkGoose('Hilda', honk_volume=1)
    casino.register_goose(g1)
    casino.register_goose(g2)
    
    assert len(casino.players) == 2
    assert len(casino.geese) == 2
    assert 'Alice' in casino.balances
    assert 'Gus' in casino.balances
    
    for i in range(10):
        casino.step()

def test_honk_goose_effect():
    """Проверяет эффект крика HonkGoose на балансы игроков"""
    casino = Casino()
    p1 = Player('A', balance=20)
    p2 = Player('B', balance=20)
    casino.register_player(p1)
    casino.register_player(p2)
    
    h = HonkGoose('Hilda', honk_volume=1)
    casino.register_goose(h)
    
    random.seed(0)
    total_before = p1.balance + p2.balance
    h.honk(casino)
    total_after = p1.balance + p2.balance
    
    assert total_after != total_before
    assert casino.balances.get('Hilda', 0) != 0
