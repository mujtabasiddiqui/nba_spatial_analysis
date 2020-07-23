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
from nba_api.stats.endpoints import commonplayerinfo
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats as st
import requests
from datetime import date

## Navbar
from navbar import Navbar
nav = Navbar()

####### Analysis, Visualization, Data Pull Functions ############
def get_players_list():
    player_dict_lst = players.get_players()
    player_lst = [{'label': player_dict['full_name'], 'value': player_dict['id']} for player_dict in player_dict_lst]
    
    return player_lst
    
def get_player_shotchartdetail(player, season_id, season_type):
    # career df
    career_df = playercareerstats.PlayerCareerStats(player_id=player).get_data_frames()[0]
    
    # team id during the season
    team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']
    
    # shotchardtdetail endpoint
    shotchartlist = shotchartdetail.ShotChartDetail(team_id=int(team_id), 
                                                   player_id=int(player), 
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
    params: fig-plotly graph object Figure, shots_df-DataFrame of shotchartdetail, name-name of player/team, season_id-year of season
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

def make_hexbin(fig, shots_df,league_avg,in_type,name,season_id):
    grid_size= 40 
    min_show = max(2, round(len(shots_df)* 0.001)) # min count for shots in hex
    
    x_loc = []
    y_loc = []
    y_limit = 300

    for y in range(len(shots_df['LOC_Y'])):
        if shots_df['LOC_Y'][y] < y_limit:
            y_loc.append(shots_df['LOC_Y'][y])
            x_loc.append(shots_df['LOC_X'][y])
    
    
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

    if in_type == 'p':
        hexbin_text = [
            '<i>Legue FG: </i>' + str(round(la_accs_by_hex[i]*100, 1)) + '%<BR>'
            '<i>Player FG: </i>' + str(round(accs_by_hex[i]*100, 1)) + '%<BR>'
            '<i>Difference: </i>' + str(round(diff_by_hex[i]*100, 1)) + '%<BR>'
            '<i>Frequency: </i>' + str(round(freq_by_hex[i]*100, 2)) + '%'
            for i in range(len(freq_by_hex))
        ]
        
    elif in_type == 't':
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
                                    colorbar=dict(thickness=15, x=0.84,y=0.87, yanchor='middle',len=0.2,
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

def player_app():
    return html.Div([
        nav,
        #Search Bars
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='player',
                    options=get_players_list(),
                    value=202695
                )
            ],
            style={'width': '32%', 'float': 'left', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='season',
                    value='2018-19'
                ),
            ],style={'width': '32%', 'float': 'center', 'display': 'inline-block','paddingLeft': '2%'}),

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

        #Shot Charts and Top Left Info
        html.Div(children=[
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
            ]),

            html.Div(children='''Shot Chart Data Not Available For Seasons Prior to 1996-97*''',style={'color': 'red'}) 
        ],style={'width': '45%', 'float': 'left', 'display': 'inline-block'}),

        #Player Stats Top Right
        html.Div(children=[

            
            html.Div([
                html.Div([
                    html.Img(id='player_img', style={'width': '30%','paddingLeft': '2%', 'display': 'inline-block', 'float': 'left', 'height': '100%'}),

                    html.Table([
                        html.Tbody([
                            html.Tr([
                                html.Td(id='timeframe', style={'border': '1px solid white','color': 'white'}, colSpan=4)
                            ]),

                            html.Tr([
                                html.Td(id='player_pts', style={'border': '1px solid white','color': 'white'}),
                                html.Td(id='player_reb', style={'border': '1px solid white','color': 'white'}),
                                html.Td(id='player_ast', style={'border': '1px solid white','color': 'white'}),
                                html.Td(id='player_pie', style={'border': '1px solid white','color': 'white'}),
                            ])
                        ])
                    ])
                ]),
                
                html.Div([
                    html.H3(id='player_name', style={'color':'white'}),
                    html.Img(id='team_logo', style={'width':'5%'}),
                    html.Div(id='player_team_pos', style={'display': 'inline-block', 'paddingLeft': '2%', 'color': 'white'})
                ]),

                html.Table([
                    html.Tbody([
                        html.Tr([
                            html.Td(id='player_ht', style={'border': '1px solid white','color': 'white'}),
                            html.Td(id='player_wt', style={'border': '1px solid white','color': 'white'}),
                            html.Td(id='player_prior', style={'border': '1px solid white','color': 'white', 'border-right': 'None'}, colSpan=2),
                        ]),

                        html.Tr([
                            html.Td(id='player_age', style={'border': '1px solid white','color': 'white', 'border-bottom': 'None'}),
                            html.Td(id='player_born', style={'border': '1px solid white','color': 'white', 'border-bottom': 'None'}),
                            html.Td(id='player_draft', style={'border': '1px solid white','color': 'white', 'border-bottom': 'None'}),
                            html.Td(id='player_exp', style={'border': '1px solid white','color': 'white', 'border-right': 'None', 'border-bottom': 'None'})
                        ])
                    ])
                ], style={'height':'50%'})
            ], style={'width': '60%','paddingLeft': '2%', 'display': 'inline-block', 'float': 'right'})

        ],style={'width': '50%', 'float': 'right', 'display': 'inline-block','background': '#1975FA', 'border-radius':'5px'})
    ])

