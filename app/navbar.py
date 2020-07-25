import dash_bootstrap_components as dbc
import dash_html_components as html

LOGO = "assets/SpotUp.svg"

def header_colors():
    return {
        'bg_color': '#85002D',
        'font_color': 'white'
    }

def Navbar():
    navbar = dbc.Navbar(
        children=[
            html.A(
                dbc.Row([
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(html.Span("Spot-Up",style={'fontSize':'20px','display':'flex','flexWrap':'nowrap','width': 'max-content'}), className="ml-2"),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="/home",
                ),
            dbc.Col(html.Span(" ")),
            html.Div( 
                dbc.Row([
                    dbc.NavLink("Player Shot Chart ", href="/player-shot-chart",style ={'color':'white'}),
                    dbc.NavLink("Team Shot Chart", href="/team-shot-chart",style ={'color':'white'}),
                ]))
    
        ],
        
        sticky="top",
        color="black",
        dark=True,
        style ={'height':'49px'}
    )

    return navbar