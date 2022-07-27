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

def queryMovieByTime(timeObject):
    connection = happybase.Connection("localhost")
    result = set()
    key2Column = {
        'year': b'c1:id',
        'month': b'c2:id',
        'quater': b'c3:id',
        'week': b'c4:id'
    }
    movie_table = connection.table('movie')
    index_table = connection.table('year')
    cost = []
    for i in range(101):
        result = set()
        start_time = time.time()
        result = index_table.row('2001')[b'c1:id'] \
            .decode().split('|')
        # for key, value in timeObject.items():
        #     index_table = connection.table(key)
        #     current = set(index_table.row(str(value))[key2Column[key]]
        #                   .decode().split('|'))
        #     if len(result) == 0:
        #         result = current
        #     else:
        #         result = result & current
        r = []
        result = sorted(result)
        movie = movie_table.rows(result)
            # for key, value in movie.items():
            #     temp[key.decode()[3:]] = value.decode()
            # r.append(temp)
        end_time = time.time()
        if i > 0:
            print(end_time - start_time)
            cost.append(end_time - start_time)
    with open('year_2001_bloom_cache.txt', 'w') as file:
        file.write(str(cost))
    # html = pd.DataFrame(r[0:100], columns=columns).to_html()
    # print(len(r))
    connection.close()
    # return html, len(r)

def queryMovieByName(name):
    connection = happybase.Connection("localhost")
    index_table = connection.table("name")
    movie_table = connection.table('movie')
    start_time = time.time()
    id_list = index_table.row(name['name'])[b'c5:id'].decode().split(',')
    result = []
    for ID in id_list:
        result.append(movie_table.row(ID))
    end_time = time.time()
    html = pd.DataFrame(result[0:100], columns=columns).to_html()
    print(len(result))
    connection.close()
    return html, len(result), end_time - start_time

def queryMovieByPeople(peopleObject):
    connection = happybase.Connection("localhost")
    if peopleObject.get('director', None) is not None:
        index_table = connection.table("director")
        movie_table = connection.table('movie')
        start_time = time.time()
        id_list = index_table.row(peopleObject['director'])[b'c6:id'].decode().split('|')
        result = []
        for ID in id_list:
            temp = {}
            movie = movie_table.row(ID)
            for key, value in movie.items():
                temp[key.decode()[3:]] = value.decode()
            result.append(temp)
        end_time = time.time()
        html = pd.DataFrame(result[0:100], columns=columns).to_html()
        print(len(result))
        connection.close()
        return html, len(result), end_time-start_time
    elif peopleObject.get('starring', None) is not None:
        index_table = connection.table("star")
        movie_table = connection.table('movie')
        start_time = time.time()
        id_list = index_table.row(peopleObject['starring'])[b'c13:id'].decode().split('|')
        result = []
        for ID in id_list:
            temp = {}
            movie = movie_table.row(ID)
            for key, value in movie.items():
                temp[key.decode()[3:]] = value.decode()
            result.append(temp)
        end_time = time.time()
        html = pd.DataFrame(result[0:100], columns=columns).to_html()
        print(len(result))
        connection.close()
        return html, len(result), end_time-start_time
    elif peopleObject.get('actor', None) is not None:
        index_table = connection.table("star")
        index_table2 = connection.table("actor")
        movie_table = connection.table('movie')
        cost = []
        # for i in range(101):
        start_time = time.time()
        id_list = []
        temp = index_table.row(peopleObject['actor'])
        if len(temp) != 0:
            id_list = temp[b'c13:id'].decode().split('|')
        id_list += index_table2.row(peopleObject['actor'])[b'c7:id'].decode().split('|')
        result = []
        for ID in id_list:
            temp = {}
            movie = movie_table.row(ID)
            for key, value in movie.items():
                temp[key.decode()[3:]] = value.decode()
            result.append(temp)
        end_time = time.time()
            # if i > 0:
            #     print(end_time-start_time)
            #     cost.append(end_time-start_time)
        # with open('actor_a.txt', 'w') as file:
        #     file.write(str(cost))
        html = pd.DataFrame(result[0:100], columns=columns).to_html()
        # print(len(result))
        connection.close()
        return html, len(result), end_time-start_time

