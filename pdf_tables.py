import json
import pandas as pd
import numpy as np

# with open('json/ROC_RICPIPR_01_table_01.json') as f:
#   data = json.load(f)

# lines = data[0][1:-2]

# print(len(lines)/3)
# splits = np.array_split(lines, 40)

# lists = []
# for array in splits:
#   lists.append(list(array))

# df = pd.DataFrame(lists, columns = ['date','time','restraint_type'])
# print(df)

with open('json/ROC_RICPIPR_01_table.json') as f:
  data = json.load(f)

print(len(data))

table_01 = data[0] + data[1] + data[2] + data[3]

# print(len(table_01)/3)
# splits = np.array_split(table_01, 146)
# lists = []
# for array in splits:
#   lists.append(list(array))

# df = pd.DataFrame(lists, columns = ['date','time','restraint_type'])
# df.to_csv('csv/ROC_RICPIPR_01_table_01.csv')

# table_02 = data[4] 
# print(len(table_02)/3)
# splits = np.array_split(table_02, 311)
# lists = []
# for array in splits:
#   #print(array)
#   lists.append(list(array))
# df = pd.DataFrame(lists, columns = ['date','time','restraint_type'])
# df.to_csv('csv/ROC_RICPIPR_01_table_02.csv')

table_03 = data[5] 
print(len(table_03)/5)
splits = np.array_split(table_03, 1018)
lists = []
for array in splits:
  print(array)
  lists.append(list(array))
df = pd.DataFrame(lists, columns = ['date','time','restraint_type','Gender','Ethnicity'])
df.to_csv('csv/ROC_RICPIPR_01_table_03.csv')