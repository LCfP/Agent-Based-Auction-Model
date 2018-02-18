# store container state info in dict
def gathering_containerinfo(containerinfo: dict, environment,):
    for container in environment.containers:
        if container.id not in containerinfo.keys():
            containerinfo[container.id] = [container.state]
        else:
            containerinfo[container.id].append(container.state)

    return containerinfo