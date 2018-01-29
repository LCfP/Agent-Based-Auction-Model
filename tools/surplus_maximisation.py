from __future__ import print_function
from ortools.linear_solver import pywraplp
from collections import Counter, namedtuple
from operator import attrgetter

def surplus_maximisation(container_bids,auctionable_shipments):
    check = check_matching_possibility(container_bids,auctionable_shipments)
    if check == 1:
        surplus_array = create_surplus_array(container_bids,auctionable_shipments)
        matches = maximisation_solver(surplus_array, container_bids, auctionable_shipments)
        if len(matches) > 0:
            return matches
    return

def maximisation_solver(surplus_array, container_bids, auctionable_shipments):
    solver = pywraplp.Solver('SolveAssignmentProblemMIP',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # Setup data for solver
    surplus = surplus_array
    num_containers = len(surplus)
    num_shipments = len(surplus[0])
    x = {}

    for i in range(num_containers):
        for j in range(num_shipments):
            x[i, j] = solver.BoolVar('x[%i,%i]' % (i, j))

    # Objective
    solver.Maximize(solver.Sum([surplus[i][j] * x[i, j] for i in range(num_containers)
                                for j in range(num_shipments)]))

    # Constraints
    # Each container is matched with atmost 1 shipment
    for i in range(num_containers):
        solver.Add(solver.Sum([x[i, j] for j in range(num_shipments)]) <= 1)
    # Each shipment is matched with atmost 1 container.
    for j in range(num_shipments):
        solver.Add(solver.Sum([x[i, j] for i in range(num_containers)]) <= 1)

    # Run solver
    sol = solver.Solve() # Necessary to keep in model, although variable sol is not used explicitly!

    matches = []
    match = namedtuple('match','container_registration_key shipment_registration_key surplus')
    grouped_container_bids = group_container_bids(container_bids)

    # with >0 auctioneer does not allow a surplus of zero, should be discussed
    # setting value comparison to >= 0 gives negative surplus matches... no idea why
    for i in range(num_containers):
        for j in range(num_shipments):
            if x[i, j].solution_value() > 0: #filters matches that were added manually to fill matrix
                container_key = grouped_container_bids[i][0].container_registration_key
                shipment_key = auctionable_shipments[j].registration_key
                new_match = match(container_registration_key= container_key,
                              shipment_registration_key= shipment_key,
                              surplus = surplus[i][j])
                matches.append(new_match)
                '''print('Container %d with key %d, is assigned to shipment %d with key %d.  surplus = %d' % (
                    i, container_key,
                    j, shipment_key,
                    surplus[i][j]))''' # remove when there are certainly no bugs anymore

    return matches


def check_matching_possibility(container_bids, auctionable_shipments):
    if len(container_bids) > 0 and len(auctionable_shipments) > 0:
        return 1 # TODO create enum for yes or no matching possibility ?
    else:
        return 0


def group_container_bids(container_bids):
    container_keys = Counter(containerbid.container_registration_key for containerbid in container_bids).keys()
    grouped_container_bids = []
    for key in container_keys:
        grouped_bids = [container for container in container_bids if container.container_registration_key == key]
        grouped_container_bids.append(grouped_bids)
    return grouped_container_bids


def create_surplus_array(container_bids, auctionable_shipments):
    grouped_container_bids = group_container_bids(container_bids)

    surplus_list = []
    for container in grouped_container_bids:
        for shipment in auctionable_shipments:
            if shipment.registration_key not in map(attrgetter('shipment_registration_key'), container):
                surplus = -1 # required to fill array, solver will filter for matches with surplus < 0
                surplus_list.append(surplus)
            else:
                for container_bid in container:
                    if container_bid.shipment_registration_key == shipment.registration_key:
                        surplus = shipment.biddingvalue - container_bid.biddingvalue
                        surplus_list.append(surplus)

    surplus_array = [surplus_list[i:i + (len(auctionable_shipments))]
                     for i in range(0, len(surplus_list), len(auctionable_shipments))]

    return (surplus_array)
