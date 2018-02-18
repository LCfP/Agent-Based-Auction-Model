from collections import namedtuple


possible_matches = []
match = namedtuple('match', ['container_registration_key',
                             'shipment_registration_key',
                             'surplus'])

for number in range(5):
    new_match = match(container_registration_key=number,
                  shipment_registration_key= number,
                  surplus= number)
    possible_matches.append(new_match)

