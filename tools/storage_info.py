
def gathering_storage_info(producer_storage_info: dict, environment):
    for producer in environment.producers:
        if producer.id not in producer_storage_info.keys():
            producer_storage_info[producer.id] = \
                [len(producer.storage) / environment.config.storage_capacity]
        else:
            producer_storage_info[producer.id].append(
                len(producer.storage) / environment.config.storage_capacity)

    return producer_storage_info