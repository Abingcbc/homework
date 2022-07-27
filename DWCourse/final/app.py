from flask import Flask
from flask import request
from hbase.v1.query import queryMovieByTime, queryMovieByName, queryMovieByGenres
from hbase.v2.query import queryMovieByPeople, \
    queryMovieByRelation, queryMovieByScore, queryMovieBySentiment

app = Flask(__name__, static_url_path="")

keyword2Query = {
    'year': queryMovieByTime,
    'month': queryMovieByTime,
    'week': queryMovieByTime,
    'day': queryMovieByTime,
    'quater': queryMovieByTime,
    'name': queryMovieByName,
    'director': queryMovieByPeople,
    'actor': queryMovieByPeople,
    'starring': queryMovieByPeople,
    'relation': queryMovieByRelation,
    'genres': queryMovieByGenres,
    'score': queryMovieByScore,
    'sentiment': queryMovieBySentiment
}

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

@app.route('/query')
def query():
    count = 0
    result = ''
    query_map = {}
    time = 0
    for key, value in request.args.items():
        print(str(key) + ': ' + str(value))
        if key == 'season':
            query_map['quater'] = value
        else:
            query_map[key] = value
    if len(query_map) != 0:
        result, count, time = keyword2Query[list(query_map.keys())[0]](query_map)
    return {
        'count': count,
        'result': result,
        'time': time
    }


if __name__ == '__main__':
    app.run()
