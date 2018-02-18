from environment_continuous import Environment_continuous
from enums import EntityTypes, ShipmentState, ContainerState
from tools import calculate_matching_distance


def transportation(environment):
    for transporter in environment.transportcompany.transporters:
        transporter.move()
        transporter.status_update()

def production_registration(environment):
    if environment.config.debug is True:
        print(" \n Production and entering shipment bids")

    for producer in environment.producers:
        # all producers produce according to their production rate
        producer.produce() #TODO update produce for continuous
        # all shipments that are produced are registered at the auction
        for shipment in producer.storage:
            if shipment.state == ShipmentState.STORAGED:
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

def container_auction_process(environment): # Continuous auction
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
                # TODO ADD AUCTION RUN
                # TODO ADD un registration


def auctioning_continuous(environment, container ,matching_distances, day):
    if environment.config.debug is True:
        print(" \n Auctioneer continuous matching process")


    if environment.config.debug is True:
        print("\n registered items in region %s before matching"
              % (container.region.id))
        container.region.auctioneer.print_shipment_bid_info()
        container.region.auctioneer.print_container_bid_info() # should be empty

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