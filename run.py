from environment import Environment
from env_activities import *
from tools import gathering_data, remove_warmup_period, write_to_dataframe
from analysis import calculate_averages
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures import wait


def run_sim(exp_no):
    environment = Environment()
    environment.setup()

    # KPI data storage
    containerinfo = {}
    shipmentinfo = {}
    transporterinfo = {}
    producer_storage_info = {}
    matching_distances = []

    for day in range(environment.config.run_length):  # run model!
        environment.day = day

        # Perform daily actions and save KPI matching distance info
        daily_actions(environment, matching_distances, day)

        # save KPI results per simulation day
        gathering_data(environment, day, containerinfo, shipmentinfo,
                       transporterinfo, producer_storage_info)

    # rewrite gathered data into dataframe
    data = write_to_dataframe(environment,containerinfo,shipmentinfo,
                              transporterinfo, producer_storage_info)

    # remove data during warmup period
    data = remove_warmup_period(environment, data)

    request_shipments_avg = sum(
        container._lookup["request_shipments"]
        for container in environment.containers
    ) / len(environment.containers)

    print(request_shipments_avg)

    for container in environment.containers:
        print(container._lookup)

    # Calculate KPI scores
    calculate_averages(data, matching_distances, exp_no)


def job(space):
    for exp_no in range(*space):
        print("Job: {0}".format(exp_no))
        run_sim(exp_no)


if __name__ == "__main__":
    '''Determine total number of experiments and specify the number of threads
    to use'''

    run_sim(0)


    # no_threads = 1
    # jobs_per_thread = 1
    #
    # executor = ProcessPoolExecutor(no_threads)
    # items = [[start, start + jobs_per_thread] for start in range(
    #     0, jobs_per_thread * no_threads, jobs_per_thread)]
    #
    # futures = [executor.submit(job, item) for item in items]
    # wait(futures)
