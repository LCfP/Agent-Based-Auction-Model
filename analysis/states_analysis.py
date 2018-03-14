import matplotlib.pyplot as plt
from config import Config

def states_analysis(df, enum_state):
    states_occurrences_dict = state_occurrences(df, enum_state)
    states_averages = calculate_state_average(states_occurrences_dict, enum_state)

    if Config.plot:
        plot_state_averages(states_averages)

    return states_averages

def state_occurrences(df, enum_state):
    states_occurrences_dict = {}

    for state in [state.name for state in enum_state]:
        states_occurrences_dict[state] = []

    for state in states_occurrences_dict:

        for _id in df:
            count_of_state = (df[_id] ==
                        enum_state[state]).sum() \
                        / (df[_id].count())
            states_occurrences_dict[state].append(count_of_state)

    return states_occurrences_dict

def calculate_state_average(states_occurrences_dict, enum_state):
    states_averages = {}

    for state in [state.name for state in enum_state]:
        occurrences = states_occurrences_dict[state]
        average = round(sum(occurrences)/len(occurrences),2)
        states_averages[state] = average

    return states_averages

def plot_state_averages(states_averages):

    plt.bar(range(len(states_averages)), states_averages.values(),
            align='center')
    plt.xticks(range(len(states_averages)), list(states_averages.keys()))

    plt.show()

