import math
import unittest


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
        # Если тип отклонения известен, учитываем только выбор монет
        total_log = log_binom
    else:
        # Если тип отклонения неизвестен, учитываем, что для каждой фальшивой монеты есть два варианта (легче или тяжелее)
        total_log = m * math.log(2) + log_binom

    # Неравенство: total_log <= k * w * ln(3)
    # Решаем относительно w: w >= total_log / (k * ln(3))
    # Округляем вверх до целого числа
    w = math.ceil(total_log / (k * math.log(3)))
    return w


# --- Тесты для функции min_weighings ---

class TestMinWeighings(unittest.TestCase):
    def test_case_1(self):
        # Пример: 1 фальшивая монета из 12 при 1 весе.
        # Независимо от известного отклонения, для n=12, m=1, k=1 ожидаем 3 взвешивания.
        self.assertEqual(min_weighings(1, 12, 1, known_type=False), 3)
        self.assertEqual(min_weighings(1, 12, 1, known_type=True), 3)

    def test_case_2(self):
        # Пример: 1 фальшивая монета из 3 при 1 весе.
        # Для неизвестного отклонения: считаем 2^1 * C(3,1) = 6 вариантов => ln(6)/ln(3) ≈ 1.63, ceil = 2.
        # Для известного отклонения: C(3,1) = 3 вариантов => ln(3)/ln(3) = 1, ceil = 1.
        self.assertEqual(min_weighings(1, 3, 1, known_type=False), 2)
        self.assertEqual(min_weighings(1, 3, 1, known_type=True), 1)

    def test_case_3(self):
        # Пример: 2 фальшивых монеты из 20 при 1 весе.
        # Независимый (неизвестное отклонение): 2^2 * C(20,2) = 4 * 190 = 760 вариантов.
        # Для известного отклонения: C(20,2) = 190 вариантов.
        # Ожидаем, что функция вернет 7 взвешиваний для неизвестного и 5 для известного варианта.
        self.assertEqual(min_weighings(2, 20, 1, known_type=False), 7)
        self.assertEqual(min_weighings(2, 20, 1, known_type=True), 5)

    def test_case_4(self):
        # Пример из предыдущего расчета:
        # 500 фальшивых из 50 000 000 при 10 весах.
        # Для неизвестного отклонения: ожидаем ~556 раундов, для известного ~524.
        self.assertEqual(min_weighings(500, 50_000_000, 10, known_type=False), 556)
        self.assertEqual(min_weighings(500, 50_000_000, 10, known_type=True), 524)

    def test_case_5(self):
        # Пример: 1 фальшивая монета из 3 при 2 весах.
        # При 2 весах количество исходов за раунд=3^2=9.
        # Для неизвестного отклонения: 2 * C(3,1)=6 вариантов, ln(6)/(2 ln3) ≈ 0.815, ceil=1.
        # Для известного отклонения: C(3,1)=3 вариантов, ln(3)/(2 ln3) ≈ 0.5, ceil=1.
        self.assertEqual(min_weighings(1, 3, 2, known_type=False), 1)
        self.assertEqual(min_weighings(1, 3, 2, known_type=True), 1)


if __name__ == '__main__':
    unittest.main()
