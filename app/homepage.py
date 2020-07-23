import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from navbar import Navbar
from app_player import display_shot_charts

nav = Navbar()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.config.suppress_callback_exceptions = True
display_type = ''

# body = dbc.Container(
#     [   html.Br(),
#         dbc.Row(
#             [
#                 dbc.Col(
#                     [
#                         html.H2("What is NBA Analysis?"),
#                         dcc.Markdown(
#                             """
#                             I'm great wahahahahahhaaaa

#                             Test Test Test TestTest Teeeeeeeeeeeeeeeeeest Test 
#                             TestTest TestTest TestTest TestTest Test

#                             newline test
#                             """),
#                     ],
#                     md=4,),

#                 dbc.Col(
#                     [
#                         html.H2("Graph"),
#                         dcc.Graph(id='hexbin')
#                     ]),
#                 ]
#             )
#         ],
# className="mt-4",
# )
 
# body2 = dbc.Container([
#     html.Br(),
    
#     html.Div(
#         dbc.Row([
#             dbc.Col(
#                 id='forna-control-tabs',
#                 className='control-tabs',
#                 children=[
#                     dcc.Tabs(id='forna-tabs', value='what-is', children=[
#                         dcc.Tab(
#                             label='About',
#                             value='what-is',
#                             children=html.Div(className='control-tab', children=[
#                                 html.H4(className='what-is', children='What is FornaContainer?'),
#                                 dcc.Markdown('''
#                                 I'm great wahahahahahhaaaa

#                                 Test Test Test TestTest Teeeeeeeeeeeeeeeeeest Test 
#                                 TestTest TestTest TestTest TestTest Test

#                                 newline test
                             
#                                 ''')
#                             ])
#                         ),

#                         dcc.Tab(
#                             label='Shot chart example',
#                             value='add-sequence',
#                             children=html.Div(className='control-tab', children=[
#                                 html.Div(
#                                     title='Enter a string and a x.',
#                                     children=[
#                                         dcc.Input(
#                                             id='forna-structure',
#                                             placeholder='structure'
#                                         ),

#                                         html.Br(),

#                                     ]
#                                 ),
#                             ]))
#                     ])]),

#                         dbc.Col(
#                         [
#                             html.H2("Graph"),
#                             dcc.Graph(id='hexbin')
#                         ]),
                    
#         ])),
#  ] )

#  css 
slideshow_container = {
  'maxWidth': 1000,
  'position': 'relative',
  'margin': 'auto',
}


body3 = dbc.Container(
    [   html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [   html.Br(),
                    
                        html.H2("What is NBA Analysis?"),
                        dcc.Markdown(
                            """
                            Analytics is a key factor in the modern NBA. Many teams have adopted analytics 
                            to change the way they play and scout. The introduction of analytics in sports has 
                            led to teams valuing play that is seen as more efficient and taking shots with the highest rate 
                            of return. Spatial analysis in the NBA is a fairly new field as opposed to more traditional 
                            statistics tracking and even advanced analytics. This does not mean that the information necessary 
                            for this analysis is not available, in fact the NBA has been tracking shot location data since 1997 
                            and recently it has become more accurate with video tracking technologies.

                            """),],
                    md=4,),

                dbc.Col(
                    [
                        html.Div([
                            # shot chart
                            html.Div(dcc.Graph(id='homne_graph')),

                            #Next and previous buttons 
                            html.Div([
                                dbc.Button('<', id='previous', n_clicks=0, outline=True, color="dark"),
                                dbc.Button('>', id='next', n_clicks=0, outline=True, color="dark"),
                            ], style = {'display': 'flex',  'justifyContent': 'center', 'justifyContent': 'center'}),
     
                        ],style=slideshow_container),
                   
                        
                    ]),
                ]
            )
        ]

)



def Homepage():
    return html.Div([
        nav,
        body3,
        ])



app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Homepage()





if __name__ == "__main__":
    app.run_server()