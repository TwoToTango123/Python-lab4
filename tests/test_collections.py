from src.game_objects import Player, Goose
from src.collections import PlayerCollection, GooseCollection, CasinoBalance

def test_player_collection():
    """Проверяет работу коллекции игроков"""
    pc = PlayerCollection()
    p1 = Player('Alice', 30)
    p2 = Player('Bob', 40)
    pc.add(p1)
    pc.add(p2)
    
    assert len(pc) == 2
    assert p1 in pc
    assert 'Bob' in pc
    assert pc[0] is p1
    assert pc.find_by_name('Alice') is p1
    
    sliced = pc[0:2]
    assert isinstance(sliced, PlayerCollection)
    assert len(sliced) == 2

def test_goose_collection():
    """Проверяет работу коллекции гусей"""
    gc = GooseCollection()
    g1 = Goose('A', honk_volume=1)
    g2 = Goose('B', honk_volume=2)
    gc.add(g1)
    gc.add(g2)
    
    assert len(gc) == 2
    assert g1 in gc
    assert 'B' in gc
    assert gc[1] is g2
    
    sliced = gc[0:2]
    assert isinstance(sliced, GooseCollection)
    assert len(sliced) == 2

def test_casino_balance():
    """Проверяет работу CasinoBalance"""
    cb = CasinoBalance()
    cb['Alice'] = 100
    cb['Alice'] = 150
    assert cb['Alice'] == 150
    
    cb.change_balance('Gus', 50)
    assert cb['Gus'] == 50
    
    cb.change_balance('Gus', 30)
    assert cb['Gus'] == 80
