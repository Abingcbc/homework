import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_daq as daq
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data = pd.read_csv('lab3-datasets/google-play-store-apps/googleplaystore2.csv')

category = list(data['Category'].value_counts().index)
category.append('ALL')
category = sorted(category)
install_map_number = {
    '1,000,000+': 1000000,
    '10,000,000+': 10000000,
    '100,000+': 100000,
    '10,000+': 10000,
    '1,000+': 1000,
    '5,000,000+': 5000000,
    '100+': 100,
    '500,000+': 500000,
    '50,000+': 50000,
    '5,000+': 5000,
    '100,000,000+': 100000000,
    '10+': 10,
    '500+': 500,
    '50,000,000+': 50000000,
    '50+': 50,
    '5+': 5,
    '500,000,000+': 500000000,
    '1+': 1,
    '1,000,000,000+': 1000000000,
    '0+': 0,
    '0': 0
}
cat_dic = {}
for cat in category:
    cat_dic[cat] = np.sum([install_map_number[count] for count in data[data['Category'] == cat]['Installs'].values])

content_list = ['Everyone', 'Teen', 'Mature 17+',
                'Everyone 10+', 'Adults only 18+', 'Unrated']
genres_list = ['Tools', 'Entertainment', 'Education', 'Medical',
               'Business', 'Productivity', 'Sports', 'Personalization',
               'Communication', 'Lifestyle', 'Finance', 'Action', 'Health & Fitness',
               'Photography', 'Social', 'News & Magazines', 'Shopping',
               'Travel & Local', 'Dating', 'Books & Reference', 'Arcade',
               'Simulation', 'Casual', 'Video Players & Editors', 'Puzzle',
               'Maps & Navigation', 'Food & Drink', 'Role Playing', 'Strategy',
               'Racing', 'House & Home', 'Auto & Vehicles', 'Libraries & Demo',
               'Weather', 'Adventure', 'Events', 'Comics', 'Art & Design',
               'Beauty', 'Card', 'Parenting', 'Board', 'Educational',
               'Casino', 'Trivia', 'Pretend Play', 'Word', 'Music & Video',
               'Music', 'Action & Adventure', 'Brain Games', 'Creativity', 'Music & Audio']
rating_split = {
    0: data[data['Rating'] == 0],
    1: data[data['Rating'] <= 1],
    2: data[(data['Rating'] <= 2) & (data['Rating'] > 1)],
    3: data[(data['Rating'] <= 3) & (data['Rating'] > 2)],
    4: data[(data['Rating'] <= 4) & (data['Rating'] > 3)],
    5: data[(data['Rating'] <= 5) & (data['Rating'] > 4)]
}

