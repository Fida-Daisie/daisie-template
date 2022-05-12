from dash import  html, dcc, dash_table

import dash_bootstrap_components as dbc

import numpy as np



def generate_dash_table(df, id):
    # country + Umsatz
    # category + Umsatz
    df = df.groupby(["Kategorie", "Land"]).agg(
        {'Umsatz': np.sum}).reset_index()
    df = df[["Kategorie", "Land", "Umsatz"]]
    return dash_table.DataTable(
        # style_data_conditional=full_config,
        style_cell={
            "font-family": "sans-serif",
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        columns=[{"name": i, "id": i, 'type': 'numeric',
                  'format': dash_table.Format.Format(
                      scheme=dash_table.Format.Scheme.fixed,
                      precision=2,
                      group=dash_table.Format.Group.yes,
                      groups=3,
                      group_delimiter='.',
                      decimal_delimiter=',')
                  } for i in df.columns],
        data=df.to_dict('records'),
        row_deletable=False,
        id=id + "-daisie-table"
    )


def get_common_graph_area(id, style_options, df):
    style_select = get_style_menu(id, style_options)

    table = get_table_with_heading(id, df)

    plots = get_plots(id)
    cards = get_cards(id)

    
    return html.Div(
        children = dcc.Loading(
            id=id+"loading",
            type="default",
            color= "rgb(158, 194, 75)",
            children=[
                style_select,
                table,
                html.Br(),
                cards,
                html.Br(),
                plots,
                html.Br(),
            ]),
        style={"width": "100%"}
    )

def get_style_menu(id, style_options):
    return dcc.Dropdown(
        id=id + "-style-select",
        options=style_options,
        value=style_options[0].get("value")
    )

def get_table_with_heading(id, df):
    return html.Div(
            children=[
                html.H3(
                    "Verkaufszahlen"
                ),
                html.Div(
                    children=generate_dash_table(df, id + "-dash-table"),
                    id=id + "-table-area"
                )
            ]
        )

def get_cards(id):
    card_icon = {
        "color": "white",
        "textAlign": "center",
        "fontSize": 30,
        "margin": "auto",
        "card_color": "#E1EEC5",
    }
    card1 = dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Mittlerer Umsatz je Bestellung",
                                className="card-title"),
                        html.P(None,
                               className="card-text",
                               id=id + "-card-1"
                               ),
                    ]
                ),
                style={"minWidth": 350},
            ),
            dbc.Card(
                html.Div(className="fa fa-tags",
                         style=card_icon),
                className="card-text",
                color=card_icon['card_color'],
                style={"maxWidth": 75,
                       "minWidth": 50},
            ),
        ], className="mt-4 shadow rounded-start",
    )

    card2 = dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Mittlerer Umsatz je Monat",
                                className="card-title"),
                        html.P(None,
                               className="card-text",
                               id=id + "-card-2"
                               ),
                    ]
                ),
                style={"minWidth": 350},
            ),
            dbc.Card(
                html.Div(className="fa fa-tags",
                         style=card_icon),
                className="card-text",
                color=card_icon['card_color'],
                style={"maxWidth": 75,
                       "minWidth": 50},
            ),
        ], className="mt-4 shadow rounded-start",
    )

    card3 = dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Gesamter Umsatz aktuelles Jahr",
                                className="card-title"),
                        html.P(None,
                               className="card-text",
                               id=id + "-card-3"
                               ),
                    ]
                ),
                style={"minWidth": 350},
            ),
            dbc.Card(
                html.Div(className="fa fa-tags",
                         style=card_icon),
                className="card-text",
                color=card_icon['card_color'],
                style={"maxWidth": 75,
                       "minWidth": 50},
            ),
        ], className="mt-4 shadow rounded-start",
    )
    return html.Div(children=[
        
            html.H2("Plots und KPIs (hier gelten auch je die ausgewählten Parameter)"),
            dbc.Row([
                dbc.Col([card1], width="auto", md="auto"),
                dbc.Col([card2], width="auto", md="auto"),
                dbc.Col([card3], width="auto", md="auto"),
            ],
                justify="center",
            ),
            html.Br(),
            ])

def get_plots(id):
    return html.Div(
        children=[
            html.Div(
                children=dcc.Graph(id=id + "-dash-bar-plot"),
                # id= id + "-plot-area"
            ),
            html.Br(),   
            html.Div(
                children=dcc.Graph(id=id + "-dash-bar-2-plot"),
                # id= id + "-plot-area"
            ),
            #html.Br(),
            # html.Div(
            #     children=dcc.Graph(id=id + "-dash-scatter-plot"),
            #     # id= id + "-plot-area"
            # ),
            # html.Br(),
            # html.Div(
            #     children=dcc.Graph(id=id + "-dash-scatter-2-plot"),
            #     # id= id + "-plot-area"
            # )
        ], className="rounded-start border border mt-4 shadow"
    )

def get_common_parameter_area(id, countries, categories):
    heading = html.H3("Parameterauswahl")
    country_select = html.Div(
        children=[
            html.A("Wählen Sie die gewünschten Länder aus:"),
            dcc.Dropdown(
                id=id + "-country-select",
                options=[{'label': item, 'value': item} for item in countries],
                value=countries,
                multi=True
            )
        ]
    )
    category_select = html.Div(
        children=[
            html.A("Wählen Sie die gewünschten Kategorien aus:"),
            dcc.Dropdown(
                id=id + "-category-select",
                options=[{'label': item, 'value': item}
                         for item in categories],
                value=categories[:1],
                multi=True
            )
        ]
    )

    parameter_area = html.Div(
        children=[
            heading,
            html.Br(),
            country_select,
            html.Br(),
            category_select,
        ],
    )
    return parameter_area
