import happybase
import pandas as pd
import numpy as np
import time

columns = \
    ["id", "name", "asin", "score",
     "imdb", "year", "month", "day",
     "quater", "week", "ds", "as",
     "star", "ps", "lan", "genres",
     "studio", "ws"]


def query(movie_table, filterString):
    count = 0
    result = []
    start_time = time.time()
    for key, data in movie_table.scan(
            filter=filterString):
        # pass
        count += 1
        temp = {'id': key.decode()}
        for k, v in data.items():
            t = v.decode()
            temp[k.decode()[3:]] = t
        result.append(temp)
    end_time = time.time()
    cost = end_time-start_time
    print('get ' + str(count) + ' movies')
    html = pd.DataFrame(result[0:100], columns=columns).to_html()
    return html, count, cost


def queryMovieByTime(timeObject):
    connection = happybase.Connection("localhost")
    movie_table = connection.table("movie")
    filterString = ''
    count = 0
    for key, value in timeObject.items():
        if count != 0:
            filterString += ' AND '
        count += 1
        filterString += "SingleColumnValueFilter ('cf', '" + key + "', =, 'binary:" + str(value) + "', true, false)"
    print(filterString)
    # cost = []
    # query(movie_table, filterString)
    # for i in range(101):
        # if i > 0:
        #     print(end_time - start_time)
        #     cost.append(end_time - start_time)
    # with open('year_2001.txt', 'w') as file:
    #     file.write(str(cost))
    html, count, cost = query(movie_table, filterString)
    connection.close()
    return html, count, cost


def queryMovieByName(name):
    connection = happybase.Connection("localhost")
    movie_table = connection.table("movie")
    filterString = "SingleColumnValueFilter ('cf', 'name', =, 'substring:" + name['name'] + "', true, false)"
    html, count, cost = query(movie_table, filterString)
    connection.close()
    return html, count, cost


def queryMovieByPeople(peopleObject):
    connection = happybase.Connection("localhost")
    movie_table = connection.table("movie")
    filterString = ""
    key2Column = {
        'director': 'ds',
        'starring': 'star'
    }
    count = 0
    for key, value in peopleObject.items():
        if count != 0:
            filterString += " AND "
        count += 1
        if key == 'actor':
            filterString += "SingleColumnValueFilter ('cf', 'as', =, 'substring:" + value + "', true, false)"
            filterString += " OR "
            filterString += "SingleColumnValueFilter ('cf', 'star', =, 'substring:" + value + "', true, false)"
        else:
            filterString += "SingleColumnValueFilter ('cf', '" + key2Column[key] + \
                            "', =, 'substring:" + value + "', true, false)"
    cost = []
    for i in range(101):
        start_time = time.time()
        query(movie_table, filterString)
        end_time = time.time()
        if i > 0:
            cost.append(end_time-start_time)
            print(end_time-start_time)
    with open('actor_a.txt', 'w') as file:
        file.write(str(cost))
    connection.close()


