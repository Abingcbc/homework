import happybase
import pandas as pd
import numpy as np

# df = pd.read_csv('../../movies.csv', dtype=str)

print('connect HBase successfully\n')

# connection.create_table("year", {"c1": dict()})
# connection.create_table("month", {"c2": dict()})
# connection.create_table("quater", {"c3": dict()})
# connection.create_table("week", {"c4": dict()})
# connection.create_table("name", {"c5": dict()})
# connection.create_table("director", {"c6": dict()})
# connection.create_table("actor", {"c7": dict()})
# connection.create_table("da", {"c8": dict()})
# connection.create_table("aa", {"c9": dict()})
# connection.create_table("genre", {"c10": dict()})
# connection.create_table("score", {"c11": dict()})
# connection.create_table("sentiment", {"c12": dict()})
print('create table successfully\n')

# year_table = connection.table("year")
# month_table = connection.table("month")
# quater_table = connection.table("quater")
# week_table = connection.table("week")
# name_table = connection.table("name")
# director_table = connection.table("director")
# actor_table = connection.table("actor")

# print('Begin create year')
# count = 0
# record_map = {}
# for index, row in df.iterrows():
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')
#     if pd.notna(row['year']):
#         if record_map.get(row['year'], '') == '':
#             record_map[str(row['year'])] = row['id']
#         else:
#             record_map[str(row['year'])] += '|' + row['id']
# with year_table.batch() as b:
#     for key, value in record_map.items():
#         b.put(key, {b'c1:id': value})
#
# print('Begin create month')
# count = 0
# record_map = {}
# for index, row in df.iterrows():
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')
#     if pd.notna(row['month']):
#         month_string = str(row['month'])
#         month_string = month_string if len(month_string) == 2 else '0' + month_string
#         if record_map.get(month_string, '') == '':
#             record_map[month_string] = row['id']
#         else:
#             record_map[month_string] += '|' + row['id']
# with month_table.batch() as b:
#     for key, value in record_map.items():
#         b.put(key, {b'c2:id': value})
#
# print('Begin create quater')
# count = 0
# record_map = {}
# for index, row in df.iterrows():
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')
#     if pd.notna(row['quater']):
#         if record_map.get(str(row['quater']), '') == '':
#             record_map[str(row['quater'])] = row['id']
#         else:
#             record_map[str(row['quater'])] += '|' + row['id']
# with quater_table.batch() as b:
#     for key, value in record_map.items():
#         b.put(key, {b'c3:id': value})
#
# print('Begin create week')
# count = 0
# record_map = {}
# for index, row in df.iterrows():
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')
#     if pd.notna(row['day_of_the_week']):
#         if record_map.get(str(row['day_of_the_week']), '') == '':
#             record_map[str(row['day_of_the_week'])] = row['id']
#         else:
#             record_map[str(row['day_of_the_week'])] += '|' + row['id']
# with week_table.batch() as b:
#     for key, value in record_map.items():
#         b.put(key, {b'c4:id': value})
#
# print('Begin create name')
# count = 0
# record_map = {}
# for index, row in df.iterrows():
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')
#     if pd.notna(row['movie_name']):
#         if record_map.get(row['movie_name'], '') == '':
#             record_map[row['movie_name']] = row['id']
#         else:
#             record_map[row['movie_name']] += '|' + row['id']
# with name_table.batch() as b:
#     for key, value in record_map.items():
#         b.put(key, {b'c5:id': value})
#
# print('Begin create director')
# count = 0
# record_map = {}
# for index, row in df.iterrows():
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')
#     if pd.notna(row['directors']):
#         for director in row['directors'].split(','):
#             if record_map.get(director, '') == '':
#                 record_map[director] = row['id']
#             else:
#                 record_map[director] += '|' + row['id']
# with director_table.batch() as b:
#     for key, value in record_map.items():
#         b.put(key, {b'c6:id': value})
#
#
# print('Begin create actor')
# count = 0
# record_map = {}
# for index, row in df.iterrows():
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')
#     if pd.notna(row['actors']):
#         for actor in row['actors'].split(','):
#             if record_map.get(actor, '') == '':
#                 record_map[actor] = row['id']
#             else:
#                 record_map[actor] += '|' + row['id']
# with actor_table.batch() as b:
#     for key, value in record_map.items():
#         b.put(key, {b'c7:id': value})
#
# print('Begin create star')
# count = 0
# record_map = {}
# for index, row in df.iterrows():
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')
#     if pd.notna(row['starring']):
#         for star in row['starring'].split(','):
#             if record_map.get(star, '') == '':
#                 record_map[star] = row['id']
#             else:
#                 record_map[star] += '|' + row['id']
# connection = happybase.Connection("localhost")
# connection.create_table("star", {"c13": dict()})
# star_table = connection.table("star")
# with star_table.batch() as b:
#     for key, value in record_map.items():
#         b.put(key, {b'c13:id': value})
#
# print('Begin create da')
# count = 0
# record_map = {}
# temp_map = {}
# for index, row in df.iterrows():
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')
#     if pd.notna(row['directors']) and \
#             (pd.notna(row['actors']) or pd.notna(row['starring'])):
#         col1List = row['directors'].split(',')
#         col2List = []
#         if pd.notna(row['actors']):
#             col2List += str(row.get('actors', '')).split(',')
#         if pd.notna(row['starring']):
#             col2List += str(row.get('starring', '')).split(',')
#         for c1 in col1List:
#             if c1 == 'various' or c1 == 'unavailable' or len(c1) < 2:
#                 continue
#             for c2 in col2List:
#                 if c2 == 'various' or c2 == 'unavailable' or len(c2) < 2:
#                     continue
#                 if temp_map.get(c1 + '|' + c2, 0) == 0:
#                     temp_map[c1 + '|' + c2] = 1
#                 else:
#                     temp_map[c1 + '|' + c2] += 1
# connection = happybase.Connection("localhost")
# da_table = connection.table("da")
# count = 0
# for key, value in temp_map.items():
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')
#     if record_map.get(value, 0) == 0:
#         record_map[value] = 1
#     else:
#         record_map[value] += 1
#     da_table.put(str(value) + '-' + str(record_map[value]), {b'c8:id': str(key)})
#
# print('Begin create aa')
# count = 0
# record_map = {}
# temp_map = {}
# for index, row in df.iterrows():
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')
#     if pd.notna(row['actors']) or pd.notna(row['starring']):
#         colList = []
#         if pd.notna(row['actors']):
#             colList += str(row.get('actors', '')).split(',')
#         if pd.notna(row['starring']):
#             colList += str(row.get('starring', '')).split(',')
#         mark = {}
#         for c1 in colList:
#             if c1 == 'various' or len(c1) < 2:
#                 continue
#             for c1_1 in colList:
#                 if c1 == c1_1 or len(c1_1) < 2:
#                     continue
#                 t1 = min(c1, c1_1)
#                 t2 = max(c1, c1_1)
#                 if mark.get(t1 + '|' + t2, 0) == 0:
#                     mark[t1 + '|' + t2] = 1
#                 else:
#                     continue
#                 if temp_map.get(t1 + '|' + t2, 0) == 0:
#                     temp_map[t1 + '|' + t2] = 1
#                 else:
#                     temp_map[t1 + '|' + t2] += 1
# connection = happybase.Connection("localhost")
# aa_table = connection.table("aa")
# count = 0
# for key, value in temp_map.items():
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')
#     if record_map.get(value, 0) == 0:
#         record_map[value] = 1
#     else:
#         record_map[value] += 1
#     aa_table.put(str(value) + '-' + str(record_map[value]), {b'c9:id': str(key)})
#
# print('Begin create genre')
# count = 0
# record_map = {}
# for index, row in df.iterrows():
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')
#     if pd.notna(row['genres']):
#         for genre in row['genres'].split(','):
#             if record_map.get(genre, '') == '':
#                 record_map[genre] = {row['id']}
#             else:
#                 record_map[genre].add(row['id'])
# connection = happybase.Connection("localhost")
# genre_table = connection.table("genre")
# for key, value in record_map.items():
#     for index, ID in enumerate(value):
#         genre_table.put(key + '-' + str(index), {b'c10:id': ID})
#
#
df = pd.read_csv('../../comments.csv', dtype=str)
print('Begin insert score')
count = 0
record_map = {0: set(), 1: set(), 2: set(),
              3: set(), 4: set(), 5: set()}
