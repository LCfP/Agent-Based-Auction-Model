from collections import namedtuple
from operator import attrgetter
from config import Config_continuous

# TODO run debug check

def best_match(container_bids, auctionable_shipments):
    # Check if matching is possible
    if len(container_bids) < 1 or len(auctionable_shipments) < 1:
        return None

    # find the shipments the container has bid on using shipment
    # registration key, calculate surplus for each matching bid check if surplus
    # is positive otherwise it is not an admissible match.
    # Select highest surplus match, ensure output is list.
    possible_matches = []
    match = namedtuple('match', ['container_registration_key',
                                 'shipment_registration_key',
                                 'surplus'])
    for container_bid in container_bids:
        for shipment_offer in auctionable_shipments:
            if container_bid.shipment_registration_key == \
                        shipment_offer.registration_key:
                if shipment_offer.biddingvalue - \
                        container_bid.biddingvalue >= 0:
                    new_match = match(container_registration_key=
                                  container_bid.container_registration_key,
                                  shipment_registration_key=
                                  shipment_offer.registration_key,
                                  surplus= shipment_offer.biddingvalue -
                                           container_bid.biddingvalue)
                    possible_matches.append(new_match)

    # Check if there are matches
    if len(possible_matches) > 0:
        winning_match = [] # list, because previous model uses a list as well
        winning_match.append(max(possible_matches, key=attrgetter('surplus')))

        return winning_match

    return None