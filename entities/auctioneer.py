from .entity import Entity
from enums import EntityTypes, ContainerState, ShipmentState
from tools import surplus_maximisation, best_match
from collections import namedtuple
from tabulate import tabulate


class Auctioneer(Entity):

    def __init__(self, env, region):
        self.env = env
        self.region = region

        self.type = EntityTypes.AUCTIONEER

        self.entities = {}

        self.auctionable_shipments = []
        self.container_bids = []

        self.account_value = 1000

    def auction(self):
        """
        Auctions with the buyers and sellers provided to this Auctioneer.
        """
        raise NotImplementedError("TODO")

    def register(self, entity: Entity) -> int:
        """
        Registers an agent with this Auctioneer.
        """
        if entity.type not in self.entities.keys():
            self.entities[entity.type] = {}

        registration_key = self._registration(entity.type)
        self.entities[entity.type][registration_key] = entity

        if self.env.config.debug and self.region.id < 1:
            print("registration takes place in region: %s "
                  "returned registration key: %s"
                  %(self.region.id,registration_key))

        return registration_key

    def unregister(self, type, registration_key) -> Entity:
        """
        Unregisters an agent from this Auctioneer, using the assigned
        registration key.
        """
        if type not in self.entities.keys():
            raise ValueError("Type `{0}' is not an understood entity!"
                             .format(type))

        return self.entities[type].pop(registration_key, False)

    def _registration(self, type):
        max_key = max(self.entities[type].keys(), default=0)

        for key in range(max_key):  # attempt to fill `holes'
            if key not in self.entities[type].keys():
                return key

        return max_key + 1  # new key, one greater than the last

    def list_shipment(self, producer_bid):  # name is porely chosen, easy way to change name in whole file?
        self.auctionable_shipments.append(producer_bid)

    def unlist_shipment(self,shipment_registration_key):
        self.auctionable_shipments = [producer_bid for producer_bid in self.auctionable_shipments
                                         if producer_bid.registration_key != shipment_registration_key]

    def list_container_bid(self, container_bid):
        self.container_bids.append(container_bid)

    def unlist_container_bid(self, container_registration_key):
        self.container_bids = [container_bid for container_bid in self.container_bids
                                  if container_bid.container_registration_key != container_registration_key]

    def match_containers_shipments(self):
        matches = surplus_maximisation(self.container_bids,
                                       self.auctionable_shipments)

        if self.env.config.debug:
            print("The following matches have been made in region %s:"
                  %(self.region.id))
            print(tabulate(matches, headers=["container registration key",
                                             "shipment registration key",
                                             "surplus"]))
        return matches

    def invoice_producers(self, matches):
        ''' The auctioneer invoices the producer from the matched shipment.
            In the current situation, the auctioneer does not obtain part of the surplus.
        '''
        invoices = []
        invoice = namedtuple('invoice', 'producer_id shipment_id amount_due')
        if matches is not None: # required because if len = 0 the for loop will produce an error
            for match in matches:
                # obtain shipment that is matched, shipment cannot be yet removed, needed to assign to container later
                shipment = self.entities[EntityTypes.SHIPMENT][match.shipment_registration_key]
                # create invoice
                for producer_bid in self.auctionable_shipments:
                    if producer_bid.registration_key == match.shipment_registration_key:
                        new_invoice = invoice(producer_id= shipment.producer_id,
                                              shipment_id= shipment.id,
                                              amount_due= producer_bid.biddingvalue -
                                              self.env.config.producer_surplus_percentage * match.surplus)
                        invoices.append(new_invoice)

        if self.env.config.debug:
            print("The following invoices have been created:")
            print(tabulate(invoices, headers=["producer id","shipment id",
                                              "amount due"]))

        return invoices

    def pay_container(self,matches):
        # pay the container
        if matches is not None:
            for match in matches:
                container = self.entities[EntityTypes.CONTAINER][
                    match.container_registration_key]

                if self.env.config.debug:
                    account_value_before = self.account_value

                for container_bid in self.container_bids:
                    if container_bid.container_registration_key == \
                            match.container_registration_key and \
                            container_bid.shipment_registration_key == \
                            match.shipment_registration_key:
                        payment = container_bid.biddingvalue +\
                                  self.env.config.container_surplus_percentage \
                                  * match.surplus
                        container.account_value += payment
                        # remove payment amount from auctioneer account
                        self.account_value -= payment

                if self.env.config.debug:
                    print(tabulate([[self.region.id,account_value_before,
                                    payment, container.id, self.account_value]],
                          headers=["region id", "account value before payment",
                                   "payment amount", "container id",
                                   "account value after payment"]))

        return

    def finalize_matchmaking(self,matches):
        '''I made a seperate function to unregister both container and shipments, otherwise it messes up the
        for loops in the invoice and container payment functions. And it seems nice to have a payment check
        before the auctioneer finalizes its contact with the container and producer'''
        if matches is not None: #TODO omzetten zodat de for loop weer op de eerste indent zit
            for match in matches:
                shipment = self.unregister(EntityTypes.SHIPMENT, match.shipment_registration_key)
                shipment.state = ShipmentState.AWAITING_PICKUP
                #TODO wit regels toevoegen tussen verschillende blokken
                container = self.unregister(EntityTypes.CONTAINER,match.container_registration_key)
                container.state = ContainerState.NEEDING_TRANSPORT
                container.idle_days = 1 # reset to initial setting
                container.shipment_contracts.append(shipment)
                self.unlist_shipment(match.shipment_registration_key)
                self.unlist_container_bid(match.container_registration_key)

        return

    def print_shipment_bid_info(self):
        if EntityTypes.SHIPMENT not in self.entities.keys():
            return
        registered_shipments = []
        for key in self.entities[EntityTypes.SHIPMENT]:
            for bid in self.auctionable_shipments:
                if key == bid.registration_key:
                    bidding_value = bid.biddingvalue
            registered_shipments.append(
                [self.entities[EntityTypes.SHIPMENT][key].id, key, bidding_value])

        print(tabulate(registered_shipments,
                       headers=["shipment id",
                                "shipment registration key",
                                "bidding value"]))

    def print_container_bid_info(self):
        if EntityTypes.CONTAINER not in self.entities.keys():
            return
        registered_containers = []
        for bid in self.container_bids:
            for key in self.entities[EntityTypes.CONTAINER]:
                if key == bid.container_registration_key:
                    container_id = self.entities[EntityTypes.CONTAINER][key].id
            container_registration_key= bid.container_registration_key
            biddingvalue = bid.biddingvalue
            shipment_registration_key = bid.shipment_registration_key
            registered_containers.append([container_id,
                                          container_registration_key,
                                          biddingvalue,
                                          shipment_registration_key])

        print(tabulate(registered_containers,
                       headers=["container id",
                                "container registration key",
                                "bidding value",
                                "shipment registration key"]))

    # Function below is written for continuous environment
    def continuous_matching(self):
        # Continuous action runs for each container, therefore resulting in one
        # match at a time
        match = best_match(self.container_bids, self.auctionable_shipments)

        if self.env.config.debug:
            print("The following matches have been made in region %s:"
                  %(self.region.id))
            print(tabulate(match, headers=["container registration key",
                                             "shipment registration key",
                                             "surplus"]))

        return match
