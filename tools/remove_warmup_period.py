def remove_warmup_period(environment, data: list):
    # Remove data from warmup period
    containerinfo_df = data[0].iloc[environment.config.warmup_period:]

    # shipmentinfo_df = data[1].iloc[environment.config.warmup_period:]
    shipmentinfo_df = data[1]

    transporterinfo_df = data[2].iloc[
                         environment.config.warmup_period:]

    return [containerinfo_df, shipmentinfo_df, transporterinfo_df, data[3]]