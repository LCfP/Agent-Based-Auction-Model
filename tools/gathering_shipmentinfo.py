
# shipment info can be stored at producer, container, and consumer

def gathering_shipmentinfo(shipmentinfo : dict, environment, day):

    for producer in environment.producers:
        for shipment in producer.storage:
            if shipment.id not in shipmentinfo.keys():
                shipmentinfo[shipment.id] = [[shipment.state], [day]]

            else:
                shipmentinfo[shipment.id][0].append(shipment.state)
                shipmentinfo[shipment.id][1].append(day)

    for container in environment.containers:
        if container.load != 0:
            if container.load.id not in shipmentinfo.keys():
                shipmentinfo[container.load.id] = [[container.load.state], [day]]
            else:
                shipmentinfo[container.load.id][0].append(container.load.state)
                shipmentinfo[container.load.id][1].append(day)

    for shipment in environment.consumer.products:
        if shipment.id not in shipmentinfo.keys():
            shipmentinfo[shipment.id] = [[shipment.state], [day]]
        else:
            shipmentinfo[shipment.id][0].append(shipment.state)
            shipmentinfo[shipment.id][1].append(day)

    return shipmentinfo