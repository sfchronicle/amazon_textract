import pandas as pd
from os import listdir
from os.path import isfile,join

path = "csv_from_image/MON2"
files = [f for f in listdir(path) if isfile(join(path, f))]
print(len(files))
all_df = []
for file in files:
  try:
    file_name = f"{path}/{file}"
    print(file_name)
    df = pd.read_csv(file_name)
    df['id'] = file.split('.')[0]
    all_df.append(df)
  except:
    continue

df = pd.concat(all_df)

df.to_csv('csv/mon2_2.csv')
