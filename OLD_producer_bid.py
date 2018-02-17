def bid(self, registrationkey, item: Shipment):
    ''' Minimum shipment biddingvalue consists of:
    1) transport costs from hub to pickup location
    2) transport costs from pickup location to destination'''
    producerbid = namedtuple('producerbid', 'registration_key biddingvalue')
    hub_coords = find_hub_coordinates(self.region)
    transport_cost_from_hub = self.env.config.transport_cost * \
                              route_euclidean_distance(self.env,
                                                       hub_coords,
                                                       item.location)
    transport_cost_to_destination = self.env.config.transport_cost * \
                                    route_euclidean_distance(self.env,
                                                             item.location,
                                                             item.destination)
    # TODO improve biddingvalue based on shipping urgency
    if len(self.storage) >= self.env.config.storage_urgency_level * \
            self.storage_capacity:
        shipping_urgency_cost = transport_cost_from_hub
    else:
        shipping_urgency_cost = 0
    # TODO add standard fees for container functionalties
    total_value = transport_cost_from_hub + transport_cost_to_destination \
                  + shipping_urgency_cost + 1

    producerbid = producerbid(registration_key=registrationkey,
                              biddingvalue=total_value)

    if self.env.config.debug is True and self.region.id < 1:
        print("producer %s in region: %s enters bid: %s "
              "for shipment with id: %s"
              % (self.id, self.region.id, producerbid, item.id))

    return producerbid