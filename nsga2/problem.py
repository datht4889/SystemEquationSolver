from nsga2.individual import Individual
from input_handler.input_handler import InputHandler
import random


class Problem:

    def __init__(self, objectives, num_of_variables, variables_range, same_range=False):
        self.num_of_variables = num_of_variables
        self.objectives = objectives
        self.variables_range = []
        if same_range:
            for _ in range(num_of_variables):
                self.variables_range.append(variables_range[0])
        else:
            self.variables_range = variables_range



    def generate_individual(self):
        individual = Individual()
        individual.features = [random.uniform(*x) for x in self.variables_range]
        return individual

    def calculate_objectives(self, individual):
        # individual.objectives = self.objectives(individual.features)
        input_handler = InputHandler(self.objectives, x = individual.features)
        individual.objectives = input_handler()
