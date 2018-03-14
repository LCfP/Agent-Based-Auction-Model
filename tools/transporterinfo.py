
def gathering_transporterinfo(transporterinfo: dict, environment):
    for transporter in environment.transportcompany.transporters:
        if transporter.id not in transporterinfo.keys():
            transporterinfo[transporter.id] = [transporter.state]
        else:
            transporterinfo[transporter.id].append(transporter.state)

    return transporterinfo