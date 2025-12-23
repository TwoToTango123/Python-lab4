import argparse
from .casino_game import run_simulation


def main():
    """Основная функция для запуска симуляции из командной строки"""
    parser = argparse.ArgumentParser(
        description='Симуляция казино "Казино и Гуси"',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python -m src.main                    # Запуск с параметрами по умолчанию
  python -m src.main --steps 50         # Запуск на 50 шагов
  python -m src.main --seed 123         # Детерминированная симуляция
  python -m src.main -s 30 --seed 42    # Комбинация параметров
        """
    )
    
    parser.add_argument(
        '-s', '--steps',
        type=int,
        default=20,
        help='Количество шагов симуляции (по умолчанию: 20)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Начальное значение для генератора случайных чисел (для воспроизводимости)'
    )
    
    args = parser.parse_args()
    
    print(f"Запуск симуляции 'Казино и Гуси'")
    print(f"Количество шагов: {args.steps}")
    if args.seed is not None:
        print(f"Seed: {args.seed} (детерминированный режим)")
    print()
    
    run_simulation(steps=args.steps, seed=args.seed)
    
    print()
    print("Симуляция завершена")


if __name__ == "__main__":
    main()
