import pandas as pd

all_data = pd.DataFrame()

for exp_no in range(10):
    f = "./experiments/{0}/KPI_run_stats_df.csv".format(exp_no)
    df = pd.read_csv(f, header=0)
    all_data = all_data.append(df, ignore_index=False)
print(all_data)

print(all_data['average container idle time:'].mean(axis=0))
print(all_data['average container idle time:'].std(axis=0))