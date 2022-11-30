import copy
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
        self.deliveries = [city_pair for city_pair in zip(delivery_indices[0::2], delivery_indices[1::2])]

    def get_delivery_nodes(self, distance_func):
        depot, *cities = self.cities
        return [
            (city1, city2, distance_func(cities[city1], cities[city2]))
            for city1, city2 in self.deliveries
        ]


class Cost:
    def __init__(self, cities, distance_func):
        self.cities = cities
        self.distance = distance_func

    def route_cost(self, route):
        depot, *cities = self.cities
        route_cost_sum = 0
        current_city = depot

        for node in route:
            start_index, end_index, inner_cost = node
            start = cities[start_index]
            end = cities[end_index]

            route_cost_sum += self.distance(current_city, start)
            route_cost_sum += inner_cost

            current_city = end

        route_cost_sum += self.distance(current_city, depot)
        return route_cost_sum

    def total_cost(self, routes):
        return sum(
            self.route_cost(route)
            for route in routes
        )

    def is_better(self, routes1, routes2):
        return self.total_cost(routes1) < self.total_cost(routes2)


def generate_routes(delivery_nodes, num_of_vehicles):
    routes = []

    for i in range(num_of_vehicles):
        routes.append(delivery_nodes[i::num_of_vehicles])

    return routes


def city_2_opt(route):
    route = copy.deepcopy(route)

    index1, index2 = random.sample(range(len(route)), 2)
    route[index1], route[index2] = route[index2], route[index1]

    return route


def route_2_opt(routes):
    routes = copy.deepcopy(routes)

    index1, index2 = random.sample(range(len(routes)), 2)
    route1 = routes[index1]
    route2 = routes[index2]

    index1 = random.choice(range(len(route1)))
    index2 = random.choice(range(len(route2)))
    route1[index1], route2[index2] = route2[index2], route1[index1]

    return routes
