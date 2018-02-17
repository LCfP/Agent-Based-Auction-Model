import pandas as pd

summary_experiment_data = pd.DataFrame()

for exp_no in range(101):

    f = "./experiments/{0}/KPI_run_stats_df.csv".format(exp_no)
    df = pd.read_csv(f, header=0)
    summary_experiment_data = summary_experiment_data.append(df, ignore_index=False)

print(summary_experiment_data)


print("results on number of matches")
print(summary_experiment_data['number of matches'].mean(axis=0))
print(summary_experiment_data['number of matches'].std(axis=0))

print("results on match distance")
print(summary_experiment_data['average match distance'].mean(axis=0))
print(summary_experiment_data['average match distance'].std(axis=0))

print("results on container idle time")
print(summary_experiment_data['average container idle time'].mean(axis=0))
print(summary_experiment_data['average container idle time'].std(axis=0))

print("results on average shipment idle time")
print(summary_experiment_data['average shipment idle time'].mean(axis=0))
print(summary_experiment_data['average shipment idle time'].std(axis=0))

summary_experiment_data.to_csv("./experiments/{0}/summary experiment.csv"
                            .format(0))