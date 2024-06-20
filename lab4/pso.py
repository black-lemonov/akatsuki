import numpy as np
from operator import itemgetter
from typing import Callable
from random import uniform, random

class PSO:
    '''
    Реализация роевого алгоритма Татаряна-Парфинцова
    '''
    def __init__(
            self,
            fitness: Callable[[float, float], float],
            particles_number: int,
            x_bound,
            y_bound,
            fi_p,
            fi_g):
        '''
        fitness          : оптимизируемая функция\n
        particles_number : кол-во частиц в стае\n
        x_bound          : ограничение области поиска по X\n
        y_bound          : ограничение области поиска по Y\n
        fi_p             : коэффициент для коррекции скорости\n
        fi_p             : коэффициент для коррекции скорости
        '''
        self.fitness = fitness
        self.particles_number = particles_number

        # Проверяем, что fi_p + fi_g > 4,
        # иначе срабатывает исключение.
        assert fi_p + fi_g > 4, "Сумма коэффициентов должна быть > 4"
        self.fi_p = fi_p
        self.fi_g = fi_g

        # Вычисляем параметр xi,
        # который используется при обновлении скорости частиц по формуле
        self.Xi = 2 / (np.abs(2 - (fi_p + fi_g) - np.sqrt((fi_p + fi_g) ** 2 - 4 * (fi_p + fi_g))))

        # Инициализируется стартовая популяция частиц particles,
        # каждая из которых представлена как список [x, y, fitness],
        # где x и y - начальные координаты частиц,
        # а fitness - значение функции fitness в этих координатах
        self.particles = [
            [
                _x := uniform(-x_bound, x_bound),
                _y := uniform(-y_bound, y_bound), 
                fitness(_x, _y)
            ]
            for _ in range(particles_number)
        ]

        # Создается копия популяции nostalgia,
        # использующаяся для хранения лучших позиций частиц
        self.nostalgia = self.particles.copy()

        # Инициализируется массив velocity,
        # который представляет скорость каждой частицы
        # (изначально все скорости установлены в 0)
        self.velocity = [
            [0.0] * 3
            for _ in range(particles_number)
        ]

        # Находится начальное лучшее решение generation_best,
        # выбирая частицу с минимальным значением fitness
        # из текущей популяции.
        self.generation_best = min(self.particles, key=itemgetter(2))


    def update_velocity(
            self,
            velocity  : list[float],
            particle  : list[float], 
            point_best: list[float]) -> list[float]:
        '''
        Обновление скорости частиц по формуле ☠
        '''
        formula: Callable[[float], float] = lambda i: self.Xi * (velocity[i] + self.fi_p * random() * (point_best[i] - particle[i]) + self.fi_g * random() * (self.generation_best[i] - particle[i])) 
        return [
            formula(0),
            formula(1)
        ]    

    def update_position(
            self,
            velocity  : list[float],
            particle  : list[float]) -> list[float]:
        '''
        Обновление позиции частицы
        '''
        x = particle[0] + velocity[0]
        y = particle[1] + velocity[1]

        return [x, y, self.fitness(x, y)]
