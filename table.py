import pandas as pd
import camelot.io as camelot

tables = camelot.read_pdf('MON2_RI_01_table.pdf', flavor = 'stream',pages='all')
dfs = []
for table in tables:
  df = table.df
  dfs.append(df)

df_all= pd.concat(dfs, ignore_index = True)
df_all.to_csv('mon2_ri_01_table.csv')



