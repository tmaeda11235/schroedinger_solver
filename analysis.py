import pandas as pd


csv = pd.read_csv("e:\\RWresult_a[0.05].csv",  chunksize=10)
for c in csv:
    print("{}".format(c.max))
    print("doing now")

