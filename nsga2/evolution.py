from nsga2.utils import NSGA2Utils
from nsga2.population import Population
from tqdm import tqdm


class Evolution:

    def __init__(self, problem, num_of_generations=1000, num_of_individuals=100, num_of_tour_particips=2,
                 tournament_prob=0.9, crossover_param=2, mutation_param=5):
        self.utils = NSGA2Utils(problem, num_of_individuals, num_of_tour_particips, tournament_prob, crossover_param,
                                mutation_param)
        self.population = None
        self.num_of_generations = num_of_generations
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals
        self.plot_populations = []

    def evolve(self):
        returned_population = None

        # Initial random Population
        self.population = self.utils.create_initial_population()
        self.utils.fast_nondominated_sort(self.population)
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)

        # Initial random Children
        children = self.utils.create_children(self.population)

        for i in tqdm(range(self.num_of_generations)):
            self.population.extend(children)
            self.utils.fast_nondominated_sort(self.population)

            # Create new_population with the best individuals
            new_population = Population()
            front_num = 0
            while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1
            self.utils.calculate_crowding_distance(self.population.fronts[front_num])
            self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
            new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals - len(new_population)])

            returned_population = self.population
            self.plot_populations.append(sorted(returned_population.fronts[0], key=lambda x: x.objectives[-1])) # save sorted best Pareto Front each generation
            # self.plot_populations.append(sorted(returned_population.fronts[0], key=lambda x: sum(x.objectives)))

            self.population = new_population
            self.utils.fast_nondominated_sort(self.population)
            for front in self.population.fronts:
                self.utils.calculate_crowding_distance(front)
            children = self.utils.create_children(self.population)

            if i % 20 == 0:
                f_check = [i.objectives for i in self.plot_populations[-1]][0][-1]
                if f_check <= 1e-6:
                    return returned_population.fronts[0]
        return returned_population.fronts[0]
