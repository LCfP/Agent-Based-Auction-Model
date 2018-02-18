from environment_continuous import Environment_continuous
from env_activities import *
from enums import EntityTypes, ContainerState, ShipmentState, TransporterState
import pandas as pd
from tools import *
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

        # END OF HOURLY SIMULATION ACTIONS


        # DATA GATHERING

        # Store container state info in dict
        containerinfo = gathering_containerinfo(containerinfo, environment)

        # Store shipment state info in dict
        shipmentinfo = gathering_shipmentinfo(shipmentinfo, environment, hour)

        # Store transporter state info in dict
        transporterinfo = gathering_transporterinfo(transporterinfo,environment)

        # Store producer storage level in dict
        producer_storage_info = gathering_storage_info(producer_storage_info,
                                                       environment)

    # REWRITE DICTS TO DATAFRAMES

    # Create dataframe for containerinfo
    containerinfo_df = pd.DataFrame(containerinfo)

    # Rewrite shipment info dict
    for key in shipmentinfo:
        shipmentinfo[key] = pd.Series(shipmentinfo[key][0],
                                      index=shipmentinfo[key][1])
    # Create dataframe for shipmentinfo
    shipmentinfo_df = pd.DataFrame(shipmentinfo)

    # Create dataframe for transporterinfo
    transporterinfo_df = pd.DataFrame(transporterinfo)

    # Create dataframe for producer storage utilisation info
    producer_storage_info_df = pd.DataFrame(producer_storage_info)

    # REMOVE DATA FROM WARMUP PERIOD
    containerinfo_df = containerinfo_df.iloc[
                       environment.config.warmup_period:]
    # shipmentinfo_df = shipmentinfo_df.iloc[
    # environment.config.warmup_period:]
    transporterinfo_df = transporterinfo_df.iloc[
                         environment.config.warmup_period:]

    # ANALYSE DATA

    container_state_averages = states_analysis(containerinfo_df,
                                               ContainerState)
    shipment_state_averages = states_analysis(shipmentinfo_df,
                                              ShipmentState)
    transporter_state_averages = states_analysis(transporterinfo_df,
                                                 TransporterState)

    # Plot storage utilisation and percentage of containers being idle over time
    storage_utilisation(producer_storage_info_df)
    idle_containers(containerinfo_df)

    KPI_run_stats_df = calculate_KPI_run_stats(matching_distances,
                                               container_state_averages,
                                               shipment_state_averages,
                                               transporter_state_averages,
                                               exp_no)

    # save this experiment
    os.makedirs("./experiments/{0}".format(exp_no))

    if len(matching_distances) > 0:
        KPI_run_stats_df.to_csv("./experiments/{0}/KPI_run_stats_df.csv"
                            .format(exp_no))

    else: print('no matches made')


def job(space):
    for exp_no in range(*space):
        print("Job: {0}".format(exp_no))
        run_sim(exp_no)


if __name__ == "__main__":
    run_sim(1)
    # no_threads = 3
    # jobs_per_thread = 34
    #
    # executor = ProcessPoolExecutor(no_threads)
    # items = [[start, start + jobs_per_thread] for start in range(
    #     0, jobs_per_thread * no_threads, jobs_per_thread)]
    #
    # futures = [executor.submit(job, item) for item in items]
    # wait(futures)