def queryRelation(relation):
    queryMap = {}
    connection = happybase.Connection("localhost")
    movie_table = connection.table("movie")
    print('Query Start')
    if relation['relation'] == 'a|a':
        count = 0
        cost = []
        for i in range(101):
            print(count)
            count += 1
            start_time = time.time()
            for key, data in movie_table.scan():
                col1 = data.get(b'cf:as', b'')
                col2 = data.get(b'cf:star', b'')
                col1List = col1.decode().split(',')
                col2List = col2.decode().split(',')
                mark = {}
                for c1 in col1List:
                    if c1 == 'various' or len(c1) < 2:
                        continue
                    for c1_1 in col1List:
                        if c1 == c1_1 or len(c1_1) < 2:
                            continue
                        t1 = min(c1, c1_1)
                        t2 = max(c1, c1_1)
                        if mark.get(t1 + '|' + t2, 0) == 0:
                            mark[t1 + '|' + t2] = 1
                        else:
                            continue
                        if queryMap.get(t1 + '|' + t2, 0) == 0:
                            queryMap[t1 + '|' + t2] = 1
                        else:
                            queryMap[t1 + '|' + t2] += 1
                    for c2 in col2List:
                        if c1 == c2 or len(c2) < 2:
                            continue
                        t1 = min(c1, c2)
                        t2 = max(c1, c2)
                        if mark.get(t1 + '|' + t2, 0) == 0:
                            mark[t1 + '|' + t2] = 1
                        else:
                            continue
                        if queryMap.get(t1 + '|' + t2, 0) == 0:
                            queryMap[t1 + '|' + t2] = 1
                        else:
                            queryMap[t1 + '|' + t2] += 1
                for c2 in col2List:
                    if c2 == 'various' or len(c2) < 2:
                        continue
                    for c2_2 in col2List:
                        if c2 == c2_2 or len(c2_2) < 2:
                            continue
                        t1 = min(c2_2, c2)
                        t2 = max(c2_2, c2)
                        if mark.get(t1 + '|' + t2, 0) == 0:
                            mark[t1 + '|' + t2] = 1
                        else:
                            continue
                        if queryMap.get(t1 + '|' + t2, 0) == 0:
                            queryMap[t1 + '|' + t2] = 1
                        else:
                            queryMap[t1 + '|' + t2] += 1
            result = sorted([[key, value] for key, value in queryMap.items()], key=lambda x: x[1], reverse=True)
            end_time = time.time()
            if count > 1:
                cost.append(end_time-start_time)
    elif relation['relation'] == 'd|a':
        for key, data in movie_table.scan():
            col1 = data.get(b'cf:as', b'')
            col2 = data.get(b'cf:star', b'')
            col3 = data.get(b'cf:ds', b'')
            col1List = col1.decode().split(',')
            col2List = col2.decode().split(',')
            col3List = col3.decode().split(',')
            for c3 in col3List:
                if c3 == 'various' or c3 == 'unavailable' or len(c3) < 2:
                    continue
                for c1 in col1List:
                    if c1 == 'various' or c1 == 'unavailable' or len(c1) < 2:
                        continue
                    if queryMap.get(c3 + '|' + c1, 0) == 0:
                        queryMap[c3 + '|' + c1] = 1
                    else:
                        queryMap[c3 + '|' + c1] += 1
                for c2 in col2List:
                    if c2 == 'various' or c2 == 'unavailable' or len(c2) < 2:
                        continue
                    if queryMap.get(c3 + '|' + c2, 0) == 0:
                        queryMap[c3 + '|' + c2] = 1
                    else:
                        queryMap[c3 + '|' + c2] += 1
    with open('relation_a|a.txt', 'w') as file:
        file.write(str(cost))
    print('Sort Start')
    # result = sorted([[key, value] for key, value in queryMap.items()], key=lambda x: x[1], reverse=True)
    # html = pd.DataFrame(result[0:100], columns=['relation', 'number']).to_html()
    connection.close()
    # return html, len(result)


def queryMovieByGenres(genres):
    connection = happybase.Connection("localhost")
    movie_table = connection.table("movie")
    filterString = "SingleColumnValueFilter ('cf', 'genres', =, 'substring:" + genres['genres'] + "', true, false)"
    html, count, cost = query(movie_table, filterString)
    connection.close()
    return html, count, cost


def queryMovieByScore(scoreObject):
    connection = happybase.Connection("localhost")
    comment_table = connection.table("review")
    score = int(scoreObject['score'][-1])
    comparer = scoreObject['score'][:-1]
    hit_id = []
    score_list = []
    comparer_map = {
        '>': lambda l: np.mean(l) > score,
        '<': lambda l: np.mean(l) < score
    }
    cur_key = ''
    cost = []
    for i in range(6):
        start_time = time.time()
        for key, data in comment_table.scan():
            if cur_key != data[b'cf1:id'].decode():
                if len(cur_key) != 0 and comparer_map[comparer](score_list):
                    hit_id.append([cur_key, np.mean(score_list)])
                    score_list.clear()
                    score_list.append(int(eval(data.get(b'cf1:score').decode())))
                cur_key = data[b'cf1:id'].decode()
            else:
                score_list.append(int(eval(data.get(b'cf1:score').decode())))
        end_time = time.time()
        if i > 0:
            print(end_time-start_time)
            cost.append(end_time-start_time)
    with open('score_>3_bloom.txt', 'w') as file:
        file.write(str(cost))
    # html = pd.DataFrame(hit_id[0: 100], columns=['id', 'score']).to_html()
    connection.close()
    # return html, len(hit_id)


def queryMovieBySentiment(sentiment):
    connection = happybase.Connection("localhost")
    comment_table = connection.table("review")
    comparer = sentiment['sentiment']
    comparer_map = {
        1: lambda s: s >= 4,
        0: lambda s: s == 3,
        -1: lambda s: s <= 2
    }
    hit_id = []
    flag = True
    remain = True
    row_start = ''
    while flag:
        for key, data in comment_table.scan(row_start=row_start):
            if comparer_map[comparer](int(eval(data.get(b'cf1:score').decode()))):
                hit_id.append(data[b'cf1:id'].decode())
                # 利用 HBase 特性的小技巧
                row_start = data[b'cf1:id'] + '1'
                remain = True
                break
            remain = False
        if not remain:
            flag = False

if __name__ == '__main__':
    queryMovieByScore({'score': '>3'})
    # queryMovieByTime({'year': 2001})