from .entity import Entity
from .transporter import Transporter
from enums import TransporterState, ContainerState
from tools import route_euclidean_distance
from random import choice

class Transportcompany(Entity):

    def __init__(self, env):
        super().__init__()

        self.env = env
        self.transporters = [Transporter(self.env, choice(self.env.regions))
                             for _ in
                             range(self.env.config.number_of_transporters)]

    def find_closest_transporter(self, container):
        available_transporters = [transporter for transporter in
                                  self.transporters if transporter.state ==
                                  TransporterState.EMPTY]

        if len(available_transporters) > 0:
            closest_distance_to_pickup = \
                [route_euclidean_distance(self.env, container.location,
                                            available_transporters[0].location),
                 available_transporters[0]]
            for transporter in available_transporters:
                distance_to_pickup = \
                    route_euclidean_distance(self.env,
                                             container.location,
                                             transporter.location)
                if distance_to_pickup < closest_distance_to_pickup[0]:
                    closest_distance_to_pickup = \
                        [distance_to_pickup,transporter]
            return closest_distance_to_pickup[1]
        return


    def assign_transporter(self, container):
        closest_transporter = self.find_closest_transporter(container)
        if closest_transporter is not None:
            for transporter in self.transporters:
                if transporter == closest_transporter:
                    transporter.state = TransporterState.PICKUP
                    transporter.transport_contract.append(container)
                    transporter.route_length = \
                        route_euclidean_distance(self.env,container.location,
                                                 transporter.location)

                    if container.state == ContainerState.NEEDING_TRANSPORT:
                        container.state = ContainerState.AWAITING_TRANSPORT

                    elif container.state == ContainerState.RELOCATION_NEED:
                        container.state = ContainerState.AWAITING_RELOCATION

                        if self.env.config.debug is True:
                            print("Transporter %s is assigned to pickup "
                                  "container %s that is in need of relocation"
                                  %(transporter.id, container.id))
        return
