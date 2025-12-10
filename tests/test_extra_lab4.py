from src.casino import (
    Player,
    Goose,
    HonkGoose,
    PlayerCollection,
    GooseCollection,
    Casino,
)
import random

def test_collections_and_goose_add():
    """Проверяет поведение коллекций игроков и гусей, а также объединение гуся"""
    pc = PlayerCollection()
    p = Player('X', 10)
    pc.add(p)
    assert p in pc
    assert 'X' in pc
    assert pc.find_by_name('X') is p
    sliced = pc[0:1]
    assert isinstance(sliced, PlayerCollection) and sliced[0] is p

    gc = GooseCollection()
    g1 = Goose('A', honk_volume=1)
    g2 = Goose('B', honk_volume=2)
    gc.add(g1)
    gc.add(g2)
    assert g1 in gc
    assert 'B' in gc
    sliced_g = gc[0:2]
    assert isinstance(sliced_g, GooseCollection) and sliced_g[1] is g2

    merged = g1 + g2
    assert merged.name == 'A-B'
    assert merged.honk_volume == 3

def test_honk_goose_changes_player_balances():
    """Проверяет, что HonkGoose.honk изменяет балансы игроков и доход гуся"""
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

def test_withdraw_fail_leaves_balance():
    """Проверяет, что при попытке снять больше баланса операция отклоняется без изменений"""
    p = Player('Z', balance=10)
    assert not p.withdraw(20)
    assert p.balance == 10
