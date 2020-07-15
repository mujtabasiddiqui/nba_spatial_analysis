##### Imports #########
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np 
from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import teamyearbyyearstats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats as st

def get_teams_list():
    teams_dict_lst = teams.get_teams()
    team_lst = [{'label': team_dict['full_name'], 'value': team_dict['id']} for team_dict in teams_dict_lst]

    return team_lst

def get_team_shotchartdetail(team_id, season_id, season_type):   
    # shotchartdetail endpoint
    shotchartlist = shotchartdetail.ShotChartDetail(team_id=int(team_id), 
                                                   player_id=0, 
                                                   season_type_all_star=season_type, 
                                                   season_nullable=season_id,
                                                   context_measure_simple="FGA").get_data_frames()
    
    return shotchartlist[0], shotchartlist[1]

def draw_plotly_court(fig, fig_width=600, margins=10, layer='below'):
    
    # From: https://community.plot.ly/t/arc-shape-with-path/7205/5
    def ellipse_arc(x_center=0.0, y_center=0.0, a=10.5, b=10.5, start_angle=0.0, end_angle=2 * np.pi, N=200, closed=False):
        t = np.linspace(start_angle, end_angle, N)
        x = x_center + a * np.cos(t)
        y = y_center + b * np.sin(t)
        path = f'M {x[0]}, {y[0]}'
        for k in range(1, len(t)):
            path += f'L{x[k]}, {y[k]}'
        if closed:
            path += ' Z'
        return path

    fig_height = fig_width * (470 + 2 * margins) / (500 + 2 * margins)
    fig.update_layout(width=fig_width, height=fig_height)

    # Set axes ranges
    fig.update_xaxes(range=[-250 - margins, 250 + margins])
    fig.update_yaxes(range=[-52.5 - margins, 417.5 + margins])

    threept_break_y = 89.47765084
    three_line_col = "#777777"
    main_line_col = "#777777"

    fig.update_layout(
        # Line Horizontal
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        shapes=[
            dict(
                type="rect", x0=-250, y0=-52.5, x1=250, y1=417.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer=layer
            ),
            dict(
                type="rect", x0=-80, y0=-52.5, x1=80, y1=137.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer=layer
            ),
            dict(
                type="rect", x0=-60, y0=-52.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer=layer
            ),
            dict(
                type="circle", x0=-60, y0=77.5, x1=60, y1=197.5, xref="x", yref="y",
                line=dict(color=main_line_col, width=1),
                # fillcolor='#dddddd',
                layer=layer
            ),
            dict(
                type="line", x0=-60, y0=137.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=1),
                layer=layer
            ),

            dict(
                type="rect", x0=-2, y0=-7.25, x1=2, y1=-12.5,
                line=dict(color="#ec7607", width=1),
                fillcolor='#ec7607',
            ),
            dict(
                type="circle", x0=-7.5, y0=-7.5, x1=7.5, y1=7.5, xref="x", yref="y",
                line=dict(color="#ec7607", width=1),
            ),
            dict(
                type="line", x0=-30, y0=-12.5, x1=30, y1=-12.5,
                line=dict(color="#ec7607", width=1),
            ),

            dict(type="path",
                 path=ellipse_arc(a=40, b=40, start_angle=0, end_angle=np.pi),
                 line=dict(color=main_line_col, width=1), layer=layer),
            dict(type="path",
                 path=ellipse_arc(a=237.5, b=237.5, start_angle=0.386283101, end_angle=np.pi - 0.386283101),
                 line=dict(color=main_line_col, width=1), layer=layer),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer=layer
            ),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer=layer
            ),
            dict(
                type="line", x0=220, y0=-52.5, x1=220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer=layer
            ),

            dict(
                type="line", x0=-250, y0=227.5, x1=-220, y1=227.5,
                line=dict(color=main_line_col, width=1), layer=layer
            ),
            dict(
                type="line", x0=250, y0=227.5, x1=220, y1=227.5,
                line=dict(color=main_line_col, width=1), layer=layer
            ),
            dict(
                type="line", x0=-90, y0=17.5, x1=-80, y1=17.5,
                line=dict(color=main_line_col, width=1), layer=layer
            ),
            dict(
                type="line", x0=-90, y0=27.5, x1=-80, y1=27.5,
                line=dict(color=main_line_col, width=1), layer=layer
            ),
            dict(
                type="line", x0=-90, y0=57.5, x1=-80, y1=57.5,
                line=dict(color=main_line_col, width=1), layer=layer
            ),
            dict(
                type="line", x0=-90, y0=87.5, x1=-80, y1=87.5,
                line=dict(color=main_line_col, width=1), layer=layer
            ),
            dict(
                type="line", x0=90, y0=17.5, x1=80, y1=17.5,
                line=dict(color=main_line_col, width=1), layer=layer
            ),
            dict(
                type="line", x0=90, y0=27.5, x1=80, y1=27.5,
                line=dict(color=main_line_col, width=1), layer=layer
            ),
            dict(
                type="line", x0=90, y0=57.5, x1=80, y1=57.5,
                line=dict(color=main_line_col, width=1), layer=layer
            ),
            dict(
                type="line", x0=90, y0=87.5, x1=80, y1=87.5,
                line=dict(color=main_line_col, width=1), layer=layer
            ),

            dict(type="path",
                 path=ellipse_arc(y_center=417.5, a=60, b=60, start_angle=-0, end_angle=-np.pi),
                 line=dict(color=main_line_col, width=1), layer=layer),

        ]
    )
    return True

