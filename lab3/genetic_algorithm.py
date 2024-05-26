from random import uniform, random

class GeneticAlgorithm:
    # Функция приспособленности, количество поколений, вероятность мутации, коэффициент выживаемости, размер популяции.
    def __init__(self, func, generations=50, min=True, mut_chance=0.8, survive_cof=0.8, pop_number=100):
        self.func = func
        self.population = dict()
        self.mut_chance = mut_chance
        self.survive_cof = survive_cof
        self.generations = generations
        self.pop_number = pop_number
        self.min_func = min

# Генерирует исходную популяцию особей, каждая из которых представлена двумя генами (x и y)
# и соответствующим им значением приспособленности.
    def generate_start_population(self, x, y):
        for i in range(self.pop_number):
            po_x = uniform(-x, x)
            po_y = uniform(-y, y)
            self.population[i] = [po_x, po_y, self.func(po_x, po_y)]  # Создание начальной популяции

# Возвращает лучших и худших индивидуумов в текущей популяции на основе их показателей физической подготовки.
    def statistic(self):
        return [max(self.population.items(), key=lambda item: item[1][2]),
                min(self.population.items(), key=lambda item: item[1][2])]

# Выполняет процесс отбора, который упорядочивает особей в популяции на основе их показателей пригодности
# и выбирает родителей для следующего поколения.
    def select(self):
        sorted_pop = dict(
            sorted(self.population.items(), key=lambda item: item[1][2], reverse=self.min_func))  # Ранжирование
# Кроссинговер - случайным образом выбираются 2 родителя и создаются 2 ребенка путем обмена их генами.
        cof = int(self.pop_number * (1 - self.survive_cof))
        parents1 = list(sorted_pop.items())[cof: cof * 2]
        parents2 = list(sorted_pop.items())[self.pop_number - cof: self.pop_number]

        i = 0
        for pop in sorted_pop.values():
            if random() > 0.5:
                pop[0] = parents1[i][1][0]
                pop[1] = parents2[i][1][1]
                pop[2] = self.func(parents1[i][1][0], parents2[i][1][1])
            else:
                pop[0] = parents2[i][1][0]
                pop[1] = parents1[i][1][1]
                pop[2] = self.func(parents2[i][1][0], parents1[i][1][1])
            i += 1
            if i >= cof:
                break

        self.population = sorted_pop

# Вносятся случайные изменения в гены индивидуумов с определенной вероятностью,
# что помогает исследовать новые области пространства решений.
    def mutation(self, cur_gen):
        for pop in self.population.values():
            if random() < self.mut_chance:
                pop[0] += (random() - 0.5) * ((self.generations - cur_gen) / self.generations)
            if random() < self.mut_chance:
                pop[1] += (random() - 0.5) * ((self.generations - cur_gen) / self.generations)
            pop[2] = self.func(pop[0], pop[1])