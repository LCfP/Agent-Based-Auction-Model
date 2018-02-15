from .entity import Entity
from enums import EntityTypes, TransporterState, ContainerState, ShipmentState
from itertools import count
from tools import route_euclidean_distance, find_region, find_hub_coordinates
from types import SimpleNamespace

class Transporter(Entity): #or name it truck?
    _ids = count(0)

    def __init__(self, env, region):
        self.env = env
        self.type = EntityTypes.TRANSPORTER
        self.region = region
        self.location = region.draw_location() # could be changed to location of hubs in the region
        self.id = next(self._ids)
        self.data = SimpleNamespace()
        # roep in de init de _data() functie aan om alle waardes toe te kennen.
        # Vervang alle onderstaande variabelen
        self.account_value = 0 #TODO add payment for transport by container
        self.state = TransporterState.EMPTY
        self.load = 0 # this attribute stores the container it is transporting

        self.speed = self.env.config.transport_speed
        self.transport_contract = [] # stores contracted object
        self.route_length = 0 # length of route to complete by transporter

        self.deliveries = 0 #TODO remove after debugging

    # functie aanmaken _data() --> alle variabelen hierin aanmaken en waardes geven
    def update_location(self):
        ''' Would be nice to update the location of the transporter
        during his transport (after unit time in run file)'''
        pass

    def move(self):
        if len(self.transport_contract) > 0: # if transporter has a purpose it moves
            self.route_length -= self.speed
        return


    def status_update(self):
        '''The transporter only updates information when he has reached a goal.
        The transporter can carry both a container (self.load) and a shipment
        (in the container = self.load.load).'''

        # transporter reached its goal
        if self.route_length <= 0 and len(self.transport_contract)> 0:

            # transporter reached empty container
            if self.state == TransporterState.PICKUP and \
                self.transport_contract[0].state == \
                            ContainerState.AWAITING_TRANSPORT:

                # update transporter info
                self.region = self.transport_contract[0].region
                self.location = self.transport_contract[0].location
                self.state = TransporterState.TRANSPORTING
                self.load = self.transport_contract[0]
                self.route_length = route_euclidean_distance(self.env,
                                       self.location,
                                       self.load.shipment_contracts[0].location)
                # update container info
                self.transport_contract[0].state = ContainerState.PICKUP

            # transporter reached container's shipment pick up location
            elif self.state == TransporterState.TRANSPORTING and \
                self.load.state == ContainerState.PICKUP:

                # update transporter info
                self.region = self.load.shipment_contracts[0].region # region of shipment
                self.location = self.load.shipment_contracts[0].location # shipment location of contracted shipment by container
                self.route_length = route_euclidean_distance(self.env,self.location,
                                        self.load.shipment_contracts[0].destination)
                # update container info
                self.load.region = self.region # container region is now same as transporter region
                self.load.location = self.location # container location is same as transporter location
                self.load.load = self.load.shipment_contracts[0]  # add shipment to container load
                self.load.state = ContainerState.DELIVERING
                # update shipment info
                self.load.load.state = ShipmentState.ON_ROUTE
                # update producer info
                self.env.producers[self.load.load.producer_id].storage.remove(self.load.load) # remove picked up shipment from producer's storage

            # transporter reach container's shipments destination
            elif self.state == TransporterState.TRANSPORTING and \
                self.load.state == ContainerState.DELIVERING:

                # update transporter info (1)
                self.region = find_region(self.env, self.load.load.destination)
                self.location = self.load.load.destination
                # update shipment info
                self.load.load.state = ShipmentState.DELIVERED
                # update consumer info
                self.env.consumer.products.append(self.load.load)
                # update container info
                self.load.region = self.region
                self.load.location = self.location
                self.load.shipment_contracts.remove(self.load.load) # remove shipment from contract
                self.load.load = 0 # remove shipment from container
                self.load.state = ContainerState.EMPTY
                # update transporter info (2)
                self.transport_contract.remove(self.load) # remove container from contract
                self.load = 0 # remove container from transporter
                self.state = TransporterState.EMPTY
                self.route_length = 0 # reset route_length
                self.deliveries += 1

            # Transporter reached empty container in need of relocating
            elif self.state == TransporterState.PICKUP and \
                self.transport_contract[0].state == \
                            ContainerState.AWAITING_RELOCATION:

                # update transporter info
                self.region = self.transport_contract[0].region
                self.location = self.transport_contract[0].location
                self.state = TransporterState.TRANSPORTING
                self.load = self.transport_contract[0]
                # To from container location to region hub
                self.route_length = route_euclidean_distance(self.env,
                                       self.location,
                                       find_hub_coordinates(self.region))
                # update container info
                self.transport_contract[0].state = ContainerState.RELOCATING

                if self.env.config.debug is True:
                    print("Container % is picked up and will be relocated"
                          % (self.load.id))

            # Transporter reached hub of relocating container
            elif self.state == TransporterState.TRANSPORTING and \
                self.load.state == ContainerState.RELOCATING:

                if self.env.config.debug is True:
                    print("Container % is dropped of at the hub of region %s "
                          %(self.load.id, self.region))

                # update transporter info (1)
                # region is still the same
                self.location = find_hub_coordinates(self.region)
                # update container info
                self.load.region = self.region
                self.load.location = self.location
                self.load.state = ContainerState.EMPTY
                # update transporter info (2)
                self.transport_contract.remove(self.load)
                self.load = 0
                self.state = TransporterState.EMPTY



