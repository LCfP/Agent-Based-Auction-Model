from environment import Environment
from enums import EntityTypes, ContainerState

environment = Environment()
environment.setup()

for _ in range(environment.config.run_length):  # run model!

    for producer in environment.producers:
        producer.produce() # all producers produce according to their production rate
        for shipment in producer.storage: # all shipments that are produced are registered at the auction
            if EntityTypes.__members__['SHIPMENT'] not in \
                        producer.region.auctioneer.entities.keys(): # the first if statement would not be necessary if the dict already has the key...
                registrationkey = producer.region.auctioneer.register(shipment)
                bid = producer.bid(registrationkey,shipment)
                producer.region.auctioneer.list_shipment(bid)
            elif shipment not in producer.region.auctioneer.entities[EntityTypes.SHIPMENT].values():
                registrationkey = producer.region.auctioneer.register(shipment)
                bid = producer.bid(registrationkey, shipment)
                producer.region.auctioneer.list_shipment(bid)

    for container in environment.containers: # the first if would not be necessary if the dict already has the key...
        if EntityTypes.__members__['CONTAINER'] not in \
            container.region.auctioneer.entities.keys():
            if container.state == ContainerState.EMPTY: #when container is empty he registers at the auction
                registrationkey = container.region.auctioneer.register(container) # registers at auction of region container is currently in
                container_bids = container.bidding_proces(registrationkey)
                for bid in container_bids:
                    container.region.auctioneer.container_bids.append(bid)
        # same as above, only checks if container is not already registered
        elif container not in container.region.auctioneer.entities[EntityTypes.CONTAINER].values():
            if container.state == ContainerState.EMPTY:
                registrationkey = container.region.auctioneer.register(container)
                container_bids = container.bidding_proces(registrationkey)
                for bid in container_bids:
                    container.region.auctioneer.container_bids.append(bid)


