from environment_continuous import Environment_continuous
from env_activities import *
from enums import EntityTypes, ContainerState, ShipmentState, TransporterState
import pandas as pd
from tools import gathering_shipmentinfo, calculate_matching_distance
from analysis import states_analysis, storage_utilisation, idle_containers
from math import floor

from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures import wait
import os


def run_sim(exp_no):
    environment = Environment_continuous()
    environment.setup()

    #KPI data storage
    containerinfo = {}
    shipmentinfo = {}
    transporterinfo = {}
    producer_storage_info = {}
    matching_distances = []

    for hour in range(environment.config.run_length):  # run model!

        if environment.config.debug:
            print(" \n \033[1m start of hour %s of day %s"
                  %(hour % environment.config.hours_in_day,
                    floor(hour/environment.config.hours_in_day)))
            print('\033[0m')

        # Transportation "during" the hour
        transportation(environment)

        # Production of shipments, and registration of shipments on auction
        production_registration_continuous(environment)

        # Container registers at auction, creates bids, participates in auction
        # and when no match is made, the container un-registers himself
        container_auction_process(environment,matching_distances,hour)

        # Assign transport for containers that have obtained a shipment contract
        assign_transport(environment)

        # When container is idle for too long and not at a hub, he initiates
        # transport to a hub
        container_idle_management(environment)

        # Assign transport for containers in need of relocation
        assign_relocation_transport(environment)

# run experiment
run_sim(1)