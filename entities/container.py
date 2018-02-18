from .buyer import Buyer
from .shipment import Shipment
from enums import EntityTypes, ContainerState
from itertools import count
from tools import route_euclidean_distance, find_hub_coordinates
from collections import namedtuple



class Container(Buyer):
    _ids = count(0)

    def __init__(self, env, region):
        super().__init__(env)

        self.type = EntityTypes.CONTAINER

        self.region = region
        self.location = region.draw_location()
        self.id = next(self._ids)
        self.state = ContainerState.EMPTY
        self.account_value = self.env.config.container_starting_account_value
        self.shipment_contracts = [] # list because in the future, containers could bid on shipments, when they are loaded
        self.load = 0
        self.idle_days = 1 # checked at end of day, therefore initially 1 day idle

    def create_bids(self, best_shipments, registrationkey):
        containerbid = namedtuple('containerbid', 'container_registration_key shipment_registration_key biddingvalue')
        containerbids = []
        for entry in best_shipments:
            shipment_registration_key = entry[0]
            shipment = entry[2]
            transport_cost_empty = route_euclidean_distance(self.env, self.location, shipment.location)
            transport_cost_shipment = route_euclidean_distance(self.env, shipment.location, shipment.destination)
            biddingvalue = transport_cost_empty + transport_cost_shipment
            #TODO add additional profit margin for container or decrease of biddingvalue based on urgency
            container_bid = containerbid(container_registration_key = registrationkey,
                                        shipment_registration_key = shipment_registration_key,
                                        biddingvalue = biddingvalue)
            containerbids.append(container_bid)
        return containerbids

    def request_shipments(self):
        #TODO add functionality of selecting shipments from auctions outside current region
        if EntityTypes.SHIPMENT not in \
                self.region.auctioneer.entities.keys(): # There are currently no shipments available
            return
        return  self.region.auctioneer.entities[EntityTypes.SHIPMENT]# dict with shipment objects and their registration keys

    def select_best_shipments(self, available_shipments):
        ''' In the final model, the container should make transport reservations for each shipment it bids on,
        therefore the container places a limited number of bids. The container makes a selection based on the
        distance to the shipments. The closer a container is to a shipment, the lower it can bid.'''
        distance_to_shipments = []

        for key in available_shipments.keys():
            shipment = self.region.auctioneer.entities[EntityTypes.SHIPMENT][key]
            distance = route_euclidean_distance(self.env, self.location, shipment.location)
            registrationkey = key
            distance_to_shipments.append([registrationkey, distance, shipment])

        distance_to_shipments.sort(key = lambda item: item[1])
        best_shipments = distance_to_shipments[:self.env.config.number_of_bids]

        if self.env.config.debug is True and self.id < 1:
            print("\n", distance_to_shipments)
            print("from this list, the container should select the %s "
                  "closest shipments" %(self.env.config.number_of_bids))
            print(best_shipments, "\n")
        return best_shipments

    def bidding_proces(self,registrationkey):
        '''A container first requests the available shipments of the auction in the region the container
        is located. Next the container selects the shipments he wants to bid on. And finally the container
        constructs a set of bids'''
        available_shipments = self.request_shipments()
        if available_shipments is not None:
            best_shipments = self.select_best_shipments(available_shipments)
            container_bids = self.create_bids(best_shipments,registrationkey)

            if self.env.config.debug is True and self.region.id < 1:
                print("container %s in region %s enters the bids %s"
                      %(self.id, self.region.id, container_bids))

            return container_bids

        if self.env.config.debug is True and self.region.id < 1:
            print("there are no shipments available in region %s"
                  %(self.region.id))
        return []

    def losing_auction_response(self):
        if self.env.config.debug is True:
            print("Container %s is still empty and undertakes action"
                  %(self.id))

        # Case when container is somewhere in region
        if self.idle_days <= self.env.config.idle_max:

            if self.env.config.debug is True:
                print("Container %s is idle for %s day(s) and therefore "
                      "un-registers itself"%(self.id, self.idle_days))

            for key in \
                    self.region.auctioneer.entities[EntityTypes.CONTAINER]:
                if self.region.auctioneer.entities[EntityTypes.CONTAINER][
                    key].id \
                        == self.id:
                    registrationkey = key
            self.region.auctioneer.unregister(self.type, registrationkey)
            self.region.auctioneer.unlist_container_bid(registrationkey)
            self.idle_days += 1

        # Case when container is idle at a hub location
        elif self.location == find_hub_coordinates(self.region):

            if self.env.config.debug is True:
                print("Container %s is idle at hub and un-registers itself"
                      %(self.id))

            for key in \
                    self.region.auctioneer.entities[EntityTypes.CONTAINER]:
                if self.region.auctioneer.entities[EntityTypes.CONTAINER][
                    key].id \
                        == self.id:
                    registrationkey = key
            self.region.auctioneer.unregister(self.type, registrationkey)
            self.region.auctioneer.unlist_container_bid(registrationkey)

        # Relocation initiation
        else:
            if self.location != find_hub_coordinates(self.region):
                self.state = ContainerState.RELOCATION_NEED

                if self.env.config.debug is True:
                    print("Container %s is idle for %s days and therefore "
                          "initiates relocation to a hub"
                          %(self.id, self.idle_days))


    def unregister_continuous_auction(self):

        if self.env.config.debug is True:
            print("Container %s did not win and therefore un-registers himself"
                  %(self.id))

        for key in \
                self.region.auctioneer.entities[EntityTypes.CONTAINER]:
            if self.region.auctioneer.entities[EntityTypes.CONTAINER][
                key].id \
                    == self.id:
                registrationkey = key
        self.region.auctioneer.unregister(self.type, registrationkey)
        self.region.auctioneer.unlist_container_bid(registrationkey)