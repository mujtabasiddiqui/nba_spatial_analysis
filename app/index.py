import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app_player import player_app, display_shot_charts, get_active_seasons, get_player_img, get_player_common_info
from app_team import team_app, display_team_shot_charts, get_team_common_info
from homepage import Homepage


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.config.suppress_callback_exceptions = True
display_type = ''

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    display_type = pathname
    if pathname == '/player-shot-chart':
        return player_app()
    if pathname == '/team-shot-chart':
        return team_app()
    else:
        return Homepage()


# @app.callback(
#     Output('season', 'options'),
#     [Input('player','value')]
# )
# def update_season(selected_player):
#     season_lst = get_active_seasons(selected_player)
#     return season_lst

@app.callback(
    [Output('shot_chart', 'figure'),
    Output('heatmap', 'figure'),
    Output('hexbin', 'figure')],
    [Input('player', 'value'),
    Input('season', 'value'),
    Input('season_type', 'value')] 
)
def update_player_graph(player, season, season_type):
    shot_fig, heat_fig, hex_fig = display_shot_charts(player, season, season_type)
    return shot_fig, heat_fig, hex_fig



@app.callback(
    [Output('team_shot_chart', 'figure'),
    Output('team_heatmap', 'figure'),
    Output('team_hexbin', 'figure')],
    [Input('team', 'value'),
    Input('season', 'value'),
    Input('season_type', 'value')]
)
def update_team_graph(team, season, season_type):
    shot_fig, heat_fig, hex_fig = display_team_shot_charts(team, season, season_type)
    return shot_fig, heat_fig, hex_fig



@app.callback(
    Output('player_img', 'src'),
    [Input('player', 'value')]
)
def update_player_img(player):
    url = get_player_img(player)
    return url


#player img
@app.callback(
    [Output('player_name', 'children'),
    Output('player_ht', 'children'),
    Output('player_wt', 'children'),
    Output('player_prior', 'children'),
    Output('player_age', 'children'),
    Output('player_born', 'children'),
    Output('player_draft', 'children'),
    Output('player_exp', 'children'),
    Output('player_team_pos', 'children'),
    Output('team_logo', 'src'),
    Output('timeframe', 'children'),
    Output('player_pts', 'children'),
    Output('player_reb', 'children'),
    Output('player_ast', 'children'),
    Output('player_pie', 'children'),],
    [Input('player', 'value')]
)
def update_player_img(player):
    return get_player_common_info(player)

#team info
@app.callback(
    [Output('team_name', 'children'),
    Output('team_city', 'children'),
    Output('team_conf', 'children'),
    Output('team_div', 'children'),
    Output('team_minYear', 'children'),
    Output('team_maxYear', 'children'),
    # Output('team_manager', 'children'),
    Output('head_coach', 'children'),
    Output('team_img', 'src'),
    Output('team_pts', 'children'),
    Output('team_reb', 'children'),
    Output('team_ast', 'children'),
    Output('team_opp_pts', 'children'),
    Output('team_pts_rank', 'children'),
    Output('team_reb_rank', 'children'),
    Output('team_ast_rank', 'children'),
    Output('team_opp_pts_rank', 'children'),
    Output('team_roster', 'data'),],
    [Input('team', 'value')]
)
def update_player_img(team):
    return get_team_common_info(team)


# homgpage graph
shot_fig, heat_fig, hex_fig = display_shot_charts(202695, "2018-19", "Regular Season")

@app.callback(
    Output('homne_graph', 'figure'),
    [Input('next', 'n_clicks'),
    Input('previous', 'n_clicks')],)
def update_homepage_slide(btn1, btn2): 
    cur_val = (btn1 - btn2) % 3

    if cur_val == 0:
        return shot_fig
    elif cur_val == 1:
        return heat_fig
    elif cur_val == 2:
        return hex_fig



if __name__ == '__main__':
    app.run_server(debug=True)