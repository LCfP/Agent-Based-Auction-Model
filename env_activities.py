from enums import EntityTypes, ShipmentState, ContainerState
from tools import calculate_matching_distance

def daily_actions(environment, matching_distances, day):
    transportation(environment)

    production_registration(environment)

    container_bidding_proces(environment)

    auctioning(environment, matching_distances, day)

    assign_transport(environment)

    container_auction_response(environment)

    assign_relocation_transport(environment)


def continuous_actions(environment, matching_distances, day):

    transportation(environment)

    production_registration_continuous(environment)

    container_auction_process(environment, matching_distances, day)

    assign_transport(environment)

    container_idle_management(environment)

    assign_relocation_transport(environment)


def transportation(environment):
    for transporter in environment.transportcompany.transporters:
        transporter.move()
        transporter.status_update()

def production_registration(environment):
    if environment.config.debug is True:
        print(" \n Production and entering shipment bids")

    for producer in environment.producers:
        # all producers produce according to their production rate
        producer.produce()
        # all shipments that are produced are registered at the auction
        for shipment in producer.storage:
            if shipment.state == ShipmentState.STORED:
                if EntityTypes.SHIPMENT not in \
                        producer.region.auctioneer.entities.keys() or \
                                shipment not in \
                                producer.region.auctioneer.entities[
                                    EntityTypes.SHIPMENT].values():
                    registrationkey = producer.region.auctioneer.register(
                        shipment)
                    bid = producer.bid(registrationkey, shipment)
                    producer.region.auctioneer.list_shipment(bid)

def production_registration_continuous(environment):
    if environment.config.debug is True:
        print(" \n Production and entering shipment bids")

    for producer in environment.producers:
        # all producers produce according to their production rate
        producer.produce_continuous()
        # all shipments that are produced are registered at the auction
        for shipment in producer.storage:
            if shipment.state == ShipmentState.STORED:
                if EntityTypes.SHIPMENT not in \
                        producer.region.auctioneer.entities.keys() or \
                                shipment not in \
                                producer.region.auctioneer.entities[
                                    EntityTypes.SHIPMENT].values():
                    registrationkey = producer.region.auctioneer.register(
                        shipment)
                    bid = producer.bid(registrationkey, shipment)
                    producer.region.auctioneer.list_shipment(bid)

def container_bidding_proces(environment): # Normal auction
    if environment.config.debug is True:
        print(" \n Container bidding process")

    for container in environment.containers:
        if container.state == ContainerState.EMPTY:
            if EntityTypes.CONTAINER not in \
                    container.region.auctioneer.entities.keys() or \
                    container not in \
                    container.region.auctioneer.entities[
                                EntityTypes.CONTAINER].values():  # when container is empty he registers at the auction
                registrationkey = container.region.auctioneer.register(
                    container)  # registers at auction of region container is currently in
                container_bids = container.bidding_proces(registrationkey)
                for bid in container_bids:
                    container.region.auctioneer.list_container_bid(bid)

def container_auction_process(environment, matching_distances, day):
    # Continuous auction process for containers

    if environment.config.debug is True:
        print(" \n Container bidding process")

    for container in environment.containers:
        if container.state == ContainerState.EMPTY:
            if EntityTypes.CONTAINER not in \
                    container.region.auctioneer.entities.keys() or \
                    container not in \
                    container.region.auctioneer.entities[
                                EntityTypes.CONTAINER].values():  # when container is empty he registers at the auction
                registrationkey = container.region.auctioneer.register(
                    container)  # registers at auction of region container is currently in
                container_bids = container.bidding_proces(registrationkey)
                for bid in container_bids:
                    container.region.auctioneer.list_container_bid(bid)

                auctioning_continuous(environment,container,matching_distances,
                                      day)

                if container.state == ContainerState.EMPTY:
                    container.unregister_continuous_auction()

                if environment.config.debug:
                    print("\n registered items in region %s after matching"
                          % (container.region.id))
                    container.region.auctioneer.print_shipment_bid_info()
                    container.region.auctioneer.print_container_bid_info()

def auctioning(environment, matching_distances, day):
    if environment.config.debug is True:
        print(" \n Auctioneer matching process")

    for region in environment.regions:

        if environment.config.surplus_tool_debug is True and \
                        EntityTypes.CONTAINER in region.auctioneer.entities.keys() and \
                        EntityTypes.CONTAINER not in region.auctioneer.entities.keys():
            print("number of containers registered: %s \n"
                  "number of shipments registered: %s"
                  % (len(region.auctioneer.entities[EntityTypes.CONTAINER]),
                     len(region.auctioneer.entities[EntityTypes.SHIPMENT])))

        if environment.config.debug is True:
            print("\n registered items in region %s before matching"
                  % (region.id))
            region.auctioneer.print_shipment_bid_info()
            region.auctioneer.print_container_bid_info()

        matches = region.auctioneer.match_containers_shipments()
        calculate_matching_distance(matches, region.auctioneer,
                                    matching_distances, day)
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


def auctioning_continuous(environment, container, matching_distances, day):
    if environment.config.debug is True:
        print(" \n Auctioneer continuous matching process")

    if environment.config.debug is True:
        print("\n registered items in region %s before matching"
              % (container.region.id))
        container.region.auctioneer.print_shipment_bid_info()
        container.region.auctioneer.print_container_bid_info() # should be empty

    match = container.region.auctioneer.continuous_matching()

    calculate_matching_distance(match, container.region.auctioneer,
                                matching_distances, day)

    invoices = container.region.auctioneer.invoice_producers(match)
    for invoice in invoices:
        for producer in environment.producers:
            if invoice.producer_id == producer.id:
                payment = producer.pay_invoice(invoice)
                container.region.auctioneer.account_value += payment

    container.region.auctioneer.pay_container(match)

    container.region.auctioneer.finalize_matchmaking(match)

def container_auction_response(environment):
    for container in environment.containers:
        if container.state == ContainerState.EMPTY:
            container.losing_auction_response()

def assign_transport(environment):
    for container in environment.containers:
        if container.state == ContainerState.NEEDING_TRANSPORT:
            environment.transportcompany.assign_transporter(container)

def assign_relocation_transport(environment):
    for container in environment.containers:
        if container.state == ContainerState.RELOCATION_NEED:
            environment.transportcompany.assign_transporter(container)

def container_idle_management(environment):
    for container in environment.containers:
        container.losing_continuous_auction_response()