def queryMovieByRelation(relation):
    if relation.get('relation', None) == 'd|a':
        connection = happybase.Connection("localhost")
        da_table = connection.table('da')
        result_map = {}
        start_time = time.time()
        for key, data in da_table.scan():
            num = int(key.decode().split('-')[0])
            if result_map.get(num, None) is None:
                result_map[num] = [data[b'c8:id']]
            else:
                result_map[num].append(data[b'c8:id'])
        result = []
        sorted_key = sorted(result_map.keys(), reverse=True)
        for key in sorted_key:
            for ID in result_map[key]:
                result.append({'id': ID, 'number':key})
        end_time = time.time()
        html = pd.DataFrame(result[0:100], columns=['number', 'id']).to_html()
        print(len(result))
        connection.close()
        return html, len(result), end_time-start_time
    elif relation.get('relation', None) == 'a|a':
        connection = happybase.Connection("localhost")
        aa_table = connection.table('aa')
        result_map = {}
        start_time = time.time()
        for key, data in aa_table.scan():
            num = int(key.decode().split('-')[0])
            if result_map.get(num, None) is None:
                result_map[num] = [data[b'c9:id']]
            else:
                result_map[num].append(data[b'c9:id'])
        result = []
        sorted_key = sorted(result_map.keys(), reverse=True)
        for key in sorted_key:
            for ID in result_map[key]:
                result.append({'id': ID, 'number':key})
        end_time = time.time()
        html = pd.DataFrame(result[0:100], columns=['number', 'id']).to_html()
        print(len(result))
        connection.close()
        return html, len(result), end_time-start_time

def queryMovieByGenres(genres):
    connection = happybase.Connection("localhost")
    genre_table = connection.table('genre')
    movie_table = connection.table('movie')
    id_list = []
    start_time = time.time()
    for key, data in genre_table.scan(row_prefix=(genres['genres']+'-').encode()):
        id_list.append(data[b'c10:id'].decode())
    result = []
    for ID in id_list:
        temp = {}
        movie = movie_table.row(ID)
        for key, value in movie.items():
            temp[key.decode()[3:]] = value.decode()
        result.append(temp)
    end_time = time.time()
    html = pd.DataFrame(result[0:100], columns=columns).to_html()
    print(len(result))
    connection.close()
    return html, len(result), end_time-start_time

def queryMovieByScore(scoreObject):
    connection = happybase.Connection("localhost")
    score_table = connection.table('score')
    movie_table = connection.table('movie')
    score = int(scoreObject['score'][-1])
    comparer = scoreObject['score'][:-1]
    cost = []
    # for i in range(1):
    id_list = []
    start_time = time.time()
    if comparer == '>':
        for key, data in score_table.scan(row_start=(str(score)+'-').encode()):
            id_list.append({'score':key.decode().split('-')[0], 'id':data[b'c11:id'].decode()})
    else:
        for key, data in score_table.scan(row_start=(str(score)+'-').encode(), reverse=True):
            id_list.append({'score':key.decode().split('-')[0], 'id':data[b'c11:id'].decode()})
        result = []
        # sorted(id_list)
        # movie = movie_table.rows(id_list)
    end_time = time.time()
    print(len(id_list))
        # if i >= 0:
        #     print(end_time-start_time)
        #     cost.append(end_time-start_time)
    # with open('score_>3.txt', 'w') as file:
    #     file.write(str(cost))
    html = pd.DataFrame(id_list[0:100], columns=['score', 'id']).to_html()
    # print(len(result))
    connection.close()
    return html, len(id_list), end_time-start_time

def queryMovieBySentiment(sentiment):
    connection = happybase.Connection("localhost")
    sentiment_table = connection.table('sentiment')
    movie_table = connection.table('movie')
    id_list = []
    count = 0
    start_time = time.time()
    for key, data in sentiment_table.scan(row_prefix=(str(sentiment['sentiment'])+'-').encode()):
        count += 1
        if count % 10000 == 0:
            print('----' + str(count) + '----')
        id_list.append({'sentiment':key.decode().split('-')[0],
                        'id': data[b'c12:id'].decode()})
    # result = []
    # count = 0
    # id_list = sorted(id_list)
    # for ID in id_list:
    #     count += 1
    #     if count % 10000 == 0:
    #         print('----' + str(count) + '----')
    #     temp = {}
    #     movie = movie_table.row(ID)
    #     for key, value in movie.items():
    #         temp[key.decode()[3:]] = value.decode()
    #     result.append(temp)
    end_time = time.time()
    html = pd.DataFrame(id_list[0:100], columns=['sentiment','id']).to_html()
    # print(len(result))
    connection.close()
    return html, len(id_list), end_time-start_time

if __name__ == '__main__':
    # queryMovieByPeople({'actor':'aaron blabey'})
    # queryMovieByTime({'year': 2001})
    queryMovieByScore({'score':'>3'})