def make_shot_chart (fig, shots_df, name, season_id):
    '''
    params: fig-plotly graph object Figure, shots_df-DataFrame of shotchartdetail, name-name of team, season_id-year of season
    param-type: fig-plotly graph object Figure, shots_df- pandas DataFrame, name-string, season_id-string
    '''
    fig.add_trace(go.Scatter(
        x=shots_df[shots_df['SHOT_MADE_FLAG']==0]['LOC_X'],
        y=shots_df[shots_df['SHOT_MADE_FLAG']==0]['LOC_Y'],
        mode='markers', name='Miss',
        marker=dict(size=5,color='red',line=dict(width=1, color='#333333'), symbol='x')
    ))
    fig.add_trace(go.Scatter(
        x=shots_df[shots_df['SHOT_MADE_FLAG']==1]['LOC_X'],
        y=shots_df[shots_df['SHOT_MADE_FLAG']==1]['LOC_Y'],
        mode='markers', name='Make',
        marker=dict(size=5,color='green',line=dict(width=1, color='#333333'), symbol='circle')
    ))
    fig.update_layout(
        title={
            'text': f"{name} {season_id} Shot Chart",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

def make_heatmap(fig, shots_df, name, season_id):
    cubehelix_cs=[[0.0, '#ffffff'],[0.16666666666666666, '#edcfc9'],[0.3333333333333333, '#daa2ac'],[0.5, '#bc7897'],
    [0.6666666666666666, '#925684'],[0.8333333333333333, '#5f3868'],[1.0, '#2d1e3e']]

    fig.add_trace(go.Histogram2dContour(
        x = shots_df['LOC_X'],
        y = shots_df['LOC_Y'],
        colorscale=cubehelix_cs,
        contours=dict(showlines=False)))

    fig.update_layout(
        title={
            'text': f"{name} {season_id} Shot Heatmap",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

def make_team_hexbin(fig, shots_df,name,season_id):
    Hex = plt.hexbin(x=shots_df['LOC_X'], y=shots_df['LOC_Y'],gridsize=25,vmin = 0.0, vmax = 0.7,
    cmap=plt.get_cmap('YlOrRd'), mincnt=10)

    HexC = plt.hexbin(x=shots_df['LOC_X'], y=shots_df['LOC_Y'], C=shots_df['SHOT_MADE_FLAG'],gridsize=25,vmin = 0.0, vmax = 0.7, 
    cmap=plt.get_cmap('YlOrRd'), mincnt=9)

    loc = HexC.get_offsets()
    acc = HexC.get_array()
    shots = Hex.get_array()

    xlocs = []
    ylocs = []
    accs_by_hex = []
    shots_by_hex = []

    for i in range(len(loc)):
        xlocs.append(loc[i][0])
        ylocs.append(loc[i][1])
        accs_by_hex.append(acc[i])
        shots_by_hex.append(shots[i])

#freq is % of total shots
    freq_by_hex= list(map(lambda x: x/len(shots_df), shots_by_hex))

    hexbin_text = [
        '<i>Accuracy: </i>' + str(round(accs_by_hex[i]*100, 1)) + '%<BR>'
        '<i>Frequency: </i>' + str(round(freq_by_hex[i]*100, 2)) + '%'
        for i in range(len(freq_by_hex))
    ]

    fig.add_trace(go.Scatter(x=xlocs, y=ylocs, mode='markers', name='markers', 
                        marker=dict(size=freq_by_hex, sizemode='area', sizeref= 2. * max(freq_by_hex) / (18. ** 2), 
                                    sizemin=4.5,color=accs_by_hex, colorscale='YlOrRd',line=dict(width=1, color='#333333'),
                                    colorbar=dict(thickness=15, x=0.84,y=0.87, yanchor='middle',len=0.2,
                                                    title=dict(text="<B>Accuracy</B>",font=dict(size=11,color='#4d4d4d'))),
                                    symbol='hexagon'), text=hexbin_text, hoverinfo='text'))

    fig.update_layout(
        title={
            'text': f"{name} {season_id} Shot Heatmap",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})


####### Dash Layout ###########
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        #Search Bars
        html.Div([
            dcc.Dropdown(
                id='team',
                options=get_teams_list(),
                value=1610612737
            )
        ],
        style={'width': '32%', 'float': 'left', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='season',
                value='2018-19'
            ),
        ],style={'width': '32%', 'float': 'center', 'display': 'inline-block','padding-left': '2%'}),

        html.Div([
            dcc.Dropdown(
                id='season_type',
                options=[
                    {'label': 'Regular Season', 'value': 'Regular Season'},
                    {'label': 'Playoffs', 'value': 'Playoffs'}
                ],
                value='Regular Season'
            )
        ],
        style={'width': '32%', 'float': 'right', 'display': 'inline-block'})
        
    ]),

    #Shot Chart Tabs
    dcc.Tabs([
        dcc.Tab(label='Shot Chart', children=[
            dcc.Graph(id='shot_chart')
        ]),
        dcc.Tab(label='Heatmap', children=[
            dcc.Graph(id='heatmap')
        ]),
        dcc.Tab(label='Hexbin', children=[
            dcc.Graph(id='hexbin')
        ]),
    ],style={'width': '55%', 'float': 'left', 'display': 'inline-block'})
])