tabs_styles = {
    'height': '44px'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

scores = [4.186066567847999,4.233487084870849,4.123427331887202,4.257178841309823,
       4.3, 4.1,4.044704264099038,4.114244186046512,4.281504702194357,
       4.176276276276279,4.119063545150502,4.212968299711816,4.2335616438356185,
       4.323443223443224,4.1408783783783765,4.074558303886923,4.132601880877745,
       4.281407035175879,4.281040892193307,4.184999999999998,4.304705882352941,
       4.12,4.239037433155084,4.108181818181817,4.1,4.349342105263158,
       4.283333333333335,4.1401360544217685,4.203181818181819,4.0641791044776125,
       4.385714285714286,4.057024793388429,4.147,4.208108108108108,4.086666666666667,
       4.216304347826089,4.185135135135136,4.1887323943661965,4.178461538461538,
       4.229577464788731,4.254814814814817,4.411111111111113,4.344,
       4.337704918032785,4.287179487179485,4.074999999999999,4.285416666666666,
       4.268518518518519,4.158620689655175,4.1,4.133333333333334,4.239772727272728,
       4.437500000000001,4.26111111111111,4.238461538461537,4.289523809523812,
       4.362318840579711,4.311111111111112,4.3,4.5,4.070165745856353,
       4.181481481481482,4.533333333333334,4.3,4.050000000000001,4.14,
       4.403571428571429,4.320833333333333,4.416666666666667,4.074999999999999,
       4.276687116564414,4.276470588235294,4.291666666666667,4.30188679245283,
       4.216129032258065,4.339583333333333,4.0600000000000005,3.5999999999999996,
       4.3050000000000015,4.40625,4.2525,4.029166666666666,4.0874999999999995,
       4.418181818181818,4.4,4.414285714285714,4.297916666666666,4.309374999999999,
       4.314285714285714,4.65,4.2,4.45,4.1968749999999995,4.542857142857144,
       4.031818181818181,4.466666666666666,4.0,4.114285714285714,4.7,4.5,
       3.8538461538461535,4.297142857142857,3.4750000000000005,4.2,4.3,3.7,
       4.186486486486487,4.5,4.466666666666666,4.6,4.285714285714286,
       4.5,4.311111111111112,4.255555555555556,4.305769230769231,4.385714285714286,
       4.38,4.122727272727271,4.307692307692308,4.266666666666667,4.6,
       3.975977653631286,4.166666666666667,4.05,4.13,3.4,3.65,2.7,
       4.333333333333333,4.300000000000001,3.9200000000000004,4.7,4.316666666666666,
       3.771428571428571,4.5,4.1,4.6,4.05,4.1,3.973333333333333,4.3533333333333335,
       4.3875,3.6,4.336363636363638,4.380000000000001,3.8400000000000007,
       4.351898734177215,3.983333333333333,4.1,4.079687500000001,
       4.459999999999999,4.3358974358974365,4.3,4.2176470588235295,
       4.1000000000000005,4.325,4.3,4.290322580645161,4.334146341463415,
       4.09,4.3,4.4,4.368421052631579,4.5,4.45,4.7,4.3,
       4.666666666666667,3.8000000000000003,4.8,4.7,4.118181818181818,4.166666666666667,
       4.406666666666666,4.5,4.199999999999999,4.1]

app.layout = html.Div([
    html.Div(children=[
        html.H1('Dashboard -- Google Play Store'),
        html.H3('1753837 陈柄畅'),
        html.P('Tab one is about the relation between column '
               '\'Category\' and \'Installs\'. '
               'Tab two is about the relation between column '
               '\'Rating\', \'Content Rating\' and \'Genres\'.\n\n'),
        html.H2('Hope this can help you more or less!\n\n')
    ], style={'textAlign': 'center',
              'background-image': 'url("assets/bg.png")',
              'background-size': 'cover'}),
    html.Div([
        dcc.Tabs(id='main', children=[
            dcc.Tab(label='Category&Installs', children=[
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='category_selected',
                            options=[{'label': c, 'value': c} for c in category],
                            value=['ALL'],
                            multi=True,
                            placeholder='Default all'
                        ),
                        dcc.Graph(
                            id='apps-count-bar'
                        )
                    ], style={'width': '48%', 'display': 'inline-block', 'margin-top': '20px'}),
                    html.Div([
                        daq.ToggleSwitch(
                            id='average_or_all',
                            value=False,
                            label='Average ----- All',
                            labelPosition='bottom'
                        ),
                        dcc.Graph(
                            id='installs-count-pie'
                        )
                    ], style={'width': '48%', 'display': 'inline-block', 'float': 'right', 'margin-top': '20px'})
                ])
            ], style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Rating&Content Rating&Genres', children=[
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='rating-content-line'
                        ),
                        html.P(id='content'),
                        dcc.RangeSlider(
                            id='rating-slider',
                            min=0,
                            max=5,
                            marks={
                                0: '0',
                                1: '1',
                                2: '2',
                                3: '3',
                                4: '4',
                                5: '5'
                            },
                            value=[0, 5],
                            step=1
                        )
                    ], style={'width': '48%', 'display': 'inline-block', 'margin-left': '10px'}),
                    html.Div([
                        daq.Gauge(
                            id='rating-gauge',
                            showCurrentValue=True,
                            value=0,
                            max=5,
                            min=0,
                            label='Average rating of Apps in specified type(Content Rating& Genres)'
                        ),
                        dcc.Graph(
                            id='content-genres-sunburst',
                            figure=go.Figure(
                                [go.Sunburst(
                                    ids=[str(num) for num in range(1, 178)],
                                    labels=['Everyone',
                                            'Teen',
                                            'Mature 17+',
                                            'Everyone 10+',
                                            'Adults only 18+',
                                            'Unrated',
                                            'Tools',
                                            'Entertainment',
                                            'Education',
                                            'Medical',
                                            'Business',
                                            'Productivity',
                                            'Sports',
                                            'Personalization',
                                            'Communication',
                                            'Lifestyle',
                                            'Finance',
                                            'Action',
                                            'Health & Fitness',
                                            'Photography',
                                            'Social',
                                            'News & Magazines',
                                            'Shopping',
                                            'Travel & Local',
                                            'Dating',
                                            'Books & Reference',
                                            'Arcade',
                                            'Simulation',
                                            'Casual',
                                            'Video Players & Editors',
                                            'Puzzle',
                                            'Maps & Navigation',
                                            'Food & Drink',
                                            'Role Playing',
                                            'Strategy',
                                            'Racing',
                                            'House & Home',
                                            'Auto & Vehicles',
                                            'Libraries & Demo',
                                            'Weather',
                                            'Adventure',
                                            'Events',
                                            'Comics',
                                            'Art & Design',
                                            'Beauty',
                                            'Card',
                                            'Parenting',
                                            'Board',
                                            'Educational',
                                            'Casino',
                                            'Trivia',
                                            'Pretend Play',
                                            'Word',
                                            'Music & Video',
                                            'Music',
                                            'Action & Adventure',
                                            'Brain Games',
                                            'Creativity',
                                            'Music & Audio',
                                            'Tools',
                                            'Entertainment',
                                            'Education',
                                            'Medical',
                                            'Business',
                                            'Productivity',
                                            'Sports',
                                            'Personalization',
                                            'Communication',
                                            'Lifestyle',
                                            'Finance',
                                            'Action',
                                            'Health & Fitness',
                                            'Photography',
                                            'Social',
                                            'News & Magazines',
                                            'Shopping',
                                            'Travel & Local',
                                            'Dating',
                                            'Books & Reference',
                                            'Arcade',
                                            'Simulation',
                                            'Casual',
                                            'Video Players & Editors',
                                            'Puzzle',
                                            'Maps & Navigation',
                                            'Food & Drink',
                                            'Role Playing',
                                            'Strategy',
                                            'Racing',
                                            'House & Home',
                                            'Auto & Vehicles',
                                            'Weather',
                                            'Adventure',
                                            'Events',
                                            'Comics',
                                            'Art & Design',
                                            'Beauty',
                                            'Card',
                                            'Parenting',
                                            'Board',
                                            'Educational',
                                            'Casino',
                                            'Trivia',
                                            'Word',
                                            'Music',
                                            'Tools',
                                            'Entertainment',
                                            'Education',
                                            'Medical',
                                            'Productivity',
                                            'Sports',
                                            'Personalization',
                                            'Communication',
                                            'Lifestyle',
                                            'Action',
                                            'Health & Fitness',
                                            'Photography',
                                            'Social',
                                            'News & Magazines',
                                            'Shopping',
                                            'Travel & Local',
                                            'Dating',
                                            'Books & Reference',
                                            'Arcade',
                                            'Simulation',
                                            'Casual',
                                            'Video Players & Editors',
                                            'Maps & Navigation',
                                            'Role Playing',
                                            'Strategy',
                                            'Racing',
                                            'Weather',
                                            'Adventure',
                                            'Comics',
                                            'Beauty',
                                            'Card',
                                            'Parenting',
                                            'Word',
                                            'Music',
                                            'Entertainment',
                                            'Education',
                                            'Medical',
                                            'Productivity',
                                            'Sports',
                                            'Personalization',
                                            'Lifestyle',
                                            'Action',
                                            'Health & Fitness',
                                            'Social',
                                            'News & Magazines',
                                            'Books & Reference',
                                            'Arcade',
                                            'Simulation',
                                            'Casual',
                                            'Video Players & Editors',
                                            'Puzzle',
                                            'Food & Drink',
                                            'Role Playing',
                                            'Strategy',
                                            'Racing',
                                            'Auto & Vehicles',
                                            'Weather',
                                            'Adventure',
                                            'Events',
                                            'Comics',
                                            'Art & Design',
                                            'Card',
                                            'Board',
                                            'Educational',
                                            'Pretend Play',
                                            'Word',
                                            'Music & Video',
                                            'Music',
                                            'Action & Adventure',
                                            'Sports',
                                            'Comics',
                                            'Tools'],
                                    parents=['',
                                             '',
                                             '',
                                             '',
                                             '',
                                             '',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '1',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '2',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '3',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '4',
                                             '5',
                                             '5',
                                             '6'],
                                    outsidetextfont={"size": 20, "color": "#377eb8"},
                                    leaf={"opacity": 0.4},
                                    marker={"line": {"width": 2}}
                                )],
                                go.Layout(
                                    margin=go.layout.Margin(t=0, l=0, r=0, b=0),
                                    sunburstcolorway=["#636efa", "#ef553b", "#00cc96"],
                                    hovermode='closest'
                                )
                            )
                        )
                    ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
                ])
            ], style=tab_style, selected_style=tab_selected_style)
        ], style=tabs_styles)
    ], style={'margin-top': '0px'}),
])


