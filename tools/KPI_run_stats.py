from enums import ContainerState, ShipmentState, TransporterState
import pandas as pd

def calculate_KPI_run_stats(matching_distances, container_state_averages,
                            shipment_state_averages, transporter_state_averages,
                            exp_no):

    if len(matching_distances) > 0:

        # Save KPI data of run
        KPI_run_stats = {'number of matches': len(matching_distances),
                         'average match distance':
                             sum(matching_distances)/len(matching_distances),
                         'average container idle time':
                             container_state_averages[ContainerState.EMPTY.name],
                         'average shipment idle time':
                             shipment_state_averages[ShipmentState.STORED.name],
                         'average transporter idle time':
                            transporter_state_averages[TransporterState.EMPTY.name]}

        KPI_run_stats_df = pd.DataFrame(KPI_run_stats, index= [exp_no])

        # print(KPI_run_stats_df)

        return KPI_run_stats_df