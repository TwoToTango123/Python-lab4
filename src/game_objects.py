from dataclasses import dataclass
import random

@dataclass
class Player:
    """Класс игрока
    Атрибуты:
        name: имя игрока
        balance: текущий баланс(целое число)
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
        interact: взаимодействие с казино(переопределяется)
        __add__: объединение двух гусей
    """
    def __init__(self, name: str, honk_volume: int = 1) -> None:
        self.name = name
        self.honk_volume = honk_volume

    def interact(self, casino) -> None:
        """Взаимодействие гуся с казино"""
        pass

    def __add__(self, other: 'Goose') -> 'Goose':
        new_name = f"{self.name}-{other.name}"
        new_volume = self.honk_volume + other.honk_volume
        return Goose(new_name, new_volume)

class WarGoose(Goose):
    """Гусь-боец, который атакует игроков и ворует у них деньги"""
    def interact(self, casino) -> None:
        """Атакует случайного игрока и переводит часть его баланса себе"""
        if len(casino.players) == 0:
            return
        victim_player = random.choice(list(casino.players))
        max_steal_amount = random.randint(1, max(1, victim_player.balance // 4))
        amount_stolen = min(max_steal_amount, victim_player.balance)
        victim_player.withdraw(amount_stolen)
        casino.balances.change_balance(self.name, amount_stolen)

class HonkGoose(Goose):
    """Гусь-крикун, который своим криком влияет на балансы всех игроков"""
    def honk(self, casino) -> None:
        """Выполняет эффект крика: случайно уменьшает/увеличивает балансы игроков"""
        for current_player in casino.players:
            balance_change = random.randint(-5, 5) * self.honk_volume
            if balance_change < 0:
                loss_amount = min(current_player.balance, -balance_change)
                current_player.withdraw(loss_amount)
                casino.balances.change_balance(self.name, loss_amount)
            else:
                current_player.deposit(balance_change)
                casino.balances.change_balance(self.name, -balance_change)
