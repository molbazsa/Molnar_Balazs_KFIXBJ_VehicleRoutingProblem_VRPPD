from pprint import pprint

from vehicle_routing import VRPPD

PROBLEM_SEED = 0xdeadbeef
NUM_OF_CITIES = 10
NUM_OF_VEHICLES = 2


def main():
    vrp = VRPPD(
        random_seed=PROBLEM_SEED,
        num_of_cities=NUM_OF_CITIES,
        num_of_vehicles=NUM_OF_VEHICLES
    )

    pprint(vrp.cities)
    pprint(vrp.deliveries)


if __name__ == '__main__':
    main()
