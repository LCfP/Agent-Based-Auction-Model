from tools import route_euclidean_distance
from enums import EntityTypes
from config import Config

def calculate_matching_distance(matches, auctioneer, matching_distances: list,
                                day):
    if matches is None:
        return

    if day < Config.warmup_period:
        return

    for match in matches:
        # first determine container location
        for key in auctioneer.entities[EntityTypes.CONTAINER]:
            if match.container_registration_key == key:
                container_location = \
                    auctioneer.entities[EntityTypes.CONTAINER][key].location
        # determine shipment location
        for key in auctioneer.entities[EntityTypes.SHIPMENT]:
            if match.shipment_registration_key == key:
                shipment_location = \
                    auctioneer.entities[EntityTypes.SHIPMENT][key].location
        match_distance = route_euclidean_distance(auctioneer.env,
                                                  container_location,
                                                  shipment_location)
        matching_distances.append(match_distance)
    return matching_distances

