from environment import Environment
from enums import EntityTypes, ContainerState, ShipmentState


environment = Environment()
environment.setup()

for _ in range(environment.config.run_length):  # run model!

    for producer in environment.producers:
        producer.produce() # all producers produce according to their production rate
        for shipment in producer.storage: # all shipments that are produced are registered at the auction
            if shipment.state == ShipmentState.STORAGED:
                if EntityTypes.SHIPMENT not in producer.region.auctioneer.entities.keys() or \
                shipment not in producer.region.auctioneer.entities[EntityTypes.SHIPMENT].values():
                    registrationkey = producer.region.auctioneer.register(shipment)
                    bid = producer.bid(registrationkey,shipment)
                    producer.region.auctioneer.list_shipment(bid)


    for container in environment.containers: # the first if would not be necessary if the dict already has the key...
        if container.state == ContainerState.EMPTY:
            if EntityTypes.CONTAINER not in container.region.auctioneer.entities.keys() or \
            container not in container.region.auctioneer.entities[EntityTypes.CONTAINER].values(): #when container is empty he registers at the auction
                registrationkey = container.region.auctioneer.register(container) # registers at auction of region container is currently in
                container_bids = container.bidding_proces(registrationkey)
                for bid in container_bids:
                    container.region.auctioneer.list_container_bid(bid)


    for region in environment.regions:
        matches = region.auctioneer.match_containers_shipments() # run the auction in each region
        invoices = region.auctioneer.invoice_producers(matches) # when containers and shipments are matched, create invoices
        for invoice in invoices:
            for producer in environment.producers:
                if invoice.producer_id == producer.id:
                    payment = producer.pay_invoice(invoice) # each producer pays the invoice of his matched shipment
                    region.auctioneer.account_value += payment
        region.auctioneer.pay_container(matches) # each container is payed for the shipment he won
        region.auctioneer.finalize_matchmaking(matches) # unregistration, and assignment of shipment contract to container


    for container in environment.containers:
        if container.state == ContainerState.NEEDING_TRANSPORT:
            environment.transportcompany.assign_transporter(container) # change to interaction? container request before assignment


    for transporter in environment.transportcompany.transporters:
        transporter.move()
        transporter.status_update()
