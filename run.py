from environment import Environment
from enums import EntityTypes, ContainerState, ShipmentState
import pandas as pd
from tools import gathering_shipmentinfo, calculate_matching_distance


environment = Environment()
environment.setup()

#KPI data storage
containerinfo = {}
shipmentinfo = {}
matching_distances = []

for day in range(environment.config.run_length):  # run model!

    if environment.config.debug is True:
        print(" \n \033[1m start of day %s" %(day))
        print('\033[0m')

    for transporter in environment.transportcompany.transporters:
        transporter.move()
        transporter.status_update()

    if environment.config.debug is True:
        print(" \n Production and entering shipment bids")

    for producer in environment.producers:
        # all producers produce according to their production rate
        producer.produce()
        # all shipments that are produced are registered at the auction
        for shipment in producer.storage:
            if shipment.state == ShipmentState.STORAGED:
                if EntityTypes.SHIPMENT not in \
                        producer.region.auctioneer.entities.keys() or \
                   shipment not in \
                        producer.region.auctioneer.entities[EntityTypes.SHIPMENT].values():
                    registrationkey = producer.region.auctioneer.register(shipment)
                    bid = producer.bid(registrationkey,shipment)
                    producer.region.auctioneer.list_shipment(bid)

    if environment.config.debug is True:
        print(" \n Container bidding process")

    for container in environment.containers:
        if container.state == ContainerState.EMPTY:
            if EntityTypes.CONTAINER not in container.region.auctioneer.entities.keys() or \
            container not in container.region.auctioneer.entities[EntityTypes.CONTAINER].values(): #when container is empty he registers at the auction
                registrationkey = container.region.auctioneer.register(container) # registers at auction of region container is currently in
                container_bids = container.bidding_proces(registrationkey)
                for bid in container_bids:
                    container.region.auctioneer.list_container_bid(bid)

    if environment.config.debug is True:
        print(" \n Auctioneer matching process")

    for region in environment.regions:

        if environment.config.surplus_tool_debug is True and \
           EntityTypes.CONTAINER in region.auctioneer.entities.keys() and \
           EntityTypes.CONTAINER not in region.auctioneer.entities.keys():
            print("number of containers registered: %s \n"
                  "number of shipments registered: %s"
                  %(len(region.auctioneer.entities[EntityTypes.CONTAINER]),
                    len(region.auctioneer.entities[EntityTypes.SHIPMENT])))

        if environment.config.debug is True:
            print("\n registered items in region %s before matching"
                  %(region.id))
            region.auctioneer.print_shipment_bid_info()
            region.auctioneer.print_container_bid_info()

        matches = region.auctioneer.match_containers_shipments()
        calculate_matching_distance(matches, region.auctioneer,
                                    matching_distances)
        invoices = region.auctioneer.invoice_producers(matches)
        for invoice in invoices:
            for producer in environment.producers:
                if invoice.producer_id == producer.id:
                    payment = producer.pay_invoice(invoice)
                    region.auctioneer.account_value += payment
        region.auctioneer.pay_container(matches)
        region.auctioneer.finalize_matchmaking(matches)

        if environment.config.debug is True:
            print("\n registered items in region %s after matching"
                  % (region.id))
            region.auctioneer.print_shipment_bid_info()
            region.auctioneer.print_container_bid_info()

    for container in environment.containers:
        if container.state == ContainerState.NEEDING_TRANSPORT:
            environment.transportcompany.assign_transporter(container)

    if environment.config.debug is True:
        for container in environment.containers:
            if container.load != 0:
                print("container %s has state %s and "
                      "delivers shipment %s with state%s"
                      % (container.id, container.state, container.load.id,
                         container.load.state))
                for producer in environment.producers:
                    for shipment in producer.storage:
                        if container.load.id == shipment.id:
                            print("ERROR")

    # Containers unregister at end of day to consider new shipment bids next day
    for container in environment.containers:
        if container.state == ContainerState.EMPTY:
            container.losing_auction_response()

    # END OF DAILY SIMULATION ACTIONS

    # store container state info in dict
    for container in environment.containers:
        if container.id not in containerinfo.keys():
            containerinfo[container.id] = [container.state]
        else:
            containerinfo[container.id].append(container.state)

    shipmentinfo = gathering_shipmentinfo(shipmentinfo,environment,day)


# Create dataframe for containerinfo
containerinfo_df = pd.DataFrame(containerinfo)
print(containerinfo_df)

# Rewrite shipment info dict
for key in shipmentinfo:
    shipmentinfo[key] = pd.Series(shipmentinfo[key][0],
                                  index=shipmentinfo[key][1])
# Create dataframe for shipmentinfo
shipmentinfo_df = pd.DataFrame(shipmentinfo)
print(shipmentinfo_df)

# matching distance
print(matching_distances)
print(len(matching_distances))

# Data analysis
container_idletimes = []
for container_id in containerinfo_df:
    idletime = (containerinfo_df[container_id] == ContainerState.EMPTY).sum()  \
                / len(containerinfo_df[container_id])
    container_idletimes.append(idletime)







