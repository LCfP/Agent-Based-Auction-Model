from environment import Environment
from enums import EntityTypes, ContainerState, ShipmentState
import pandas as pd
from tools import gathering_shipmentinfo, calculate_matching_distance
from analysis import states_analysis

from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures import wait
import os


def run_sim(exp_no):
    environment = Environment()
    environment.setup()

    #KPI data storage
    containerinfo = {}
    shipmentinfo = {}
    matching_distances = []

    for day in range(environment.config.run_length):  # run model!

        if environment.config.debug is True:
            print(" \n \033[1m start of day %s" %(day))
            print('\033[0m')

        # Transportation "during" the day
        for transporter in environment.transportcompany.transporters:
            transporter.move()
            transporter.status_update()

        if environment.config.debug is True:
            print(" \n Production and entering shipment bids")

        for producer in environment.producers:
            # all producers produce according to their production rate
            producer.produce()
            # all shipments that are produced are registered at the auction
            for shipment in producer.storage:
                if shipment.state == ShipmentState.STORAGED:
                    if EntityTypes.SHIPMENT not in \
                            producer.region.auctioneer.entities.keys() or \
                       shipment not in \
                            producer.region.auctioneer.entities[EntityTypes.SHIPMENT].values():
                        registrationkey = producer.region.auctioneer.register(shipment)
                        bid = producer.bid(registrationkey,shipment)
                        producer.region.auctioneer.list_shipment(bid)

        if environment.config.debug is True:
            print(" \n Container bidding process")

        for container in environment.containers:
            if container.state == ContainerState.EMPTY:
                if EntityTypes.CONTAINER not in container.region.auctioneer.entities.keys() or \
                container not in container.region.auctioneer.entities[EntityTypes.CONTAINER].values(): #when container is empty he registers at the auction
                    registrationkey = container.region.auctioneer.register(container) # registers at auction of region container is currently in
                    container_bids = container.bidding_proces(registrationkey)
                    for bid in container_bids:
                        container.region.auctioneer.list_container_bid(bid)

        if environment.config.debug is True:
            print(" \n Auctioneer matching process")

        for region in environment.regions:

            if environment.config.surplus_tool_debug is True and \
               EntityTypes.CONTAINER in region.auctioneer.entities.keys() and \
               EntityTypes.CONTAINER not in region.auctioneer.entities.keys():
                print("number of containers registered: %s \n"
                      "number of shipments registered: %s"
                      %(len(region.auctioneer.entities[EntityTypes.CONTAINER]),
                        len(region.auctioneer.entities[EntityTypes.SHIPMENT])))

            if environment.config.debug is True:
                print("\n registered items in region %s before matching"
                      %(region.id))
                region.auctioneer.print_shipment_bid_info()
                region.auctioneer.print_container_bid_info()

            matches = region.auctioneer.match_containers_shipments()
            calculate_matching_distance(matches, region.auctioneer,
                                        matching_distances)
            invoices = region.auctioneer.invoice_producers(matches)
            for invoice in invoices:
                for producer in environment.producers:
                    if invoice.producer_id == producer.id:
                        payment = producer.pay_invoice(invoice)
                        region.auctioneer.account_value += payment
            region.auctioneer.pay_container(matches)
            region.auctioneer.finalize_matchmaking(matches)

            if environment.config.debug is True:
                print("\n registered items in region %s after matching"
                      % (region.id))
                region.auctioneer.print_shipment_bid_info()
                region.auctioneer.print_container_bid_info()

        for container in environment.containers:
            if container.state == ContainerState.NEEDING_TRANSPORT:
                environment.transportcompany.assign_transporter(container)

        if environment.config.debug is True:
            for container in environment.containers:
                if container.load != 0:
                    print("container %s has state %s and "
                          "delivers shipment %s with state%s"
                          % (container.id, container.state, container.load.id,
                             container.load.state))
                    for producer in environment.producers:
                        for shipment in producer.storage:
                            if container.load.id == shipment.id:
                                print("ERROR")

        # Containers unregister at end of day to consider new shipment bids next day
        for container in environment.containers:
            if container.state == ContainerState.EMPTY:
                container.losing_auction_response()
            # when container is not matched after x number of days, he relocates
            if container.state == ContainerState.RELOCATION_NEED:
                environment.transportcompany.assign_transporter(container)

        # END OF DAILY SIMULATION ACTIONS

        # store container state info in dict
        for container in environment.containers:
            if container.id not in containerinfo.keys():
                containerinfo[container.id] = [container.state]
            else:
                containerinfo[container.id].append(container.state)

        # store shipment state info in dict
        shipmentinfo = gathering_shipmentinfo(shipmentinfo,environment,day)


    # Create dataframe for containerinfo
    containerinfo_df = pd.DataFrame(containerinfo)

    # Rewrite shipment info dict
    for key in shipmentinfo:
        shipmentinfo[key] = pd.Series(shipmentinfo[key][0],
                                      index=shipmentinfo[key][1])
    # Create dataframe for shipmentinfo
    shipmentinfo_df = pd.DataFrame(shipmentinfo)

    # matching distance
    print("number of matches:")
    print(len(matching_distances))
    print("average match distance:")
    print(sum(matching_distances)/len(matching_distances))


    states_analysis(containerinfo_df, ContainerState)
    states_analysis(shipmentinfo_df, ShipmentState)

    # save this experiment
    os.makedirs("./experiments/{0}".format(exp_no))

    containerinfo_df.to_csv("./experiments/{0}/container_info.csv"
                            .format(exp_no))



def job(space):
    for exp_no in range(*space):
        print("Job: {0}".format(exp_no))
        run_sim(exp_no)


if __name__ == "__main__":
    # run_sim(1)
    no_threads = 3
    jobs_per_thread = 25

    executor = ProcessPoolExecutor(no_threads)
    items = [[start, start + jobs_per_thread] for start in range(
        0, jobs_per_thread * no_threads, jobs_per_thread)]

    futures = [executor.submit(job, item) for item in items]
    wait(futures)