@app.callback(
    Output('apps-count-bar', 'figure'),
    [Input('category_selected', 'value')]
)
def update_apps_count_bar(category_list):
    sorted_categories = sorted(category_list)
    if len(sorted_categories) == 0:
        sorted_categories.append('ALL')
    if sorted_categories[0] == 'ALL':
        return {
            'data': [
                go.Bar(
                    x=category[1:],
                    y=[data['Category'].value_counts()[c] for c in category[1:]]
                )
            ],
            'layout': go.Layout(
                xaxis={
                    'title': 'Category',
                    'titlefont': {'color': 'black', 'size': 14},
                    'tickfont': {'size': 9, 'color': 'black'}
                },
                yaxis={
                    'title': 'App Number',
                    'titlefont': {'color': 'black', 'size': 14, },
                    'tickfont': {'color': 'black'}
                },
                margin={'l': 50, 'b': 200, 't': 100, 'r': 0},
                hovermode='closest',
                title='The number of Apps of each category'
            )
        }
    else:
        return {
            'data': [
                go.Bar(
                    x=category_list,
                    y=[data['Category'].value_counts()[c] for c in sorted_categories]
                )
            ],
            'layout': go.Layout(
                xaxis={
                    'title': 'Category',
                    'titlefont': {'color': 'black', 'size': 14},
                    'tickfont': {'size': 9, 'color': 'black'}
                },
                yaxis={
                    'title': 'App Number',
                    'titlefont': {'color': 'black', 'size': 14, },
                    'tickfont': {'color': 'black'}
                },
                margin={'l': 50, 'b': 200, 't': 100, 'r': 0},
                hovermode='closest',
                title='The number of Apps of each category'
            )
        }


