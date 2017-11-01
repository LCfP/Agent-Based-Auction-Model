from typing import List
from operator import attrgetter

# Temporary
from collections import namedtuple
from statistics import median

Bid = namedtuple('Bid', ['action', 'quantity', 'item_price'])

buyers = [Bid("buy", 200, 0.45),
          Bid("buy", 250, 0.60),
          Bid("buy", 400, 0.57),
          Bid("buy", 150, 0.64)]

sellers = [Bid("sell", 100, 0.80),
           Bid("sell", 80, 0.90),
           Bid("sell", 120, 0.79),
           Bid("sell", 100, 0.88),
           Bid("sell", 90, 0.84),
           Bid("sell", 50, 0.99),
           Bid("sell", 60, 0.92)]

"""
PROBLEM: I sorted the buyers and sellers to I can distribute the items to the buyers that are willing
to pay the highest price. However, this gives problems with returning the index (buyer-code) of the buyer. 
I thought I'd wait resolving this till I know the exact input.
"""

#buyers = sorted(buyers, key=attrgetter('item_price'), reverse=True)
#sellers = sorted(sellers, key=attrgetter('item_price'))

# Get Qs and Median Ps:
total_q_s = 0
auction_items = []

for m in sellers:
    total_q_s += m[1]
    for i in range(m[1]):
        auction_items.append(m[2])

median_p_s = median(sorted(auction_items))

# Get Qb and Median Pb:
total_q_b = 0
auction_items_b = []

for n in buyers:
    total_q_b += n[1]
    for j in range(n[1]):
        auction_items_b.append(n[2])

auction_items_b = sorted(auction_items_b, reverse=True)
median_p_b = median(auction_items_b[0:total_q_s])

# Determine final selling price:
price = (median_p_s + median_p_b) / 2

print("There are %s items for sale." % total_q_s)
print("Total demand is %s" % total_q_b)
print("Median seller price: %s" % median_p_s)
print("Median buyer price: %s" % median_p_b)
print("Final auction price: %s" % price)

# Distribution of the auction items:
buyers_dict = {}
buyer_code = 0
for b in buyers:
    buyer_code += 1
    buyers_dict[buyer_code] =

buyers = sorted(buyers, key=attrgetter('item_price'), reverse=True)

for n in buyers:
    buyer_quantity = n[1]

    buyer_code = buyers.index(n)
    if total_q_s >= buyer_quantity:
        print("Buyer %s gets %s units." % (buyer_code, buyer_quantity))
        total_q_s -= buyer_quantity
    elif total_q_s > 0:
        print("Buyer %s gets %s units." % (buyer_code, total_q_s))
        total_q_s = 0
    else:
        print("Buyer %s gets nothing." % buyer_code)