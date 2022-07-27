import happybase
import pandas as pd

connection = happybase.Connection("localhost")
print('connect HBase successfully\n')

# connection.create_table("movie", {"cf": dict()})
# connection.create_table("review", {"cf1": dict()})
print('create table successfully\n')

# movie_table = connection.table("movie")
review_table = connection.table("review")

movie_attr = {
    "movie_name": "name",
    "product_asin": "asin",
    "score": "score",
    "imdb": "imdb",
    "year": "year",
    "month": "month",
    "day": "day",
    "quater": "quater",
    "day_of_the_week": "week",
    "directors": "ds",
    "actors": "as",
    "starring": "star",
    "producers": "ps",
    "language": "lan",
    "genres": "genres",
    "studio": "studio",
    "writers": "ws"
}
comment_attr = {
    "movie_id": "id",
    "summary": "sum",
    "score": "score",
    "time": "time",
    "helpfulness": "help",
    "user_id": "uid"
}

# df = pd.read_csv('../../movies.csv', dtype=str)
# print('Begin insert movie')
# count = 0
# for index, row in df.iterrows():
#     temp_map = {}
#     for attr in movie_attr.keys():
#         if pd.notna(row[attr]):
#             temp_map['cf:'+movie_attr[attr]] = row[attr]
#     movie_table.put(row['id'], temp_map)
#     count += 1
#     if count % 10000 == 0:
#         print('----' + str(count) + '----')

df = pd.read_csv('../../comments.csv', dtype=str)
print('Begin insert comment')
count = 0
for index, row in df.iterrows():
    temp_map = {}
    for attr in comment_attr.keys():
        if pd.notna(row[attr]):
            temp_map['cf1:'+comment_attr[attr]] = row[attr]
    review_table.put(str(count), temp_map)
    count += 1
    if count % 10000 == 0:
        print('----' + str(count) + '----')

connection.close()