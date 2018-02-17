from .entity import Entity
from enums import EntityTypes, TransporterState, ContainerState, ShipmentState
from itertools import count
from tools import route_euclidean_distance, find_region, find_hub_coordinates
from types import SimpleNamespace


class Transporter(Entity):  # or name it truck?
    _ids = count(0)

    def __init__(self, env, region):
        self.env = env
        self.type = EntityTypes.TRANSPORTER
        self.region = region
        self.location = region.draw_location()  # could be changed to location of hubs in the region
        self.id = next(self._ids)
        self.data = SimpleNamespace()
        # roep in de init de _data() functie aan om alle waardes toe te kennen.
        # Vervang alle onderstaande variabelen
        self.account_value = 0  # TODO add payment for transport by container
        self.state = TransporterState.EMPTY
        self.load = 0  # this attribute stores the container it is transporting

        self.speed = self.env.config.transport_speed
        self.transport_contract = []  # stores contracted object
        self.route_length = 0  # length of route to complete by transporter

        self.deliveries = 0  # TODO remove after debugging

    def move(self):
        if len(
                self.transport_contract) > 0:  # if transporter has a purpose it moves
            self.route_length -= self.speed
        return

    def status_update(self):
        '''The transporter only updates information when he has reached a goal.
        The transporter can carry both a container (self.load) and a shipment
        (in the container = self.load.load).'''

        # When a transporter has no transport contract he does not move
        if len(self.transport_contract) == 0:
            return

        # Update info when transporter reached empty container
        if self.route_length <= 0 and \
                        self.state == TransporterState.PICKUP and \
                        self.transport_contract[0].state == \
                        ContainerState.AWAITING_TRANSPORT:
            self.reached_empty_container()

        # Update info when transporter reached shipment pickup location
        if self.route_length <= 0 and self.load != 0:
            if self.state == TransporterState.TRANSPORTING and \
                            self.load.state == ContainerState.PICKUP:
                self.reached_shipment_pickup()

        # Update info when transporter reached shipment destination
        if self.route_length <= 0 and self.load != 0:
            if self.state == TransporterState.TRANSPORTING and \
                            self.load.state == ContainerState.DELIVERING:
                self.reached_shipment_destination()

        # Update info when transporter reached container in need of relocation
        if self.route_length <= 0 and \
                        self.state == TransporterState.PICKUP and \
                        self.transport_contract[0].state == \
                        ContainerState.AWAITING_RELOCATION:
            self.reached_relocating_container()

        # Update info when transporter reach hub of relocating container
        if self.route_length <= 0 and self.load != 0:
            if self.state == TransporterState.TRANSPORTING and \
                            self.load.state == ContainerState.RELOCATING:
                self.reached_hub()

    def reached_empty_container(self):
        # UPDATE TRANSPORTER INFO
        # location and state info
        self.region = self.transport_contract[0].region
        self.location = self.transport_contract[0].location
        self.state = TransporterState.TRANSPORTING
        # assign container to load
        self.load = self.transport_contract[0]
        # new route is from container pick up location to shipment
        # pick up location
        self.route_length += route_euclidean_distance(
            self.env, self.location, self.load.shipment_contracts[0].location)

        # UPDATE CONTAINER INFO
        self.transport_contract[0].state = ContainerState.PICKUP

        if self.env.config.debug is True:
            print("Transporter %s reached container %s and "
                  "has an updated route length of: %s"
                  % (self.id, self.transport_contract[0].id,
                     self.route_length))

    def reached_shipment_pickup(self):
        # UPDATE TRANSPORTER INFO
        # location and state info with shipment info from container contract
        self.region = self.load.shipment_contracts[0].region
        self.location = self.load.shipment_contracts[0].location
        self.route_length += route_euclidean_distance(
            self.env, self.location,
            self.load.shipment_contracts[0].destination)

        # UPDATE CONTAINER INFO (= self.load)
        # location and state info update with updated transporter info (above)
        self.load.region = self.region
        self.load.location = self.location
        self.load.state = ContainerState.DELIVERING
        # add shipment to container load
        self.load.load = self.load.shipment_contracts[0]

        # UPDATE SHIPMENT INFO (= container.load, therefore self.load.load)
        self.load.load.state = ShipmentState.ON_ROUTE

        # UPDATE PRODUCER INFO
        # remove picked up shipment from producer's storage
        self.env.producers[self.load.load.producer_id].storage = \
            [shipment for shipment in
             self.env.producers[self.load.load.producer_id].storage
             if shipment.id != self.load.load.id]

        if self.env.config.debug is True:
            print("Transporter %s reached shipment %s pickup location"
                  "and has an updated route length of: %s"
                  % (self.id, self.load.shipment_contracts[0].id,
                     self.route_length))

    def reached_shipment_destination(self):
        # UPDATE TRANSPORTER INFO(1)
        # update location with shipment destination info
        self.region = find_region(self.env, self.load.load.destination)
        self.location = self.load.load.destination

        # UPDATE CONTAINER INFO
        # update location and state with updated transporter location info
        self.load.region = self.region
        self.load.location = self.location
        self.load.state = ContainerState.EMPTY
        # remove shipment contract and corresponding shipment
        self.load.shipment_contracts.remove(self.load.load)
        self.load.load = 0

        # UPDATE TRANSPORTER INFO(2)
        # remove container contract and container
        self.transport_contract.remove(self.load)
        self.load = 0
        # update state and reset route length
        self.state = TransporterState.EMPTY
        self.route_length = 0

        if self.env.config.debug is True:
            print("Transporter %s reached shipment destination and "
                  "has an updated route length of: %s"
                  % (self.id, self.route_length))

    def reached_relocating_container(self):
        # UPDATE TRANSPORTER INFO
        # update location and state info from transport contract
        self.region = self.transport_contract[0].region
        self.location = self.transport_contract[0].location
        self.state = TransporterState.TRANSPORTING
        # Add container to load from contract
        self.load = self.transport_contract[0]
        #  new route is from container location to region hub
        self.route_length += route_euclidean_distance(
            self.env, self.location, find_hub_coordinates(self.region))

        # UPDATE CONTAINER INFO
        self.transport_contract[0].state = ContainerState.RELOCATING

        if self.env.config.debug is True:
            print("Container % is picked up and will be relocated"
                  % (self.load.id))

    def reached_hub(self):

        if self.env.config.debug is True:
            print("Container % is dropped of at the hub of region %s "
                  % (self.load.id, self.region.id))

        # UPDATE TRANSPORTER INFO (1)
        # region is still the same, location is updated with hub coordinates
        self.location = find_hub_coordinates(self.region)

        # UPDATE CONTAINER INFO
        # update location and status info
        self.load.region = self.region
        self.load.location = self.location
        self.load.state = ContainerState.EMPTY

        # UPDATE TRANSPORTER INFO (2)
        # remove container contract and container
        self.transport_contract.remove(self.load)
        self.load = 0
        # update state and reset route length
        self.state = TransporterState.EMPTY
        self.route_length = 0