@app.callback(
    Output('installs-count-pie', 'figure'),
    [Input('average_or_all', 'value'),
     Input('category_selected', 'value')]
)
def update_average_or_all(average_all, category_list):
    sorted_categories = sorted(category_list)
    if len(sorted_categories) == 0:
        sorted_categories.append('ALL')
    if average_all:
        if sorted_categories[0] == 'ALL':
            return {
                'data': [go.Pie(
                    labels=category[1:],
                    values=[cat_dic[c] for c in category[1:]],
                    hoverinfo='label+percent+value',
                    textinfo='none'
                )],
                'layout': {
                    'title': 'Install number',
                    'height': 450
                }
            }
        else:
            return {
                'data': [go.Pie(
                    labels=sorted_categories,
                    values=[cat_dic[c] for c in sorted_categories],
                    hoverinfo='label+percent+value',
                    textinfo='none'
                )],
                'layout': {
                    'title': 'Install number',
                    'height': 450
                }
            }
    else:
        if sorted_categories[0] == 'ALL':
            return {
                'data': [go.Pie(
                    labels=category[1:],
                    values=[int(cat_dic[c] / data['Category'].value_counts()[c]) for c in category[1:]],
                    hoverinfo='label+percent+value',
                    textinfo='none'
                )],
                'layout': {
                    'title': 'Install number'
                }
            }
        else:
            return {
                'data': [go.Pie(
                    labels=sorted_categories,
                    values=[int(cat_dic[c] / data['Category'].value_counts()[c]) for c in sorted_categories],
                    hoverinfo='label+percent+value',
                    textinfo='none'
                )],
                'layout': {
                    'title': 'Install number'
                }
            }


