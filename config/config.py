from numpy.random import randint


class Config(object):
    run_length = 250

    regions = 16   # should *always* be a square map
    region_size = 25  # each region is itself square

    transport_cost = 1

    number_of_bids = 5  # number of container bids
    idle_max = 3  # number of days before container repositions to hub

    number_of_containers = 128
    number_of_producers = 64
    number_of_transporters = 48

    producer_surplus_percentage = 0.5  # = 50%
    container_surplus_percentage = 1 - producer_surplus_percentage

    container_starting_account_value = 1000
    producer_starting_account_value = 1000

    transport_speed = 25
    storage_capacity = 20
    storage_urgency_level = 0.3

    debug = False
    surplus_tool_debug = False
    plot = False

    warmup_period = 100

    @staticmethod
    def producer_production_rate():
        return randint(1, 2)
