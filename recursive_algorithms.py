"""
Лабораторна робота № 7. Модуль 2.
Рекурсивний алгоритм швидкого сортування (QuickSort)
із програмним контролем глибини стека та захистом від переповнення.
Освітній компонент: Програмування на Python.
"""

import sys
import time


class RecursionDepthTracker:
    """Клас моніторингу та захисту глибини рекурсивного стека."""
    def __init__(self, max_allowed_depth: int = 500):
        self.current_depth = 0
        self.max_observed_depth = 0
        self.max_allowed_depth = max_allowed_depth

    def enter(self) -> None:
        """Фіксує вхід у новий рекурсивний стековий кадр."""
        self.current_depth += 1
        if self.current_depth > self.max_observed_depth:
            self.max_observed_depth = self.current_depth
        if self.current_depth > self.max_allowed_depth:
            raise RecursionError(
                f"Перевищено безпечний ліміт глибини рекурсії: {self.current_depth} > {self.max_allowed_depth}"
            )

    def leave(self) -> None:
        """Фіксує вихід зі стекового кадру при поверненні значення."""
        self.current_depth -= 1


def karatsuba_instrumented(x: int, y: int, tracker: RecursionDepthTracker) -> int:
    """
    Реалізує рекурсивний алгоритм множення Карацуби для довгих цілих чисел
    із контролем глибини рекурсивного стека.
    """
    tracker.enter()
    try:
        # Базовий випадок рекурсії: якщо числа однозначні (менші за 10), множимо звичайним способом
        if x < 10 or y < 10:
            return x * y

        # Визначаємо кількість цифр для розбиття числа
        n = max(len(str(x)), len(str(y)))
        m = n // 2

        # Розбиття чисел на старшу і молодшу частини
        high_1, low_1 = divmod(x, 10**m)
        high_2, low_2 = divmod(y, 10**m)

        # Рекурсивні обчислення трьох добутків
        z0 = karatsuba_instrumented(low_1, low_2, tracker)
        z2 = karatsuba_instrumented(high_1, high_2, tracker)
        z1 = karatsuba_instrumented(high_1 + low_1, high_2 + low_2, tracker) - z2 - z0

        # Збирання результату за формулою Карацуби: z2 * 10^(2*m) + z1 * 10^m + z0
        result = z2 * (10 ** (2 * m)) + z1 * (10**m) + z0
        return result

    finally:
        tracker.leave()


def main() -> None:
    """Головна точка входу для демонстрації та профілювання алгоритму Карацуби."""
    print("=" * 80)
    print(f"{'РЕКУРСИВНИЙ АЛГОРИТМ МНОЖЕННЯ КАРАЦУБИ':^80}")
    print("=" * 80)

    # Налаштування системного ліміту рекурсії
    system_limit = sys.getrecursionlimit()
    print(f"Системний ліміт глибини стека CPython: {system_limit} кадрів")

    # Довгі числа для демонстрації множення
    num1 = 12345678901234567890
    num2 = 98765432109876543210

    print(f"Перше довге число X:                {num1}")
    print(f"Друге довге число Y:                {num2}")
    print("-" * 80)

    # Створення об'єкта моніторингу рекурсії
    tracker = RecursionDepthTracker(max_allowed_depth=100)

    t_start = time.perf_counter()
    product = karatsuba_instrumented(num1, num2, tracker)
    t_elapsed = time.perf_counter() - t_start

    # Верифікація коректності результату за допомогою стандартного множення
    expected_product = num1 * num2
    is_correct = (product == expected_product)

    print(f"{'РЕЗУЛЬТАТИ МНОЖЕННЯ КАРАЦУБИ':^80}")
    print(f"Обчислений добуток:                  {product}")
    print(f"Верифікація коректності:             {str(is_correct).upper()}")
    print(f"Максимальна зафіксована глибина D:   {tracker.max_observed_depth} кадрів")
    print(f"Час виконання алгоритму Карацуби:    {t_elapsed * 1000:.4f} мс")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()