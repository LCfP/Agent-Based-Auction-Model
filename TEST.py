from collections import namedtuple
from operator import attrgetter


possible_matches = []
match = namedtuple('match', ['container_registration_key',
                             'shipment_registration_key',
                             'surplus'])

for number in range(5):
    new_match = match(container_registration_key=number,
                  shipment_registration_key= number,
                  surplus= number)
    possible_matches.append(new_match)

winning_match = []
winning_match.append(max(possible_matches, key=attrgetter('surplus')))

print(winning_match)

import numpy as np
from numpy.random import randint

sample_1 = randint(1, 5, (1, 100))
sample_2 = randint(1, 4, (1, 100))

stds = np.asarray((sample_1.std(), sample_2.std()))

print(stds.std())  # of statistic
print(np.concatenate((sample_1, sample_1)).std())  # of sample
