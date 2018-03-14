from analysis import states_analysis, storage_utilisation, idle_containers
from enums import ContainerState, ShipmentState, TransporterState
import pandas as pd
import os


def calculate_averages(data: list, matching_distances, exp_no):
    # Analyse data
    container_state_averages = states_analysis(data[0], ContainerState)
    shipment_state_averages = states_analysis(data[1], ShipmentState)
    transporter_state_averages = states_analysis(data[2],
                                                 TransporterState)

    # Plot storage utilisation and percentage of containers being idle over time
    storage_utilisation(data[3])
    idle_containers(data[0])


    # Save KPI data of run
    if len(matching_distances) > 0:
        KPI_run_stats = {'number of matches': len(matching_distances),
                         'average match distance':
                             sum(matching_distances) / len(matching_distances),
                         'average container idle time':
                             container_state_averages[
                                 ContainerState.EMPTY.name],
                         'average shipment idle time':
                             shipment_state_averages[ShipmentState.STORED.name],
                         'average transporter idle time':
                             transporter_state_averages[
                                 TransporterState.EMPTY.name]}

        KPI_run_stats_df = pd.DataFrame(KPI_run_stats, index=[exp_no])

        # save this experiment
        os.makedirs("./experiments/{0}".format(exp_no))

        KPI_run_stats_df.to_csv("./experiments/{0}/KPI_run_stats_df.csv"
                                .format(exp_no))

