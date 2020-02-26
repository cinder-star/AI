import pandas as pd
import matplotlib.pyplot as plt

csv_list = ["bfs.csv", "ucs.csv", "gbfs.csv", "a*.csv", "dls.csv", "ids.csv"]
for csv in csv_list:
    data_frame = pd.read_csv(csv,delimiter=",")
    plt.plot(data_frame["depth"], data_frame["nodes"], label=csv.split(".")[0], linestyle='solid', marker='o')

plt.legend(loc = "upper left")
plt.xlabel("depth")
plt.ylabel("generated nodes")
plt.xticks(range(0,21))
plt.ylim([0,max(data_frame["nodes"])+1])
plt.grid()
plt.show()