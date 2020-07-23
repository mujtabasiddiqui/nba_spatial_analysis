import dash_bootstrap_components as dbc

def header_colors():
    return {
        'bg_color': '#85002D',
        'font_color': 'white'
    }

def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Player Shot Chart ", href="/player-shot-chart")),
            dbc.NavItem(dbc.NavLink("Team Shot Chart", href="/team-shot-chart")),
            # dbc.DropdownMenu(
            #     nav=True,
            #     in_navbar=True,
            #     label="Menu",
            #     children=[
            #         dbc.DropdownMenuItem("Entry 1"),
            #         dbc.DropdownMenuItem("Entry 2"),
            #         dbc.DropdownMenuItem(divider=True),
            #         dbc.DropdownMenuItem("Entry 3"),
            #             ],
            #         ),
                ],
        brand="Home",
        brand_href="/home",
        sticky="top",
        color="black",
        dark=True,
    )

    return navbar