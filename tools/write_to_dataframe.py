import pandas as pd

def write_to_dataframe(environment, containerinfo, shipmentinfo,
                       transporterinfo, producer_storage_info):
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

    return [containerinfo_df,shipmentinfo_df,transporterinfo_df,
            producer_storage_info_df]


