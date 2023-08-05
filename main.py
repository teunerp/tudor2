import plotly.graph_objects as go
import pandas as pd
import folium
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import dash
# import seaborn as sns
from dash import dcc
from dash import Dash, dcc, dash_table, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import pickle


df_races = pd.read_excel("C:/Users/teunv/Dropbox (Personal)/2024/TT analysis/TT_info.xlsx")
options2 = [{'label': x, 'value': x}
           for x in sorted(df_races["Races"].unique())]

# riders = pd.read_excel("C:/Users/teunv/Dropbox (Personal)/teun1/2024/TT analysis/TT_info.xlsx", "Riders")
# print(riders)
# print(options2)
# print(type(options2))
#
# # race = "Norway"
# file_path = "C://Users//teunv//Dropbox (Personal)//teun1//2024//TT analysis//Norway.pickle"
# with open(file_path, 'rb') as file:
#     # Load the data from the pickle file
#     data = pickle.load(file)
# print(data)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )


# Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
# ************************************************************************
app.layout = dbc.Container([
   dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='races', multi=False, searchable=True, placeholder="select race",
                         options=[{'label' : x, 'value': x}
                                   for x in sorted(df_races["Races"].unique())],
# [[j for j in range(5)] for i in range(5)]
                         value ='',
                         )
        ],  width={'size': 2},),

       dbc.Col([
           dcc.Dropdown(id='rider', multi=True, searchable=True, placeholder="select riders",
                        # options=[{'label' : x, 'value': x}
                        #           for x in sorted(df_ridersdata["Lastname"].unique())],
                        # [[j for j in range(5)] for i in range(5)]
                        #                          options="",
                        #                          value ='',
                        )
       ], width={'size': 3}, ),
       ]),


dbc.Row([
        dbc.Col([
            dcc.RangeSlider(
                id='slider',
                # marks={i: '{}'.format(i) for i in range(0,int(maxdistance),5)},
                step=0.1,
                min=0,
                value=[0, 2],


            )

        ]
        ),
    ]),

dbc.Row([
        dbc.Col([
            dcc.Graph(id='fig1', figure={})
        ], width={'size': 4, 'offset': 0},

        ),

    dbc.Col([
        dcc.Graph(id='fig2', figure={})
    ], width={'size': 6, 'offset': 0},

    ),

dbc.Col([
    dash_table.DataTable (
        id="datatable",
        editable=True

                      )

                          # data = df_ridersdata.to_dict('records'))
                          # row_deletable="True")


], width={'size': 1, 'offset': 0})



        ]),

dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='para1', multi=False, searchable=True, placeholder="select parameter",
                         value ='watts',
                        options=[{'label' : 'watts', 'value': 'watts'},
                                  {'label' : 'speed', 'value': 'kph'},
                                  {'label' : 'watts/kg', 'value': 'watts/kg'},

                                 ]
                         )
        ],  width={'size': 2},),

       dbc.Col([
           dcc.Dropdown(id='para2', multi=False, searchable=True, placeholder="select parameter",
                     value ='watts/kg',
                    options=[{'label' : 'watts', 'value': 'watts'},
                                  {'label' : 'speed', 'value': 'kph'}]
                        )
       ], width={'size': 2}, ),
       ]),

dbc.Row([
        dbc.Col([
            dcc.Graph(id='fig3', figure={})
        ], width={'size': 4, 'offset': 0},

        ),

    dbc.Col([
        dcc.Graph(id='fig4', figure={})
    ], width={'size': 6, 'offset': 0},

    ),
    dbc.Col([
        dash_table.DataTable (
            id="datatable2"
              )

            ], width={'size': 2, 'offset': 0}),



]),

    dcc.Store(id='stored-racedata', data=[], storage_type='memory'),
    dcc.Store(id='stored-ridersdata', data=[], storage_type='memory'),

    ], fluid=True)


@app.callback(
    [Output('rider', 'options'),
     Output("slider", "marks"),
     Output("slider", "max"),
     Output('stored-racedata', 'data'),
     Output('stored-ridersdata', 'data'),
     Output('slider', 'value'),
     Output('datatable', 'data'),
     Output('datatable', 'columns')],
    [Input('races', 'value')])

def build_graph(race):
    file_path = f"C://Users//teunv//Dropbox (Personal)//2024//TT analysis//{race}.pickle"
    with open(file_path, 'rb') as file:
        # Load the data from the pickle file
        racedata = pickle.load(file)

    options = [{'label': x, 'value': x}
               for x in sorted(racedata["rider"].unique())]

    maxdistance = racedata["km"].max()*2
    marks = {i: str(i/2) for i in range(0, int(maxdistance * 2) + 1)}

    ridersdata = pd.read_excel("C:/Users/teunv/Dropbox (Personal)/2024/TT analysis/TT_info.xlsx", 'Riders')
    dfcolumns = racedata.columns
    racedata.reset_index(inplace=True)
    racedata = racedata.to_dict('records')
    columns = [{"name": i, "id": i} for i in ridersdata.columns]

    ridersdata = ridersdata.to_dict('records')
    slidervalue = [0, maxdistance]




    return (options, marks, maxdistance, racedata, ridersdata, slidervalue, ridersdata, columns)


