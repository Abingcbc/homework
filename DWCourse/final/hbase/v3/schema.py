import happybase
import pandas as pd
import numpy as np

df = pd.read_csv('../../movies.csv', dtype=str)

connection = happybase.Connection("localhost")
# connection.create_table("time", {"c15": dict()})

print('Begin create time')
count = 0
record_map = {}
for index, row in df.iterrows():
    count += 1
    if count % 10000 == 0:
        print('----' + str(count) + '----')
    time_string = ''
    if pd.notna(row['year']):
        time_string = 'y' + row['year']
    else:
        time_string = 'y0000'
    time_string += '-'
    if pd.notna(row['month']):
        if len(row['month']) == 1:
            time_string += 'm0'
        else:
            time_string += 'm'
        time_string += row['month']
    time_string += '-'
    if pd.notna(row['day_of_the_week']):
        time_string += 'w' + row['day_of_the_week']
    if record_map.get(time_string, '') == '':
        record_map[time_string] = row['id']
    else:
        record_map[time_string] += '|' + row['id']
time_table = connection.table('time')
with time_table.batch() as b:
    for key, value in record_map.items():
        b.put(key, {b'c15:id': value})

connection.close()