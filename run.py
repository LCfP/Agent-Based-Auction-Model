from environment import Environment


environment = Environment()
environment.setup()

for _ in range(environment.config.run_length):  # run model!
    pass
