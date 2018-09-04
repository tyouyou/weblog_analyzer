import pandas as pd
from datetime import datetime, timezone, timedelta
import matplotlib
import pprint

data = pd.read_csv("./output_access_log.csv", header=0, encoding="shift-jis")

# print(data.columns)

data["time"] = pd.to_datetime(data["time"])
# print(abs(data['time'][0]-data['time'][1]))

# dataframe to dictionary, key is data['user]
dic = {}
for index, row in data.iterrows():
    if row['user'] in dic:
        dic[row['user']].append(row.tolist())
    else:
        dic[row['user']] = [row.tolist()]

# sorted list to session dictionary
def li_to_dic(li):
    sess_no = 0
    sess_dic = {}
    sess_dic[sess_no] = [li[0]]
    for i in range(1, len(li)):
        if li[i][6] - li[i-1][6] > timedelta(minutes=30):
            sess_no = sess_no + 1
            sess_dic[sess_no] = [li[i]]
        else:
            print(sess_no)
            print(sess_dic[sess_no])
            sess_dic[sess_no].append(li[i])
    return sess_dic

# sort list in dictionary by timestamp
for k, v in dic.items():
    v.sort(key = lambda row: row[6])

# divide session by timestamp in same user dictionary
dic_sess = {}
for k,v in dic.items(): 
    dic_sess[k] = li_to_dic(dic[k])

pprint.pprint(dic_sess)






#grouped = data.groupby('user')
# print(grouped['time'])


# for index, row in data.iterrows():
#   print(row['user'], row['time'])

# Plot of grouped
# ax = grouped.size().plot.bar(rot=0)
# fig = ax.get_figure()
# fig.savefig('./groupby_size.png')
