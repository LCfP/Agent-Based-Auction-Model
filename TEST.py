import pandas as pd

d = {'one': [1,2,3],
     'two': [3,4,5]}

df = pd.DataFrame(d)

print(df)


row_min = df.min(axis=1)
row_max = df.max(axis=1)
row_average = df.mean(axis=1)

print(row_min)
print(row_max)
print(row_average)

df["min"] = df.min(axis = 1)

print(df)