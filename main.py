import random
from pprint import pprint

import vehicle_routing as vr
from search_utils import manhattan_distance

PROBLEM_SEED = 0xdeadbeef
NUM_OF_CITIES = 10
NUM_OF_VEHICLES = 2


def print_routes(vrp, routes, *, short=False):
    if short:
        print()
        pprint(routes)
    else:
        for i, route in enumerate(routes):
            print()
            print(f'Route for vehicle {i}:')
            print(' -> '.join(f'{city1} -> {city2}' for city1, city2, _ in route))
            print(f'Length of route: {vr.route_cost(vrp.cities, route, manhattan_distance)}')
        print()

    print(f'*** Total cost: {vr.total_cost(vrp.cities, routes, manhattan_distance)}')


def main():
    vrp = vr.VRPPD(
        random_seed=PROBLEM_SEED,
        num_of_cities=NUM_OF_CITIES,
        num_of_vehicles=NUM_OF_VEHICLES
    )

    print('Cities:')
    pprint(vrp.cities)
    print('Deliveries:')
    pprint(vrp.deliveries)

    delivery_nodes = vrp.get_delivery_nodes(manhattan_distance)
    print('Nodes:')
    pprint(delivery_nodes)

    routes = vr.generate_routes(delivery_nodes, vrp.num_of_vehicles)
    print_routes(vrp, routes)

    best_routes = routes

    for i in range(10 ** 3):
        new_routes = vr.route_2_opt(routes)

        for j, route in enumerate(new_routes):
            new_routes[j] = vr.city_2_opt(route)

        if vr.is_better(vrp.cities, manhattan_distance, new_routes, routes) or random.random() < 0.01:
            routes = new_routes

        if vr.is_better(vrp.cities, manhattan_distance, new_routes, best_routes):
            best_routes = new_routes

        if i % 10 ** 1 == 0:
            print_routes(vrp, routes, short=True)

    print()
    print('Best routes:')
    print_routes(vrp, best_routes)


if __name__ == '__main__':
    main()
