import happybase
import pandas as pd
import time

columns = \
    ["id", "name", "asin", "score",
     "imdb", "year", "month", "day",
     "quater", "week", "ds", "as",
     "star", "ps", "lan", "genres",
     "studio", "ws"]

def queryMovieByYearRow(timeObject):
    connection = happybase.Connection("localhost")
    yr_table = connection.table('yr')
    movie_table = connection.table('movie')
    cost = []
    for i in range(101):
        start_time = time.time()
        result = list(yr_table.row(timeObject['year']).values())
        # movie = movie_table.rows(result)
        end_time = time.time()
        if i > 0:
            print(end_time-start_time)
            cost.append(end_time-start_time)
    with open('year_2001_r.txt', 'w') as file:
        file.write(str(cost))
    # html = pd.DataFrame(r[0:100], columns=columns).to_html()
    # print(len(movie))
    connection.close()
    # return html, len(r)

def queryMovieByYearCol(timeObject):
    connection = happybase.Connection("localhost")
    yc_table = connection.table('yc')
    movie_table = connection.table('movie')
    cost = []
    for i in range(101):
        result = []
        start_time = time.time()
        for key, data in yc_table.scan(row_prefix=timeObject['year'].encode()):
            result.append(data[b'c17:id'])
        # movie = movie_table.rows(result)
        end_time = time.time()
        if i > 0:
            print(end_time-start_time)
            cost.append(end_time-start_time)
    with open('year_2001_c.txt', 'w') as file:
        file.write(str(cost))
    # html = pd.DataFrame(r[0:100], columns=columns).to_html()
    # print(len(movie))
    connection.close()
    # return html, len(r)

if __name__ == '__main__':
    # queryMovieByYearRow({'year':'2001'})
    queryMovieByYearCol({'year':'2001'})
