import pandas as pd
import camelot.io as camelot


# get all tables from pdf
# dfs = []
# for page in list(range(1,396)):
#   try:
#     table = camelot.read_pdf('pdf/super_messy_MON1_RISI_01.pdf', flavor = 'stream',pages=f'{page}',strip_text= '\n')

#     if len(table)  == 1:
#       df_table = table[0].df
#     else:
#       df_table = table.df
#   except:
#     pass
# # for table in tables:
#   dfs.append(df_table)
# df_all= pd.concat(dfs, ignore_index = True)

# df_all.to_csv('csv/super_messy_mon2_risi_01_table.csv')

table = camelot.read_pdf('pdf/BETH_SI_01_table.pdf', flavor = 'stream')



print(table[0].df)