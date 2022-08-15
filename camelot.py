import camelot.io as camelot
import pandas as pd

tables = camelot.read_pdf("pdf/BALL_RI_07_table.pdf", flavor='stream',pages='all')
print(tables[0])