@app.callback(
    Output('rating-content-line', 'figure'),
    [Input('rating-slider', 'value')]
)
def update_rating_content_line(rates):
    return {
        'data': [
            dict(
                name=content_list[0],
                x=[num for num in range(rates[0], rates[1] + 1)],
                y=[len(rating_split[num][rating_split[num]['Content Rating'] == content_list[0]]) for num in
                   range(rates[0], rates[1] + 1)],
                hoverinfo='x+y',
                line=dict(width=0.5),
                stackgroup='one'
            ),
            dict(
                name=content_list[1],
                x=[num for num in range(rates[0], rates[1] + 1)],
                y=[len(rating_split[num][rating_split[num]['Content Rating'] == content_list[1]]) for num in
                   range(rates[0], rates[1] + 1)],
                hoverinfo='x+y',
                line=dict(width=0.5),
                stackgroup='one'
            ),
            dict(
                name=content_list[2],
                x=[num for num in range(rates[0], rates[1] + 1)],
                y=[len(rating_split[num][rating_split[num]['Content Rating'] == content_list[2]]) for num in
                   range(rates[0], rates[1] + 1)],
                hoverinfo='x+y',
                line=dict(width=0.5),
                stackgroup='one'
            ),
            dict(
                name=content_list[3],
                x=[num for num in range(rates[0], rates[1] + 1)],
                y=[len(rating_split[num][rating_split[num]['Content Rating'] == content_list[3]]) for num in
                   range(rates[0], rates[1] + 1)],
                hoverinfo='x+y',
                line=dict(width=0.5),
                stackgroup='one'
            ),
            dict(
                name=content_list[4],
                x=[num for num in range(rates[0], rates[1] + 1)],
                y=[len(rating_split[num][rating_split[num]['Content Rating'] == content_list[4]]) for num in
                   range(rates[0], rates[1] + 1)],
                hoverinfo='x+y',
                line=dict(width=0.5),
                stackgroup='one'
            ),
            dict(
                name=content_list[5],
                x=[num for num in range(rates[0], rates[1] + 1)],
                y=[len(rating_split[num][rating_split[num]['Content Rating'] == content_list[5]]) for num in
                   range(rates[0], rates[1] + 1)],
                hoverinfo='x+y',
                line=dict(width=0.5),
                stackgroup='one'
            )
        ],
        'layout': {
            'title': 'The number of Apps of different content in each rating interval'
        }
    }


@app.callback(
    Output('rating-gauge', 'value'),
    [Input('content-genres-sunburst', 'hoverData')]
)
def update_content_genres_sunburst(hoverData):
    if hoverData is None:
        return 0
    else:
        print(hoverData)
        return scores[hoverData['points'][0]['pointNumber']]


if __name__ == '__main__':
    app.run_server()
