from src.casino import (
    Player,
    Chip,
    WarGoose,
    PlayerCollection,
    CasinoBalance,
    Casino,
    run_simulation,
)


def test_collections_and_chip_add():
    """Проверяет работу коллекций игроков и корректность сложения фишек"""
    pc = PlayerCollection()
    p1 = Player('Alice', 30)
    p2 = Player('Bob', 40)
    pc.add(p1)
    pc.add(p2)
    assert len(pc) == 2
    assert pc[0] is p1
    assert pc[0:2][1] is p2

    c1 = Chip(5)
    c2 = Chip(10)
    assert (c1 + c2).value == 15


def test_casino_balance_and_goose():
    """Проверяет работу CasinoBalance и создание гуся"""
    cb = CasinoBalance()
    cb['Alice'] = 50
    cb['Alice'] = 70
    g = WarGoose('Gus', honk_volume=1)
    assert 'Alice' in cb


def test_casino_simulation_runs():
    """Запускает небольшую детерминированную симуляцию для проверки ошибок"""
    run_simulation(steps=5, seed=42)


def test_wargoose_attack_effects():
    """Проверяет эффект атаки WarGoose: баланс игрока уменьшается и доход гуся растёт"""
    casino = Casino()
    p = Player('Charlie', balance=100)
    casino.register_player(p)
    g = WarGoose('Gus', honk_volume=1)
    casino.register_goose(g)
    old_balance = p.balance
    import random
    random.seed(1)
    casino._wargoose_attack()
    new_balance = p.balance
    stolen = old_balance - new_balance
    assert stolen >= 0
    assert casino.balances.get(g.name, 0) == stolen
