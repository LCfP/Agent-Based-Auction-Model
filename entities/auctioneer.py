from .entity import Entity
from enums import EntityTypes, ContainerState, ShipmentState
from tools import surplus_maximisation
from collections import namedtuple

class Auctioneer(Entity):

    def __init__(self, env, region):
        self.env = env
        self.region = region

        self.type = EntityTypes.AUCTIONEER

        self.entities = {}

        self.auctionable_shipments = []
        self.container_bids = []

        self.account_value = 0


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

            #self.entities[EntityTypes.SHIPMENT] (.values returns all values from dict)

        registration_key = self._registration(entity.type)
        self.entities[entity.type][registration_key] = entity

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

    def list_shipment(self, producer_bid): # name is porely chosen, easy way to change name in whole file?
        self.auctionable_shipments.append(producer_bid)

    def unlist_shipment(self,shipment_registration_key):
        for producer_bid in self.auctionable_shipments:
            if producer_bid.registration_key == shipment_registration_key:
                self.auctionable_shipments.remove(producer_bid)

    def list_container_bid(self, container_bid):
        self.container_bids.append(container_bid)

    def unlist_container_bid(self, container_registration_key):
        for container_bid in self.container_bids:
            if container_bid.container_registration_key == container_registration_key:
                self.container_bids.remove(container_bid)

    def match_containers_shipments(self):
        matches = surplus_maximisation(self.container_bids,self.auctionable_shipments)
        return matches

    def invoice_producers(self, matches):
        '''The auctioneer invoices the producer from the matched shipment.
            In the current situation, the auctioneer does not obtain part of the surplus.
            Unlisting bids from auctionable_shipments happens later, creates error in for loop'''
        invoices = []
        invoice = namedtuple('invoice', 'producer_id amount_due')
        if matches is not None: # required because if len = 0 the for loop will produce an error
            for match in matches:
                # obtain shipment that is matched, shipment cannot be yet removed, needed to assign to container later
                shipment = self.entities[EntityTypes.SHIPMENT][match.shipment_registration_key]
                # create invoice
                for producer_bid in self.auctionable_shipments:
                    if producer_bid.registration_key == match.shipment_registration_key:
                        new_invoice = invoice(producer_id= shipment.producer_id,
                                                amount_due= producer_bid.biddingvalue -
                                                  self.env.config.producer_surplus_percentage * match.surplus)
                        invoices.append(new_invoice)
        return invoices

    def pay_container(self,matches):
        # pay the container
        if matches is not None:  # required because if len = 0 the for loop will produce an error
            for match in matches:
                container = self.entities[EntityTypes.CONTAINER][match.container_registration_key]
                for container_bid in self.container_bids:
                    if container_bid.container_registration_key == match.container_registration_key:
                        payment = container_bid.biddingvalue \
                                  + self.env.config.container_surplus_percentage * match.surplus
                        container.account_value += payment
                        # remove payment amount from auctioneer account
                        self.account_value -= payment

        return

    #TODO make functions that unregister container and shipments after payment, and unlist items
    #TODO change container state when container wins shipment

    def finalize_matchmaking(self,matches):
        '''I made a seperate function to unregister both container and shipments, otherwise it messes up the
        for loops in the invoice and container payment functions. And it seems nice to have a payment check
        before the auctioneer finalizes its contact with the container and producer'''
        if matches is not None:
            for match in matches:
                shipment = self.unregister(EntityTypes.SHIPMENT, match.shipment_registration_key)
                shipment.state = ShipmentState.AWAITING_PICKUP
                container = self.unregister(EntityTypes.CONTAINER,match.container_registration_key)
                container.state = ContainerState.PICKUP
                container.shipment_contracts.append(shipment)
                self.unlist_shipment(match.shipment_registration_key)
                self.unlist_container_bid(match.container_registration_key)

        return

