import random
import numpy as np
from operator import itemgetter

class PSO:
    # В данном конструкторе инициализируем параметры алгоритма:
    # оптимизируемую функцию, кол-во частиц в стае, диапазоны начальных позиций частиц по Ox и Oy,
    # а также коэффициенты для влияния на движение частиц.
    def __init__(self, func, population, position_x, position_y, fi_p, fi_g):
        self.func = func
        self.population = population

        self.pos_x = float(position_x)
        self.pos_y = float(position_y)

        # Проверяем, что fi_p + fi_g > 4, иначе срабатывает исключение.
        assert fi_p + fi_g > 4, "Сумма коэффициентов должна быть > 4"
        self.fi_p = fi_p
        self.fi_g = fi_g

        # Вычисляем параметр xi, который используется при обновлении скорости частиц по формуле.
        self.xi = 2 / (np.abs(2 - (fi_p + fi_g) - np.sqrt((fi_p + fi_g) ** 2 - 4 * (fi_p + fi_g))))

        # Инициализируется стартовая популяция частиц particles, каждая из которых представлена как список [x, y, fitness],
        # где x и y - начальные координаты частиц, а fitness - значение функции func в этих координатах.
        self.particles = [[random.uniform(-self.pos_x, self.pos_x), random.uniform(-self.pos_y, self.pos_y), 0.0]
                          for _ in range(self.population)]
        for i in self.particles:
            i[2] = self.func(i[0], i[1])

        # Создается копия популяции nostalgia, использующаяся для хранения "лучших" позиций частиц.
        self.nostalgia = self.particles.copy()

        # Инициализируется массив velocity, который представляет скорость каждой частицы (изначально все скорости установлены в 0).
        self.velocity = [[0.0 for _ in range(2)] for _ in range(self.population)]

        # Находится начальное лучшее решение generation_best, выбирая частицу с минимальным значением fitness из текущей популяции.
        self.generation_best = min(self.particles, key=itemgetter(2))

    # update_velocity используется для обновления скорости частиц.
    def update_velocity(self, velocity, particle, point_best) -> list:
        new_vel = list()
        for i in range(2):
            r1 = random.random()
            r2 = random.random()

            new_vel.append(self.xi * (velocity[i] + self.fi_p * r1 * (point_best[i] - particle[i]) + self.fi_g * r2 * (
                    self.generation_best[i] - particle[i])))
        return new_vel

    # update_position используется для обновления позиции частиц.
    def update_position(self, velocity, particle):
        x = particle[0] + velocity[0]
        y = particle[1] + velocity[1]

        return [x, y, self.func(x, y)]

    # next_iteration обновляет скорость и позицию каждой частицы и сравнивает их со значениями в nostalgia,
    # затем обновляет generation_best, который будет содержать координаты наилучшей позиции.
    def next_iteration(self):
        for i in range(self.population):

            if self.nostalgia[i][2] < self.particles[i][2]:
                point_best = self.nostalgia[i]
            else:
                self.nostalgia[i] = self.particles[i]
                point_best = self.particles[i]

            self.velocity[i] = PSO.update_velocity(self, self.velocity[i], self.particles[i], point_best)
            self.particles[i] = PSO.update_position(self, self.velocity[i], self.particles[i])

        self.generation_best = min(self.particles, key=itemgetter(2))