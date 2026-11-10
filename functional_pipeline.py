"""
Лабораторна робота № 7. Модуль 1.
Варіативні сигнатури функцій (*args, **kwargs), валідація параметрів
та багатокритеріальне сортування через lambda-вирази.
Освітній компонент: Програмування на Python.
"""

import sys
import time
from typing import Any


def process_san_storage(*lun_packets: tuple, **options: Any) -> list[dict]:
    """
    Приймає варіативну кількість пакетів LUN-томів (*args) та опції конфігурації (**kwargs).
    Кожен пакет має формат: (lun_id: str, fill_percentage: float, size_tb: float, error_flag: bool).
    """
    min_fill = options.get("min_fill_percentage", 0.0)
    max_fill = options.get("max_fill_percentage", 100.0)
    exclude_errors = options.get("exclude_errors", False)

    validated_records = []

    for idx, raw_pkt in enumerate(lun_packets, start=1):
        # Валідація структури кортежу
        if not isinstance(raw_pkt, tuple) or len(raw_pkt) != 4:
            print(f"Попередження: Пакет LUN #{idx} має некоректну структуру і проігнорований.")
            continue

        lun_id, fill_pct, size_tb, err_flag = raw_pkt

        # Валідація типів даних полів
        if not (isinstance(fill_pct, (int, float)) and isinstance(size_tb, (int, float)) and isinstance(err_flag, bool)):
            print(f"Помилка валідації: Пакет LUN #{idx} містить некоректні типи даних.")
            continue

        # Фільтрація за інженерними умовами (**kwargs)
        if fill_pct < min_fill or fill_pct > max_fill:
            continue
        if exclude_errors and err_flag:
            continue

        # Формування структурованого словника
        record = {
            "lun_id": str(lun_id),
            "fill_percentage": float(fill_pct),
            "size_tb": float(size_tb),
            "error_flag": bool(err_flag),
        }
        validated_records.append(record)

    return validated_records


def main() -> None:
    """Головна функція демонстрації аналізатора SAN сховища та lambda-сортування."""
    print("=" * 80)
    print(f"{'АНАЛІЗАТОР СХОВИЩА SAN: ВАРІАТИВНА ОБРОБКА ТА LAMBDA-СОРТУВАННЯ':^80}")
    print("=" * 80)

    # Сирий масив даних LUN-томів SAN
    raw_lun_stream = (
        ("LUN-101", 78.5, 12.0, False),
        ("LUN-103", 92.1, 24.0, True),   # Помилка, може бути відфільтрована за потреби
        ("LUN-102", 45.0, 8.0, False),
        ("LUN-105", 15.2, 16.0, False),  # Буде відфільтровано за мінімальним заповненням (< 20.0%)
        ("LUN-103", 88.4, 24.0, False),  # Інший стан того ж LUN-103
        ("LUN-104", 92.1, 32.0, False),  # Однаковий відсоток заповнення з LUN-103 для перевірки 2-го критерію
    )

    # 1. Виклик функції з розпакуванням кортежу (*args) та опціями (**kwargs)
    filtered_luns = process_san_storage(
        *raw_lun_stream,
        min_fill_percentage=20.0,
        max_fill_percentage=100.0,
        exclude_errors=False
    )

    print(f"Вхідний потік: {len(raw_lun_stream)} пакетів. Пройшли валідацію: {len(filtered_luns)} пакетів.\n")

    # 2. Багатокритеріальне сортування за допомогою sorted та lambda
    # Критерій 1: Заповненість % за спаданням (-item['fill_percentage'])
    # Критерій 2: ID тому за зростанням (item['lun_id'])
    sorted_luns = sorted(
        filtered_luns,
        key=lambda item: (-item["fill_percentage"], item["lun_id"])
    )

    # 3. Виведення результатів у вигляді таблиці
    print(f"| {'№':^4} | {'ID LUN-тому':^15} | {'Заповненість (%)':^18} | {'Розмір (ТБ)':^14} | {'Помилка':^10} |")
    print("-" * 80)
    for idx, rec in enumerate(sorted_luns, start=1):
        print(
            f"| {idx:^4d} | {rec['lun_id']:<15} | {rec['fill_percentage']:^18.1f} | "
            f"{rec['size_tb']:^14.1f} | {str(rec['error_flag']):^10} |"
        )
    print("=" * 80 + "\n")


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_elapsed = time.perf_counter() - t_start
    print(f"Час виконання функціонального конвеєра SAN: {t_elapsed * 1000:.3f} мс\n")