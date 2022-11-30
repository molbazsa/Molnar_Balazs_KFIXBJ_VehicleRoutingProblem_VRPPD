import matplotlib.pyplot as plt
from pprint import pprint

import vehicle_routing as vr
from search_utils import manhattan_distance
from simulated_annealing import SimulatedAnnealing, CoolingStrategy

PROBLEM_SEED = 0xdeadbeef
NUM_OF_CITIES = 100
NUM_OF_VEHICLES = 10

T_ZERO = 100_000
ALPHA = 0.05
DISTANCE = manhattan_distance

ITERATIONS = 10_000
TRACING_INTERVAL = 100
GRAPH_INTERVAL = 1


def print_routes(vrp, routes, *, short=False):
    cost = vr.Cost(vrp.cities, DISTANCE)

    if short:
        print()
        pprint(routes)
    else:
        for i, route in enumerate(routes):
            print()
            print(f'Route for vehicle {i}:')
            print(' -> '.join(f'{city1} -> {city2}' for city1, city2, _ in route))
            print(f'Length of route: {cost.route_cost(route)}')
        print()

    print(f'*** Total cost: {cost.total_cost(routes)}')


def show_graph(graph):
    temperatures = list(map(lambda g: g[0], graph))
    probabilities = list(map(lambda g: g[1], graph))
    costs = list(map(lambda g: g[2], graph))

    fig, axis1 = plt.subplots()
    axis2 = axis1.twinx()
    axis3 = axis1.twinx()

    axis1.plot(temperatures, color='red', label='Temperature')
    axis1.set_ylabel('Temperature')
    axis1.legend(loc=[0, 0])

    axis2.plot(probabilities, color='orange', label='Probability')
    axis2.get_yaxis().set_visible(False)
    axis2.legend(loc=[0, 1])

    axis3.plot(costs, color='green', alpha=0.5, label='Cost')
    axis3.set_ylabel('Cost')
    axis3.legend(loc=[1, 0])

    plt.show()


def main():
    # global NUM_OF_CITIES
    # global NUM_OF_VEHICLES
    #
    # nc = input('Num of cities: ')
    # if nc:
    #     NUM_OF_CITIES = int(nc)
    #
    # nv = input('Num of vehicles: ')
    # if nv:
    #     NUM_OF_VEHICLES = int(nv)

    vrp = vr.VRPPD(
        random_seed=PROBLEM_SEED,
        num_of_cities=NUM_OF_CITIES,
        num_of_vehicles=NUM_OF_VEHICLES
    )

    print('Cities:')
    pprint(vrp.cities)
    print('Deliveries:')
    pprint(vrp.deliveries)

    delivery_nodes = vrp.get_delivery_nodes(DISTANCE)
    print('Nodes:')
    pprint(delivery_nodes)

    routes = vr.generate_routes(delivery_nodes, vrp.num_of_vehicles)
    print_routes(vrp, routes)

    cost = vr.Cost(vrp.cities, DISTANCE)
    initial_cost = cost.total_cost(routes)
    sa = SimulatedAnnealing(CoolingStrategy.multiplicative(T_ZERO, ALPHA), initial_cost)
    best_routes = routes

    graph = []

    for i in range(ITERATIONS):
        new_routes = vr.route_2_opt(routes)

        for j, route in enumerate(new_routes):
            new_routes[j] = vr.city_2_opt(route)

        new_routes_cost = cost.total_cost(new_routes)

        if sa.should_accept(i, new_routes_cost):
            routes = new_routes

        if cost.is_better(new_routes, best_routes):
            best_routes = new_routes

        if i % TRACING_INTERVAL == 0:
            print_routes(vrp, routes, short=True)
            print(f't = {sa.cooling(i)}, p = {sa.probability(i, new_routes_cost)}')

        graph.append((sa.cooling(i), sa.probability(i, new_routes_cost), cost.total_cost(routes)))

    print()
    print('Best routes:')
    print_routes(vrp, best_routes)

    show_graph(graph)


if __name__ == '__main__':
    main()
