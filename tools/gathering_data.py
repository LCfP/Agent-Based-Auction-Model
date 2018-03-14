from tools import gathering_containerinfo, gathering_shipmentinfo, \
    gathering_transporterinfo, gathering_storage_info

def gathering_data(environment, day, containerinfo, shipmentinfo,
                   transporterinfo, producer_storage_info):
    # Store container state info in dict
    gathering_containerinfo(containerinfo, environment)

    # Store shipment state info in dict
    shipmentinfo = gathering_shipmentinfo(shipmentinfo, environment, day)

    # Store transporter state info in dict
    transporterinfo = gathering_transporterinfo(transporterinfo,
                                                environment)

    # Store producer storage level in dict
    producer_storage_info = gathering_storage_info(producer_storage_info,
                                                   environment)