sentiment_map = {-1: set(), 0: set(), 1: set()}

cur_key = ''
score_list = []
for index, row in df.iterrows():
    count += 1
    if count % 10000 == 0:
        print('----' + str(count) + '----')
    if cur_key != row['movie_id']:
        if len(cur_key) != 0:
            record_map[int(np.mean(score_list))].add(cur_key)
            score_list.clear()
            score_list.append(eval(row['score']))
            if int(eval(row['score'])) >= 4:
                sentiment_map[1].add(row['movie_id'])
            elif int(eval(row['score'])) <= 2:
                sentiment_map[-1].add(row['movie_id'])
            else:
                sentiment_map[0].add(row['movie_id'])
        cur_key = row['movie_id']
    else:
        score_list.append(eval(row['score']))
        if int(eval(row['score'])) >= 4:
            sentiment_map[1].add(row['movie_id'])
        elif int(eval(row['score'])) <= 2:
            sentiment_map[-1].add(row['movie_id'])
        else:
            sentiment_map[0].add(row['movie_id'])
connection = happybase.Connection("localhost")
score_table = connection.table("score")
# sentiment_table = connection.table("sentiment")
for key, value in record_map.items():
    print(key)
    for index, ID in enumerate(value):
        score_table.put(str(int(key))+'-'+str(index), {b'c11:id': ID})

# for key, value in sentiment_map.items():
#     print(key)
#     for index, ID in enumerate(value):
#         sentiment_table.put(str(int(key))+'-'+str(index), {b'c12:id': ID})

connection.close()

