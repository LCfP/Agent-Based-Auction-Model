from numpy.random import randint


class Config(object):
    price_range = [0, 10]  # say for a uniform distribution
    quantity_range = [100, 1500]  # again uniform?
    run_length = 250
    number_of_containers = 20
    number_of_producers = 5

    regions = 9  # should *always* be a square map
    region_size = 50  # each region is itself square

    transport_cost = 1

    @staticmethod
    def producer_production_rate():
        return randint(1, 4)
