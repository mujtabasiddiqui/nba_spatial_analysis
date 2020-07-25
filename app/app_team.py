##### Imports #########
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np 
from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import teamyearbyyearstats
from nba_api.stats.endpoints import teaminfocommon
from nba_api.stats.endpoints import teamdetails
from nba_api.stats.endpoints import teamdashlineups
from nba_api.stats.endpoints import commonteamroster

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats as st

## Navbar
from navbar import Navbar
nav = Navbar()

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
    limit = 400
    make_df = shots_df.loc[shots_df['SHOT_MADE_FLAG']==1, ['LOC_X','LOC_Y']]
    make_x_df = make_df[make_df['LOC_Y']<limit]['LOC_X']
    make_y_df = make_df[make_df['LOC_Y']<limit]['LOC_Y']
    miss_df = shots_df.loc[shots_df['SHOT_MADE_FLAG']==0, ['LOC_X','LOC_Y']]
    miss_x_df = miss_df[miss_df['LOC_Y']<limit]['LOC_X']
    miss_y_df = miss_df[miss_df['LOC_Y']<limit]['LOC_Y']

    fig.add_trace(go.Scatter(
        x=miss_x_df,
        y=miss_y_df,
        mode='markers', name='Miss',
        marker=dict(size=5,color='red',line=dict(width=1, color='#333333'), symbol='x')
    ))
    fig.add_trace(go.Scatter(
        x=make_x_df,
        y=make_y_df,
        mode='markers', name='Make',
        marker=dict(size=5,color='green',line=dict(width=1, color='#333333'), symbol='circle')
    ))
    fig.update_layout(
        title={
            'text': f"{name} {season_id} Shot Chart",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        legend=dict(x=0.80,y=0.94,
            bordercolor="black",
            bgcolor="LightSteelBlue",
            borderwidth=0.5))

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

def make_team_hexbin(fig, shots_df,league_avg,name,season_id):
    grid_size= 40
    min_show = max(2, round(len(shots_df)* 0.001)) # min count for shots in hex
    
    y_limit = 400
    xy = shots_df.loc[shots_df['LOC_Y']< y_limit, ['LOC_X','LOC_Y']]
    x_loc = xy['LOC_X']
    y_loc = xy['LOC_Y']
    
    Hex = plt.hexbin(x=x_loc, y=y_loc,gridsize=grid_size,vmin = 0.0, vmax = 0.7,
    cmap=plt.get_cmap('YlOrRd'), mincnt= min_show + 1)

    # join shotchart with legue average
    la_fg_pct = shots_df.merge(league_avg, on=['SHOT_ZONE_BASIC','SHOT_ZONE_AREA','SHOT_ZONE_RANGE'], how='left')

    # Make hex distribution of the legue average FG % 
    HexL = plt.hexbin(x=x_loc, y=y_loc, C=la_fg_pct['FG_PCT'],gridsize=grid_size, vmin = 0.0, vmax = 0.7, 
    cmap=plt.get_cmap('YlOrRd'), mincnt=min_show)

    # Make hex distribution of the palyer FG % 
    HexC = plt.hexbin(x=x_loc, y=y_loc, C=shots_df['SHOT_MADE_FLAG'],gridsize=grid_size, vmin = 0.0, vmax = 0.7, 
    cmap=plt.get_cmap('YlOrRd'), mincnt=min_show)

    # Extract data from hexbins
    loc = HexC.get_offsets()
    acc = HexC.get_array()
    la_acc = HexL.get_array()
    shots = Hex.get_array()

    xlocs = []
    ylocs = []
    accs_by_hex = []
    la_accs_by_hex = []
    diff_by_hex = []
    shots_by_hex = []
    hex_size = []

    for i in range(len(loc)):
        xlocs.append(loc[i][0])
        ylocs.append(loc[i][1])
        accs_by_hex.append(acc[i])
        la_accs_by_hex.append(la_acc[i])
        diff_by_hex.append(acc[i] - la_acc[i])
        shots_by_hex.append(shots[i])

    #freq is % of total shots
    freq_by_hex = list(map(lambda x: x/len(shots_df), shots_by_hex))
    hex_size = list(map(lambda x: x * 4, freq_by_hex))


    hexbin_text = [
        '<i>Legue FG: </i>' + str(round(la_accs_by_hex[i]*100, 1)) + '%<BR>'
        '<i>Team FG: </i>' + str(round(accs_by_hex[i]*100, 1)) + '%<BR>'
        '<i>Difference: </i>' + str(round(diff_by_hex[i]*100, 1)) + '%<BR>'
        '<i>Frequency: </i>' + str(round(freq_by_hex[i]*100, 2)) + '%'
        for i in range(len(freq_by_hex))
    ]

        
    max_val = max(diff_by_hex) - max(diff_by_hex) * 0.2
    min_val = min(diff_by_hex)
    fig.add_trace(go.Scatter(x=xlocs, y=ylocs, mode='markers', name='markers', 
                        marker=dict(size=freq_by_hex, sizemode='area', sizeref= 2. * max(freq_by_hex) / (12. ** 2), 
                                    sizemin=3.,color=diff_by_hex, colorscale="RdYlBu",line=dict(width=1, color='black'),reversescale=True,
                                    colorbar=dict(thickness=15, x=0.80,y=0.87, yanchor='middle',len=0.2,
                                                    title=dict(text="<B>vs League Avg</B>",font=dict(size=10,color='black')),
                                                    tickvals=[max_val, 0, min_val], 
                                                    ticktext=["Better", "On par", "Worse"]),
                                    symbol='hexagon'), text=hexbin_text, hoverinfo='text'))

    fig.update_layout(
        title={
            'text': f"{name} {season_id} Hex Shot Map",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
         font=dict(color="black"))


####### Dash Layout ###########
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 
                        'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.scripts.append_script({'external_url': 'https://code.jquery.com/jquery-3.5.1.slim.min.js'})
app.scripts.append_script({'external_url': 'https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js'})
app.scripts.append_script({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js'})

tb_center = {
    'display': 'flex',
    'justifyContent': 'center',
}
tb_big_center = {
    'display': 'flex',
    'fontSize': '40px',
    'justifyContent': 'center',
}

def team_app():
    return html.Div([
        nav,
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

        html.Div(children=[
            #Shot Chart Tabs
            dcc.Tabs([
                dcc.Tab(label='Shot Chart', children=[
                    dcc.Graph(id='team_shot_chart')
                ]),
                dcc.Tab(label='Heatmap', children=[
                    dcc.Graph(id='team_heatmap')
                ]),
                dcc.Tab(label='Hexbin', children=[
                    dcc.Graph(id='team_hexbin')
                ]),
            ]),

            html.Div(children='''Shot Chart Data Not Available For Seasons Prior to 1996-97*''',
            style={'color': 'red', 'paddingLeft': '38px', 'zIndex': '9', 'position': 'absolute','marginTop': '-24px'}) 
        ],style={'width': '45%', 'float': 'left', 'display': 'inline-block'}),

        #Team profile Top Right
        html.Div(children=[
            html.Div([
                html.Div([
                    html.Img(id='team_img', style={'width': '40%','display': 'inline-block', 'float': 'left', 'height': '100%'}),
                ]),
                
                html.Div([
                    html.H3(id='team_name', style={'color':'white'}),
                    html.Div(id='team_city', style={'display': 'inline-block', 'paddingLeft': '2%', 'color': 'white'})
                ]),

                html.Table([
                    html.Tbody([
                        html.Tr([
                            html.Td([
                                html.Div('Record:'),
                                html.Div(id='team_conf',style={'paddingLeft': '7%'}),
                                html.Div(id='team_div',style={'paddingLeft': '7%'}),
                            ],style={'border': '1px solid white','color': 'white','padding': '0 4px 0'}, colSpan=3), 
                            # html.Td(id='team_manager', style={'border': '1px solid white','color': 'white','padding': '0 4px 0'}),
                        ]),

                        html.Tr([
                            html.Td(id='team_minYear', style={'border': '1px solid white','color': 'white','padding': '0 4px 0'}),
                            html.Td(id='team_maxYear', style={'border': '1px solid white','color': 'white','padding': '0 4px 0'}),
                            html.Td(id='head_coach', style={'border': '1px solid white','color': 'white','padding': '0 4px 0'}),
                        ]),
                    ])
                ], style={'height':'50%'})
            ], style={'display': 'inline-block', 'float': 'left', "width":"92%"}),

        ],style={'margin': '2% 3% 0', "width":"49%",
                'padding': '10px 10px 10px',
                'display': 'inline-block','background': '#F0A74B', 'border-radius':'5px'},
            id='team_profile'),
    
        # team stats
        html.Div([
            html.Table([
                html.Tbody([
                    html.Tr([
                        html.Td([
                            html.Div("Team Points Per Game: "),
                            html.Div(id='team_pts',style=tb_big_center),
                            html.Div(id='team_pts_rank',style=tb_center),
                            ],
                        style={'border': '1px solid white','color': 'white','padding': '12px'}),
                        # html.Td([
                        #     html.Div("Average Field Goals Made: "),
                        #     html.Div(id='team_fgm',style=tb_big_center),
                        #     html.Div(id='team_fgm_rank',style=tb_center),],
                        # style={'border': '1px solid white','color': 'white','padding': '12px'}),
                        html.Td([
                            html.Div("Team Assists Per Game: "),
                            html.Div(id='team_ast',style=tb_big_center),
                            html.Div(id='team_ast_rank',style=tb_center),
                            ],
                        style={'border': '1px solid white','color': 'white','padding': '12px'}),                        
                    ]),
                    html.Tr([
                        html.Td([
                            html.Div("Rebound Per Game: "),
                            html.Div(id='team_reb',style=tb_big_center),
                            html.Div(id='team_reb_rank',style=tb_center),
                            ],
                        style={'border': '1px solid white','color': 'white','padding': '12px'}),
                        html.Td([
                            html.Div("Opponent points per game: "),
                            html.Div(id='team_opp_pts',style=tb_big_center),
                            html.Div(id='team_opp_pts_rank',style=tb_center),],
                        style={'border': '1px solid white','color': 'white','padding': '12px'}),
                        # html.Td([
                        #     html.Div("Game play: "),
                        #     html.Div(id='team_gp',style=tb_big_center),
                        #     html.Div(id='team_gp_rank',style=tb_center),
                        #     ],
                        # style={'border': '1px solid white','color': 'white','padding': '12px'}),                        
                    ]),
                ])
            ], style={'margin': 'auto'})
        ], style={'marginLeft': '3%', 
                'padding': '23px', "width":"49%",
                'display': 'inline-block','background': '#F0A74B', 'border-radius':'5px'}, 
            id='team_stats'),

        # team player
        html.Div([
            html.Br(),
            html.H2("Players List"),
            dash_table.DataTable(
                id='team_roster', columns=[
                    {'name': 'Season', 'id': 'SEASON'},
                    {'name': 'Player', 'id': 'PLAYER'},
                    {'name': 'Jersey number', 'id': 'NUM'},
                    {'name': 'Position', 'id': 'POSITION'},
                    {'name': 'Height', 'id': 'HEIGHT'},
                    {'name': 'Weight', 'id': 'WEIGHT'},
                    {'name': 'Birth Date', 'id': 'BIRTH_DATE'},
                    {'name': 'Age', 'id': 'AGE'},
                    {'name': 'Years Active', 'id': 'EXP'},
                    {'name': 'Drafted From', 'id': 'SCHOOL'},
                    # {'name': 'Player', 'id': 'PLAYER_ID'},
                    ]
            )
        ], style={
                'width': '95%', #Use when we show 6 team stats
                'paddingLeft': '23px',
                'display': 'inline-block', 'border-radius':'5px'}, 
            id='team_player_stats')

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


def display_team_shot_charts(team, season, season_type):
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
            
        make_team_hexbin(hex_fig,shots_df,league_avg,name,season)
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

# def get_team_img(player):
#     url = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player}.png'
#     r = requests.head(url)
#     if r.status_code == 200:
#         return url
#     else:
#         return 'https://stats.nba.com/media/img/league/nba-headshot-fallback.png'


def rank_name(rank):
    if rank % 10 == 1:
        return str(rank) + "st"
    elif rank % 10 == 2:
        return str(rank) + "nd"
    elif rank % 10 == 3:
        return str(rank) + "rd"
    else:
        return str(rank) + "th"

def get_team_common_info(team):
    team_info = teaminfocommon.TeamInfoCommon(team).get_data_frames()[0]
    team_info2 = teamdetails.TeamDetails(team).get_data_frames()[0]
    team_stats = teaminfocommon.TeamInfoCommon(team).get_data_frames()[1]
    team_players = teamdetails.TeamDetails(team).get_data_frames()[6]

    team_roster_df = commonteamroster.CommonTeamRoster(1610612737).get_data_frames()[0]
    player_columns=[{"name": i, "id": i} for i in team_roster_df.columns],
    team_roster_df = team_roster_df.loc[team_roster_df['EXP']!="R"]
    team_roster = team_roster_df.to_dict(orient='records')


    name = team_info['TEAM_NAME'][0]
    city = team_info['TEAM_CITY'][0]
    team_conf = rank_name(team_info['CONF_RANK'][0]) + ' in ' + team_info['TEAM_CONFERENCE'][0] + " Conference" 
    team_div = rank_name(team_info['DIV_RANK'][0]) + ' in ' + team_info['TEAM_DIVISION'][0] + ' Division'
    firstactive = 'Year Founded: ' + team_info['MIN_YEAR'][0]
    lastactive = 'Last Active: ' +  team_info['MAX_YEAR'][0]
    # manager = 'Manager: ' + team_info2['GENERALMANAGER'][0]
    head_coach = 'Head Coach: ' +  team_info2['HEADCOACH'][0]


    abrv = team_info['TEAM_ABBREVIATION'][0]
    team_logo = f'https://stats.nba.com/media/img/teams/logos/{abrv}_logo.svg'

    team_pts = str(team_stats['PTS_PG'][0]) 
    team_ast = str(team_stats['AST_PG'][0]) 
    # team_oreb = str(team_info['OREB'][0]) 
    # team_dreb = str(team_info['DREB'][0]) 
    team_reb = str(team_stats['REB_PG'][0]) 
    team_opp_pts = str(team_stats['OPP_PTS_PG'][0]) 
    team_pts_rank = rank_name(team_stats['PTS_RANK'][0]) 
    team_ast_rank = rank_name(team_stats['AST_RANK'][0]) 
    # team_oreb_rank = rank_name(team_info['OREB_RANK'][0]) 
    # team_dreb_rank = rank_name(team_info['DREB_RANK'][0]) 
    team_reb_rank = rank_name(team_stats['REB_RANK'][0]) 
    team_opp_pts_rank = rank_name(team_stats['OPP_PTS_RANK'][0]) 



    # ppg = team_info['PTS_PG'][0]
    # rpg = team_info['REB_PG'][0]
    # apg = team_info['AST_PG'][0]

    return name, city, team_conf, team_div, firstactive, lastactive, head_coach, team_logo, \
            team_pts, team_reb, team_ast, team_opp_pts,\
            team_pts_rank, team_reb_rank, team_ast_rank,team_opp_pts_rank, team_roster



#### Run ###
if __name__ == '__main__':
    app.run_server(debug=True)