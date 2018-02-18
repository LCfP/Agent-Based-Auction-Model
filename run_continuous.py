from environment_continuous import Environment_continuous
from env_activities import *
from enums import EntityTypes, ContainerState, ShipmentState, TransporterState
import pandas as pd
from tools import gathering_shipmentinfo, calculate_matching_distance
from analysis import states_analysis, storage_utilisation, idle_containers

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

    for day in range(environment.config.run_length):  # run model!

        if environment.config.debug is True:
            print(" \n \033[1m start of day %s" %(day))
            print('\033[0m')

        # Transportation "during" the day
        transportation(environment)

        # Production of shipments, and registration of shipments on auction
        production_registration(environment)

        # Container registers at auction, creates bids, participates in auction
        # and when no match is made, the container un-registers himself
        container_auction_process(environment,matching_distances,day)

