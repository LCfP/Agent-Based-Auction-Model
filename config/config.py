from numpy.random import randint


class Config(object):
    price_range = [0, 10]  # say for a uniform distribution
    quantity_range = [100, 1500]  # again uniform?
    run_length = 1
    random_agent_creation = .05

    regions = 9  # should *always* be a square map
    region_size = 50  # each region is itself square

    transport_cost = 1

    number_of_bids = 3

    number_of_containers = 40
    number_of_producers = 20

    producer_surplus_percentage = 0.5 # = 50%
    container_surplus_percentage = 1 - producer_surplus_percentage

    container_starting_account_value = 1000
    producer_starting_account_value = 1000

    @staticmethod
    def producer_production_rate():
        return randint(1, 4)


