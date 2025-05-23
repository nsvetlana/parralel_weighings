import math
from weighings import min_weighings


def min_weighings(m, n, k, known_type=False):
    """
    Вычисляет минимальное число раундов взвешиваний для обнаружения m фальшивых монет среди n монет
    при наличии k весов (используемых параллельно).

    Параметры:
        m (int): число фальшивых монет.
        n (int): общее число монет.
        k (int): число весов.
        known_type (bool): если True, то считается, что отклонение фальшивых монет известно
                           (например, все фальшивые монеты легче или тяжелее);
                           если False — отклонение неизвестно (для каждой фальшивой монеты два варианта).

    Возвращает:
        int: минимальное число раундов взвешиваний, необходимое для различения всех вариантов.
    """
    # Вычисляем ln(binom(n, m)) через функцию math.lgamma:
    # ln(binom(n, m)) = ln(n!) - ln(m!) - ln((n-m)!)
    log_binom = math.lgamma(n + 1) - math.lgamma(m + 1) - math.lgamma(n - m + 1)

    if known_type:
        total_log = log_binom  # Только выбор монет
    else:
        # Учитываем, что для каждой фальшивой монеты два варианта (легче или тяжелее)
        total_log = m * math.log(2) + log_binom

    # Неравенство: total_log <= k * w * ln(3)
    # Решаем относительно w: w >= total_log / (k * ln(3)), округляем вверх.
    return math.ceil(total_log / (k * math.log(3)))


def run_tests():
    # Тест 1: 1 фальшивая монета из 12 при 1 весе
    # Оба случая: известное и неизвестное отклонение => должно быть 3 раунда.
    result_unknown = min_weighings(1, 12, 1, known_type=False)
    result_known = min_weighings(1, 12, 1, known_type=True)
    assert result_unknown == 3, f'Ожидалось 3, получено {result_unknown} (unknown)'
    assert result_known == 3, f'Ожидалось 3, получено {result_known} (known)'

    # Тест 2: 1 фальшивая монета из 3 при 1 весе
    # Неизвестное отклонение: 2^1 * C(3,1) = 6 вариантов, ln(6)/ln(3) ≈ 1.63, ceil = 2.
    # Известное отклонение: C(3,1) = 3 вариантов, ln(3)/ln(3) = 1, ceil = 1.
    result_unknown = min_weighings(1, 3, 1, known_type=False)
    result_known = min_weighings(1, 3, 1, known_type=True)
    assert result_unknown == 2, f'Ожидалось 2, получено {result_unknown} (unknown)'
    assert result_known == 1, f'Ожидалось 1, получено {result_known} (known)'

    # Тест 3: 2 фальшивые монеты из 20 при 1 весе
    # Неизвестное отклонение: 2^2 * C(20,2) = 4 * 190 = 760 вариантов, ln(760)/ln(3) → ceil = 7.
    # Известное отклонение: C(20,2) = 190 вариантов, ln(190)/ln(3) → ceil = 5.
    result_unknown = min_weighings(2, 20, 1, known_type=False)
    result_known = min_weighings(2, 20, 1, known_type=True)
    assert result_unknown == 7, f'Ожидалось 7, получено {result_unknown} (unknown)'
    assert result_known == 5, f'Ожидалось 5, получено {result_known} (known)'

    # Тест 4: Большой пример: 500 фальшивых из 50_000_000 при 10 весах
    # По предыдущим расчётам: неизвестное отклонение → 556, известное → 524.
    result_unknown = min_weighings(500, 50_000_000, 10, known_type=False)
    result_known = min_weighings(500, 50_000_000, 10, known_type=True)
    assert result_unknown == 556, f'Ожидалось 556, получено {result_unknown} (unknown)'
    assert result_known == 524, f'Ожидалось 524, получено {result_known} (known)'

    # Тест 5: 1 фальшивая монета из 3 при 2 весах (параллельно)
    # Количество исходов за раунд = 3^2 = 9.
    # Неизвестное отклонение: 2 * C(3,1)=6 вариантов → ln(6)/(2*ln(3)) ≈ 0.815, ceil =1.
    # Известное отклонение: C(3,1)=3 вариантов → ln(3)/(2*ln(3)) = 0.5, ceil = 1.
    result_unknown = min_weighings(1, 3, 2, known_type=False)
    result_known = min_weighings(1, 3, 2, known_type=True)
    assert result_unknown == 1, f'Ожидалось 1, получено {result_unknown} (unknown)'
    assert result_known == 1, f'Ожидалось 1, получено {result_known} (known)'

    print("All tests passed!")

if __name__ == '__main__':
    run_tests()
