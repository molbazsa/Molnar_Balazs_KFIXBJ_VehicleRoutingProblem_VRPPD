import math
import random


class CoolingStrategy:
    @staticmethod
    def multiplicative(t0, alpha):
        return lambda t: t0 / (1 + alpha * t)


class SimulatedAnnealing:
    def __init__(self, cooling, initial_cost):
        self.least_cost = initial_cost
        self.cooling = cooling

    def probability(self, iteration, current_cost):
        if current_cost < self.least_cost:
            self.least_cost = current_cost
            return 1

        temperature = self.cooling(iteration)
        return math.exp(-(current_cost - self.least_cost) / temperature)

    def should_accept(self, iteration, current_cost):
        return random.random() < self.probability(iteration, current_cost)