###### Callback Dash Functions ##########
@app.callback(
    Output('season', 'options'),
    [Input('player','value')]
)
def get_active_seasons(selected_player):
    # career df
    career_df = playercareerstats.PlayerCareerStats(player_id=selected_player).get_data_frames()[0]
    #List of active seasons
    season_lst = [{'label': season, 'value': season} for season in career_df['SEASON_ID']]

    return season_lst


def display_shot_charts(player, season, season_type):
    shots_df,league_avg = get_player_shotchartdetail(player,season,season_type)
    name = players.find_player_by_id(player)['full_name']
    
    shot_fig = go.Figure()
    heat_fig = go.Figure()
    hex_fig = go.Figure()

    if int(season[:4]) >= 1996 :
        make_shot_chart(shot_fig,shots_df, name, season)
        draw_plotly_court(shot_fig)
        
        make_heatmap(heat_fig,shots_df,name,season)
        draw_plotly_court(heat_fig, layer='above')
        
        make_hexbin(hex_fig,shots_df,league_avg,'p',name,season)
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


def get_player_img(player):
    url = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player}.png'
    r = requests.head(url)
    if r.status_code == 200:
        return url
    else:
        return 'https://stats.nba.com/media/img/league/nba-headshot-fallback.png'


def get_player_common_info(player):
    player_info = commonplayerinfo.CommonPlayerInfo(player).get_data_frames()[0]
    name = player_info['DISPLAY_FIRST_LAST'][0]
    prior = 'Prior: ' + player_info['LAST_AFFILIATION'][0]
    height = 'Height: '+player_info['HEIGHT'][0]
    weight = 'Weight: '+player_info['WEIGHT'][0] + 'lbs'
    exp = 'Exp: ' + str(player_info['SEASON_EXP'][0])
    jersey = '#' + player_info['JERSEY'][0] + ' '
    team = ' | ' + player_info['TEAM_CITY'][0]+' '+player_info['TEAM_NAME'][0]
    position = player_info['POSITION'][0]
    abrv = player_info['TEAM_ABBREVIATION'][0]
    team_logo= f'https://stats.nba.com/media/img/teams/logos/{abrv}_logo.svg'
    birthDate=date(int(player_info['BIRTHDATE'][0][0:4]),int(player_info['BIRTHDATE'][0][5:7]),int(player_info['BIRTHDATE'][0][8:10]))
    today=date.today()
    age = 'Age: ' + str(today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)))
    born = 'Born: ' + player_info['BIRTHDATE'][0][5:7]+'/'+player_info['BIRTHDATE'][0][8:10]+'/'+player_info['BIRTHDATE'][0][0:4]
    draft ='Drafted: ' + player_info['DRAFT_YEAR'][0]+' Rnd '+player_info['DRAFT_ROUND'][0]+' Pick '+player_info['DRAFT_NUMBER'][0]

    player_stats = commonplayerinfo.CommonPlayerInfo(player).get_data_frames()[1]
    timeframe = player_stats['TimeFrame'][0].capitalize() + ' Stats'
    if list(player_stats.columns)[-1] == 'PIE':
        pie = 'PIE: ' + str(player_stats['PIE'][0])
    else:
        pie = 'All Star: ' + str(player_stats['ALL_STAR_APPEARANCES'][0])
    pts = 'PTS: ' + str(player_stats['PTS'][0])
    reb = 'REB: ' + str(player_stats['PTS'][0])
    ast = 'AST: ' + str(player_stats['AST'][0])
    
    return [jersey,name], height, weight, prior, age, born, draft, exp, [position,team], team_logo, timeframe, pts, reb, ast, pie

#### Run ###
if __name__ == '__main__':
    app.run_server(debug=True)