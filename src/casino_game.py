import random
from typing import Optional
from .game_objects import Player, WarGoose, HonkGoose
from .collections import PlayerCollection, GooseCollection, CasinoBalance


class Casino:
    """Главный класс казино, управляющий игроками, гусями и симуляцией событий"""
    def __init__(self) -> None:
        self.players = PlayerCollection()
        self.geese = GooseCollection()
        self.balances: CasinoBalance = CasinoBalance()

    def register_player(self, player: Player) -> None:
        """Зарегистрировать игрока в казино"""
        self.players.add(player)
        self.balances[player.name] = player.balance

    def register_goose(self, goose) -> None:
        """Зарегистрировать гуся в казино"""
        self.geese.add(goose)
        self.balances.setdefault(goose.name, 0)

    def step(self) -> None:
        """Выполнить один шаг симуляции: выбрать и выполнить случайное событие"""
        events = [
            self._player_bet,
            self._player_win,
            self._wargoose_attack,
            self._honk_goose_honk,
            self._goose_steal,
            self._merge_geese,
            self._panic_loss,
        ]
        selected_event = random.choice(events)
        selected_event()

    def _choose_random_player(self) -> Optional[Player]:
        return random.choice(list(self.players)) if len(self.players) else None

    def _get_random_goose_from_collection(self):
        return random.choice(list(self.geese)) if len(self.geese) else None

    def _player_bet(self) -> None:
        current_player = self._choose_random_player()
        if not current_player:
            return
        bet_amount = random.randint(1, 10)
        if current_player.withdraw(bet_amount):
            self.balances[current_player.name] = current_player.balance
            self.balances.change_balance('house', bet_amount)

    def _player_win(self) -> None:
        current_player = self._choose_random_player()
        if not current_player:
            return
        win_amount = random.randint(1, 20)
        current_player.deposit(win_amount)
        self.balances[current_player.name] = current_player.balance
        self.balances.change_balance('house', -win_amount)

    def _wargoose_attack(self) -> None:
        random_goose = self._get_random_goose_from_collection()
        if isinstance(random_goose, WarGoose):
            random_goose.interact(self)

    def _honk_goose_honk(self) -> None:
        random_goose = self._get_random_goose_from_collection()
        if isinstance(random_goose, HonkGoose):
            random_goose.honk(self)

    def _goose_steal(self) -> None:
        random_goose = self._get_random_goose_from_collection()
        target_player = self._choose_random_player()
        if not random_goose or not target_player:
            return
        amount_to_steal = random.randint(1, min(10, target_player.balance)) if target_player.balance > 0 else 0
        target_player.withdraw(amount_to_steal)
        self.balances[target_player.name] = target_player.balance
        self.balances.change_balance(random_goose.name, amount_to_steal)

    def _merge_geese(self) -> None:
        if len(self.geese) < 2:
            return
        first_goose = random.choice(list(self.geese))
        second_goose = random.choice(list(self.geese))
        if first_goose is second_goose:
            return
        merged_goose = first_goose + second_goose
        self.geese.add(merged_goose)

    def _panic_loss(self) -> None:
        panicked_player = self._choose_random_player()
        if not panicked_player:
            return
        loss_amount = panicked_player.balance
        panicked_player.withdraw(loss_amount)
        self.balances[panicked_player.name] = panicked_player.balance
        self.balances.change_balance('house', loss_amount)


def run_simulation(steps: int = 20, seed: Optional[int] = None) -> None:
    """Запустить симуляцию казино с указанным количеством шагов
    Параметры:
        steps: количество шагов симуляции
        seed: начальное значение для генератора случайных чисел (необязательно)
    """
    if seed is not None:
        random.seed(seed)
    casino = Casino()

    p1 = Player('Alice', balance=100)
    p2 = Player('Bob', balance=50)
    casino.register_player(p1)
    casino.register_player(p2)

    g1 = WarGoose('Gus', honk_volume=2)
    g2 = HonkGoose('Hilda', honk_volume=1)
    casino.register_goose(g1)
    casino.register_goose(g2)

    for i in range(steps):
        casino.step()
