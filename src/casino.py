from dataclasses import dataclass
from typing import Iterator, List, Optional
import random

@dataclass
class Player:
    """Класс игрока

    Атрибуты:
        name: имя игрока
        balance: текущий баланс (целое число)
    """
    name: str
    balance: int = 0

    def deposit(self, amount: int) -> None:
        """Пополнить баланс игрока на amount"""
        self.balance += amount

    def withdraw(self, amount: int) -> bool:
        """Попытаться снять amount с баланса игрока"""
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

@dataclass
class Chip:
    """Фишка казино с номиналом value

    Поддерживает сложение через __add__
    """
    value: int

    def __add__(self, other: 'Chip') -> 'Chip':
        return Chip(self.value + other.value)

class Goose:
    """Базовый класс гуся с параметрами имени и громкости крика

    Методы:
        interact: взаимодействие с казино (переопределяется в подклассах)
        __add__: объединение двух гусей
    """
    def __init__(self, name: str, honk_volume: int = 1) -> None:
        self.name = name
        self.honk_volume = honk_volume

    def interact(self, casino: 'Casino') -> None:
        """Взаимодействие гуся с казино"""
        pass

    def __add__(self, other: 'Goose') -> 'Goose':
        new_name = f"{self.name}-{other.name}"
        new_volume = self.honk_volume + other.honk_volume
        return Goose(new_name, new_volume)

class WarGoose(Goose):
    """Гусь-боец, который атакует игроков и ворует у них деньги"""
    def interact(self, casino: 'Casino') -> None:
        """Атакует случайного игрока и переводит часть его баланса себе"""
        if len(casino.players) == 0:
            return
        victim_player = random.choice(list(casino.players))
        max_steal_amount = random.randint(1, max(1, victim_player.balance // 4))
        amount_stolen = min(max_steal_amount, victim_player.balance)
        victim_player.withdraw(amount_stolen)
        casino.balances.adjust_income(self.name, amount_stolen)

class HonkGoose(Goose):
    """Гусь-крикун, который своим криком влияет на балансы всех игроков"""
    def honk(self, casino: 'Casino') -> None:
        """Выполняет эффект крика: случайно уменьшает/увеличивает балансы игроков"""
        for current_player in casino.players:
            balance_change = random.randint(-5, 5) * self.honk_volume
            if balance_change < 0:
                loss_amount = min(current_player.balance, -balance_change)
                current_player.withdraw(loss_amount)
                casino.balances.adjust_income(self.name, loss_amount)
            else:
                current_player.deposit(balance_change)
                casino.balances.adjust_income(self.name, -balance_change)

class BaseCollection:
    """Абстрактный базовый класс для коллекций
    Определяет интерфейс для всех коллекций: итератор, длина, индексация
    """
    def __iter__(self) -> Iterator:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

class PlayerCollection(BaseCollection):
    """Коллекция игроков, поддерживающая итерацию, индексацию и срезы"""
    def __init__(self, players: Optional[List[Player]] = None) -> None:
        self._players: List[Player] = list(players) if players is not None else []

    def __iter__(self) -> Iterator[Player]:
        return iter(self._players)

    def __len__(self) -> int:
        return len(self._players)

    def __getitem__(self, idx):
        res = self._players[idx]
        if isinstance(idx, slice):
            return PlayerCollection(res)
        return res

    def add(self, player: Player) -> None:
        """Добавить игрока в коллекцию"""
        self._players.append(player)

    def remove(self, player: Player) -> None:
        """Удалить игрока из коллекции"""
        self._players.remove(player)
    
    def __contains__(self, item) -> bool:
        if isinstance(item, Player):
            return any(p.name == item.name for p in self._players)
        if isinstance(item, str):
            return any(p.name == item for p in self._players)
        return False

    def find_by_name(self, name: str) -> Optional[Player]:
        """Найти игрока по имени"""
        for p in self._players:
            if p.name == name:
                return p
        return None

class GooseCollection(BaseCollection):
    """Коллекция гусей, поддерживающая итерацию, индексацию и срезы"""
    def __init__(self, geese: Optional[List[Goose]] = None) -> None:
        self._geese: List[Goose] = list(geese) if geese is not None else []

    def __iter__(self) -> Iterator[Goose]:
        return iter(self._geese)

    def __len__(self) -> int:
        return len(self._geese)

    def __getitem__(self, idx):
        res = self._geese[idx]
        if isinstance(idx, slice):
            return GooseCollection(res)
        return res

    def add(self, goose: Goose) -> None:
        """Добавить гуся в коллекцию"""
        self._geese.append(goose)

    def remove(self, goose: Goose) -> None:
        """Удалить гуся из коллекции"""
        self._geese.remove(goose)

    def __contains__(self, item) -> bool:
        if isinstance(item, Goose):
            return any(g.name == item.name for g in self._geese)
        if isinstance(item, str):
            return any(g.name == item for g in self._geese)
        return False

class CasinoBalance(dict):
    """Словарь для отслеживания доходов игроков и гусей в казино
    
    Переопределяет __setitem__ для логирования изменений и предоставляет
    метод adjust_income для быстрого изменения баланса
    """
    def __setitem__(self, key: str, value: int) -> None:
        """Установить значение баланса и залогировать изменение"""
        super().__setitem__(key, value)

    def adjust_income(self, goose_name: str, amount: int) -> None:
        """Отрегулировать доход для указанного гуся"""
        self.setdefault(goose_name, 0)
        previous_income = self[goose_name]
        self[goose_name] = previous_income + amount

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

    def register_goose(self, goose: Goose) -> None:
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

    def _get_random_goose_from_collection(self) -> Optional[Goose]:
        return random.choice(list(self.geese)) if len(self.geese) else None

    def _player_bet(self) -> None:
        current_player = self._choose_random_player()
        if not current_player:
            return
        bet_amount = random.randint(1, 10)
        if current_player.withdraw(bet_amount):
            self.balances.adjust_income('house', bet_amount)

    def _player_win(self) -> None:
        current_player = self._choose_random_player()
        if not current_player:
            return
        win_amount = random.randint(1, 20)
        current_player.deposit(win_amount)
        self.balances.adjust_income('house', -win_amount)

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
        self.balances.adjust_income(random_goose.name, amount_to_steal)

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
        self.balances.adjust_income('house', loss_amount)

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

    for _ in range(steps):
        casino.step()
