from .buyer import Buyer
from .seller import Seller
from .agent import Agent
from operator import attrgetter
from statistics import median

"""
Couple remarks:
- I haven't worked with GitHub before, so I hope I didn't mess things up;
- Nor with code from multiple files (what I did before was just using one file with the 
  entire code). Therefore, I did nothing with the other files yet;
- I know the basics of Classes, and practiced with them, but I have no experience in 
  using Classes in my own projects.
- Don't really know yet how I can best test my code if it requires information from other
  sources (that are not ready yet). So I just made a seperate file using test data. That
  worked fine, but I figure that's not the optimal way, right?
If I'm using things the wrong way, please let me know.

--> Sandholm, T. (2002). eMediator: A next generation electronic commerce server.
        Computational Intelligence, 18(4), 656-676.

Based on the Sandholm (2002) article, Middle Price 50:50 is best suited for determining
the prices in double auctions. This also happens to be a simple way of determining the
aution winners.

To keep it simple (for now), I followed these steps:
(1) Calculate Qs
(2) Calculate median Ps
(3) Calculate Qb
(2) Deleted the lowest bids from the buyers, so Qs = Qb
(3) Calculate median Pb
(4) Calculate auction price (average of Ps and Pb)
(5) Distribute the items to the highest bidders

I tested the function with this data:
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
    
    Results:
        There are 600 items for sale.
        Total demand is 1000
        Median seller price: 0.84
        Median buyer price: 0.6
        Final auction price: 0.72
        Buyer 0 gets 150 units.
        Buyer 1 gets 250 units.
        Buyer 2 gets 200 units.
        Buyer 3 gets nothing.
"""


class Auctioneer(object):

    def __init__(self):
        self.buyers = []
        self.sellers = []

    def auction(self):
        """
        Auctions with the buyers and sellers provided to this Auctioneer.
        """

        # Get Qs and Median Ps:
        total_q_s = 0
        auction_items = []

        for seller in self.sellers:
            total_q_s += seller[1]
            for i in range(seller[1]):
                auction_items.append(seller[2])

        median_p_s = median(sorted(auction_items))

        # Get Qb and Median Pb:
        total_q_b = 0
        auction_items_b = []

        for buyer in self.buyers:
            total_q_b += buyer[1]
            for j in range(buyer[1]):
                auction_items_b.append(buyer[2])

        auction_items_b = sorted(auction_items_b, reverse=True)
        median_p_b = median(auction_items_b[0:total_q_s])

        # Determine auction price:
        price = (median_p_s + median_p_b) / 2

        print("There are %s items for sale." % total_q_s)
        print("Total demand is %s" % total_q_b)
        print("Median seller price: %s" % median_p_s)
        print("Median buyer price: %s" % median_p_b)
        print("Final auction price: %s" % price)

        # (5) Distribution of the auction items:
        buyers = sorted(self.buyers, key=attrgetter('item_price'), reverse=True)

        for buyer in buyers:
            buyer_quantity = buyer[1]

            buyer_code = buyers.index(buyer)
            if total_q_s >= buyer_quantity:
                print("Buyer %s gets %s units." % (buyer_code, buyer_quantity))
                total_q_s -= buyer_quantity
            elif total_q_s > 0:
                print("Buyer %s gets %s units." % (buyer_code, total_q_s))
                total_q_s = 0
            else:
                print("Buyer %s gets nothing." % buyer_code)

    def register(self, agent: Agent) -> int:
        pass  # TODO

    def unregister(self, identifier: int) -> Agent:
        pass  # TODO
