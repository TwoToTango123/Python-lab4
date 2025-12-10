from typing import Iterator, List, Optional
from .game_objects import Player, Goose

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
    метод change_balance для быстрого изменения баланса
    """
    def __setitem__(self, key: str, value: int) -> None:
        """Установить значение баланса и залогировать изменение"""
        super().__setitem__(key, value)

    def change_balance(self, goose_name: str, amount: int) -> None:
        """Отрегулировать доход для указанного гуся"""
        self.setdefault(goose_name, 0)
        previous_income = self[goose_name]
        self[goose_name] = previous_income + amount
