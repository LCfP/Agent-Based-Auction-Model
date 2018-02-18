from collections import namedtuple

def best_match(container_bids, auctionable_shipments):
    pass
    # find the shipments the container has bid on using shipment registration key
    # calculate surplus for each matching bid
    # select highest surplus match
    possible_matches = []
    match = namedtuple('match', ['container_registration_key',
                                'shipment_registration_key',
                                'surplus'])
    for container_bid in container_bids:
        for shipment_offer in auctionable_shipments:
            if container_bid.shipment_registration_key == \
                        shipment_offer.registration_key:
                new_match = match(container_registration_key=
                              container_bid.shipment_registration_key,
                              shipment_registration_key=
                              shipment_offer.registration_key,
                              surplus= shipment_offer.biddingvalue -
                                       container_bid.biddingvalue)
                possible_matches.append(new_match)

