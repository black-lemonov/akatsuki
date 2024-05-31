from random import uniform, random, randint
from typing import Callable
from operator import itemgetter
from math import floor

class GeneticAlgorithm:
    '''Реализация генетического алгоритма Татаряна-Парфинцова'''
    def __init__(
            self,
            fitness          : Callable[[float, float], float], 
            generations_limit: int   = 50, 
            is_min           : bool  = True, 
            p_mutation       : float = 0.8, 
            p_survive        : float = 0.8, 
            population_size  : float = 100
            ):
        '''
        fitness          : функция для оптимизации\n
        generations_limit: кол-во поколений\n
        is_min           : искать минимум или нет\n 
        p_mutation       : вероятность мутации\n
        p_survive        : веротность выживаемости\n 
        population_size  : размер популяции
        '''
        self.fitness           = fitness
        self.population        = []
        self.p_mutation        = p_mutation
        self.p_survive         = p_survive
        self.generations_limit = generations_limit
        self.population_size   = population_size
        self.is_min            = is_min

    def generate_start_population(
            self, 
            x_bound: int, 
            y_bound: int
            ):
        '''
        Генерирует начальную популяцию особей вида [x, y, fitness(x,y)]\n
        на отрезках [-x_bound, +x_bound] и [-y_bound, +y_bound].
        '''
        self.population = [
            [
                x:=uniform(-x_bound, x_bound),
                y:=uniform(-y_bound, y_bound),
                self.fitness(x, y)
            ]
            for _ in range(self.population_size)
        ]

    def best(self):
        '''
        Возвращает лучшую особь на основании фитнес-функции
        '''
        return min(self.population, key=itemgetter(2)) if self.is_min else max(self.population, key=itemgetter(2))

    def select(self):
        '''
        Упорядочивает особей в популяции по фитнес-функции\n
        и выбирает родителей для следующего поколения
        '''
        self.population.sort(key=itemgetter(2), reverse=self.is_min)    # ранжирование

        # Кроссинговер - случайным образом выбираются 2 родителя и создаются 2 ребенка путем обмена их генами.
        children_count = floor(self.population_size * (1 - self.p_survive))
        parents = self.population[self.population_size - 2 * children_count:]

        for one in self.population[:children_count]:
            if random() > 0.5:
                one[0], one[1], one[2] = (x:=parents.pop()[0]), (y:=parents.pop()[1]), self.fitness(x, y)
            else:
                one[1], one[0], one[2] = (y:=parents.pop()[1]), (x:=parents.pop()[0]), self.fitness(x, y)

    def mutation(self):
        '''
        Вносятся случайные изменения в гены с определенной вероятностью,\n
        что помогает исследовать новые области пространства решений.\n
        '''
        for one in self.population:
            if random() < self.p_mutation:
                one[0] += randint(-1, 1) * 0.1 * one[0]
            if random() < self.p_mutation:
                one[1] += randint(-1, 1) * 0.1 * one[1]
            one[2] = self.fitness(one[0], one[1])