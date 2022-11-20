"""
This module generates random Vehicle Routing Problems.
"""

import random


def grid_size(num_of_cities):
    """
    Returns the size of the square grid for the number of cities.
    E.g. Right now 10 cities will be placed in a 500 × 500 grid.
    """
    grid_scale = 100
    return num_of_cities // 2 * grid_scale


class VRPPD:
    def __init__(self, *, random_seed=None, num_of_cities: int, num_of_vehicles: int):
        if num_of_cities <= 0:
            raise ValueError('there should be at least 1 city')
        elif num_of_cities % 2 != 0:
            raise ValueError('there should be an even number of cities')

        if num_of_vehicles <= 0:
            raise ValueError('there should be at least 1 vehicle')

        self._random = random.Random(random_seed)

        self.num_of_cities = num_of_cities
        self.num_of_vehicles = num_of_vehicles

        self._generate_problem()

    def _generate_problem(self):
        self._generate_cities()
        self._generate_deliveries()

    def _generate_cities(self):
        """Generate a depot and self.num_of_cities cities."""
        size = grid_size(self.num_of_cities)

        self.cities = []

        def random_city():
            x = self._random.randrange(0, size)
            y = self._random.randrange(0, size)
            return x, y

        # the first city is the depot
        for _ in range(self.num_of_cities + 1):
            city = random_city()
            while city in self.cities:
                city = random_city()
            self.cities.append(city)

    def _generate_deliveries(self):
        """
        Generate pairs of city indices corresponding to deliveries.
        Cities are numbered as if the depot didn't exist.
        That is, the indices are in range(0, self.num_of_cities).
        """
        # shuffle indices
        delivery_indices = self._random.sample(range(self.num_of_cities), self.num_of_cities)

        # pair every two shuffled index
        self.deliveries = [(city1, city2) for city1, city2 in zip(delivery_indices[0::2], delivery_indices[1::2])]
