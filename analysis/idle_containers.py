import matplotlib.pyplot as plt
import pandas as pd
from config import Config
from enums import ContainerState

def idle_containers(df):
    x = len(df.columns)
    df['idle'] = df.apply(lambda row: sum(row[0:x] == ContainerState.EMPTY) / x,
                          axis= 1)


    if Config.plot:
        df['idle'].plot()

        axes = plt.gca()
        axes.set_ylim([0, 1])

        plt.ylabel('% of containers that are idle')
        plt.xlabel('days')

        plt.show()