###### Callback Dash Functions ##########
@app.callback(
    Output('season', 'options'),
    [Input('team','value')]
)
def get_active_seasons(selected_team):
    # career df
    career_df = teamyearbyyearstats.TeamYearByYearStats(team_id=selected_team).get_data_frames()[0]
    #List of active seasons
    season_lst = [{'label': season, 'value': season} for season in career_df['YEAR']]

    return season_lst

@app.callback(
    [Output('shot_chart', 'figure'),
    Output('heatmap', 'figure'),
    Output('hexbin', 'figure')],
    [Input('team', 'value'),
    Input('season', 'value'),
    Input('season_type', 'value')]
)
def display_shot_charts(team, season, season_type):
    shots_df,league_avg = get_team_shotchartdetail(team, season, season_type)
    name = teams.find_team_name_by_id(team)['full_name']
    
    shot_fig = go.Figure()
    heat_fig = go.Figure()
    hex_fig = go.Figure()

    if int(season[:4]) >= 1996 :
        make_shot_chart(shot_fig,shots_df, name, season)
        draw_plotly_court(shot_fig)
            
        make_heatmap(heat_fig,shots_df,name,season)
        draw_plotly_court(heat_fig, layer='above')
            
        make_team_hexbin(hex_fig,shots_df,name,season)
        draw_plotly_court(hex_fig)
    else:
        draw_plotly_court(shot_fig)
        shot_fig.update_layout(
            title={
                'text': 'No Shot Chart Data',
                'y':0.98,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

        draw_plotly_court(heat_fig)
        heat_fig.update_layout(
            title={
                'text': 'No Shot Chart Data',
                'y':0.98,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
        
        draw_plotly_court(hex_fig)
        hex_fig.update_layout(
            title={
                'text': 'No Shot Chart Data',
                'y':0.98,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'}) 
    return shot_fig, heat_fig, hex_fig


#### Run ###
if __name__ == '__main__':
    app.run_server(debug=True)