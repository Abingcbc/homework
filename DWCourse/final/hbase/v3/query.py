import happybase
import pandas as pd
import time

columns = \
    ["id", "name", "asin", "score",
     "imdb", "year", "month", "day",
     "quater", "week", "ds", "as",
     "star", "ps", "lan", "genres",
     "studio", "ws"]

def queryMovieByTime(timeObject):
    connection = happybase.Connection("localhost")
    time_table = connection.table('time')
    movie_table = connection.table('movie')
    time_string = 'y' + timeObject.get('year', '0000')
    if timeObject.get('month', None) is not None:
        time_string += '-m' + timeObject['month']
    if timeObject.get('week', None) is not None:
        time_string += '-w' + timeObject['week']
    cost = []
    for i in range(101):
        result = []
        start_time = time.time()
        for key, data in time_table.scan(row_prefix=time_string.encode()):
            result += data[b'c15:id'].decode().split('|')
        r = []
        movie = movie_table.rows(result)
        # for key, value in movie.items():
        #     temp[key.decode()[3:]] = value.decode()
        # r.append(temp)
        end_time = time.time()
        if i > 0:
            print(end_time-start_time)
            cost.append(end_time-start_time)
    with open('year_2001_01.txt', 'w') as file:
        file.write(str(cost))
    # html = pd.DataFrame(r[0:100], columns=columns).to_html()
    connection.close()
    # return html, len(r)

if __name__ == '__main__':
    queryMovieByTime({'year':'2001', 'month': '01'})