@app.callback(
    [Output('fig1', 'figure'),
     Output("fig2", 'figure'),
     Output("fig3", 'figure'),
     Output("fig4", 'figure'),
     Output('datatable2', 'data')],
    [Input('slider', 'value'),
     Input('datatable', 'data'),
     Input('stored-racedata', 'data'),
     Input('rider', 'value'),
     Input('para1', 'value'),
     Input('para2', 'value')])

def build_graph(slider, ridersdata, racedata, riders, para1, para2):

    print(para1)
    racedata = pd.DataFrame(racedata)
    racedata.set_index('index', inplace=True)

    df_filt_riders = racedata[racedata['rider'].isin(riders)]

    fastest = riders[0]
    ridersdata = pd.DataFrame (ridersdata)


    for index, row in ridersdata.iterrows():       # maakt watts/kg or watts/cp etc
        bmass = int(row['BW'])
        name = row['Name']
        df_filt_riders.loc[df_filt_riders['rider'] == name, 'watts/kg'] = df_filt_riders.loc[df_filt_riders['rider'] == name, 'watts'] / bmass


    # from here data is chosen by sliders
    analyseddata = df_filt_riders[(df_filt_riders["km"] > slider[0]/2) & (df_filt_riders["km"] < slider[1]/2)]
    min_secs_per_rider = analyseddata.groupby('rider')['secs'].min()
    print(min_secs_per_rider)
    # Step 2: Subtract the minimum 'secs' value from each row for the corresponding rider
    analyseddata['secs_difference'] = analyseddata.apply(lambda row: row['secs'] - min_secs_per_rider[row['rider']], axis=1)

    print(analyseddata)

    for rider in riders:
        analyseddata.loc[analyseddata['rider'] == rider, 'timediff'] = analyseddata.loc[analyseddata['rider'] == rider, 'secs_difference'] - analyseddata.loc[analyseddata['rider'] == fastest, 'secs_difference']


    fig1 = px.scatter_mapbox(analyseddata, lat="lat", lon="lon", color="rider", # display maps
                            color_continuous_scale=px.colors.cyclical.IceFire, zoom=12,
                            mapbox_style="open-street-map")
    fig1.update_layout(showlegend=False)

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])

    dfalt = analyseddata[analyseddata["rider"] == riders[0]]

    ymin = dfalt["alt"].min()
    ymax = dfalt["alt"].max()

    fig2.add_trace(
        go.Scatter(x=dfalt["km"], y=dfalt["alt"], stackgroup='one', opacity=0, name="alt",
                   line=dict(width=1, color='rgb(224, 224, 224)')
                   ),
        secondary_y=False,
    )

    fig3.add_trace(
        go.Scatter(x=dfalt["km"], y=dfalt["alt"], stackgroup='one', opacity=0, name="alt",
                   line=dict(width=1, color='rgb(224, 224, 224)')
                   ),
        secondary_y=False,
    )

    fig4.add_trace(
        go.Scatter(x=dfalt["km"], y=dfalt["alt"], stackgroup='one', opacity=0, name="alit",
                   line=dict(width=1, color='rgb(224, 224, 224)')
                   ),
        secondary_y=False,
    )

    for rider in riders:
        print(rider)
        dfnew = analyseddata[analyseddata["rider"] == rider]

        fig2.add_trace(
            go.Scatter(x=dfnew["km"], y=dfnew["timediff"], name=rider),
            secondary_y=True,
        )

        fig3.add_trace(
        go.Scatter(x=dfnew["km"], y=dfnew[para1], name=rider),
        secondary_y=True,
        )

        fig4.add_trace(
            go.Scatter(x=dfnew["km"], y=dfnew[para2], name=rider),
            secondary_y=True,
        )

    fig2.update_layout(
        template='simple_white', showlegend=False,
        yaxis_range=[ymin-10, ymax+10],
    )

    fig2.update_yaxes(
        title_text="time losses",

        secondary_y=True)

    fig3.update_layout(
        template='simple_white', showlegend=True,
        yaxis_range=[ymin-10, ymax+10])

    fig4.update_layout(
        template='simple_white', showlegend=False,
        yaxis_range=[ymin-10, ymax+10])

    df_results = analyseddata.groupby('rider').agg({'watts': ['max'],'kph': ['mean'],'watts/kg': ['mean'],"timediff": "last"}).round(1)

    df_results.columns = df_results.columns.droplevel()
    df_results.reset_index(inplace=True)
    df_results.columns = ["test", "test1", "test2","test3",'test5']
    print(df_results)
    datatable2 = df_results.to_dict('records')
    return (fig1, fig2, fig3, fig4, datatable2)




if __name__ == '__main__':
    app.run_server(debug=False)