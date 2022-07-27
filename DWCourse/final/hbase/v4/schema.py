import happybase
import pandas as pd
import numpy as np

df = pd.read_csv('../../movies.csv', dtype=str)

print('Begin create year_row')
count = 0
record_map = {}
for index, row in df.iterrows():
    count += 1
    if count % 10000 == 0:
        print('----' + str(count) + '----')
    if pd.notna(row['year']):
        if record_map.get(row['year'], '') == '':
            record_map[row['year']] = [row['id']]
        else:
            record_map[row['year']].append(row['id'])
connection = happybase.Connection("localhost")
# connection.create_table("yr", {"c16": dict()})
yr_table = connection.table('yr')
for key, value in record_map.items():
    yr_table.put(str(key), dict(zip([('c16:'+str(i)).encode()
                                for i in range(len(value))], value)))
connection.close()

print('Begin create year_col')
count = 0
record_map = {}
for index, row in df.iterrows():
    count += 1
    if count % 10000 == 0:
        print('----' + str(count) + '----')
    if pd.notna(row['year']):
        if record_map.get(row['year'], '') == '':
            record_map[row['year']] = [row['id']]
        else:
            record_map[row['year']].append(row['id'])
connection = happybase.Connection("localhost")
# connection.create_table("yc", {"c17": dict()})
yc_table = connection.table('yc')
for key, value in record_map.items():
    for index, ID in enumerate(value):
        yc_table.put(str(key) + '-' + str(index), {b'c17:id': ID})
connection.close()