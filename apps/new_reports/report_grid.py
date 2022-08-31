from dash import html, dcc, Input, Output, State, MATCH, dash_table
import dash_bootstrap_components as dbc
from daisie.apps import DaisieApp
from daisie.core.presentation.components.Helpbutton import Helper 
from daisie.core.misc import read_config_for_oauth
from flask_login import current_user
import pandas as pd
import plotly.express as px
from daisie.core.database.db import db_alchemy

from ..helper.downloads import HelperDownload

class ReportGrid(DaisieApp):
    def __init__(self, id, title, login=True, **kwargs):
        self.login = login
        if self.login:
            from daisie.core.authentification.routes.oauth_google import create_request_url as google_cru
            from daisie.core.authentification.routes.oauth_github import create_request_url as github_cru
            from daisie.core.authentification.routes.oauth_linked import create_request_url as linkedin_cru
            self.google_cru = google_cru
            self.github_cru = github_cru
            self.linkedin_cru = linkedin_cru

            self.display_google, self.display_github, self.display_linkedin = read_config_for_oauth()

        self.eu_countries = "Belgien, Bulgarien, Dänemark, Deutschland, Estland, Finnland, Frankreich, Griechenland, Irland, Italien, Kroatien, Lettland, Litauen, Luxemburg, Malta, Niederlande, Österreich, Polen, Portugal, Rumänien, Schweden, Slowakei, Slowenien, Spanien, Tschechische Republik, Ungarn, Zypern".split(", ")
        self.daisie_main = kwargs.get('daisie_main')
        self.db_engine = db_alchemy('database').get_engine()
        try: 
            self.df = pd.read_sql_table('v_mart_artikelverkauf', con=self.db_engine, schema='dwh')
        except Exception as e:
            print('No Database for the data available \nCSV file will be used \n' + str(e))
            import os
            filepath = os.getcwd() + "/apps/new_reports/data/v_mart_artikelverkauf.csv"
            self.df = pd.read_csv(filepath)
            self.df=self.df.rename(columns={
                "Menge": 'Anzahl', 
                "Preis": "Umsatz in EUR", 
                "Artikelbeschreibung": "Name", 
                "Land": "Land", 
            })
            self.df['datum']= pd.to_datetime(self.df["datum"])
            
        self.df=self.df.rename(columns={
                "fakt_anzahl_artikel": 'Anzahl', 
                "fakt_preis_artikel": "Umsatz in EUR", 
                "artikelbeschreibung": "Name", 
                "name_land": "Land", 
                "datum": "Datum"
            })

        self.df = self.df[["Name", "Land", "Datum", "Anzahl", "Umsatz in EUR"]]
        self.countries = list(set(self.df['Land'].values.tolist()))

        super().__init__(id=id, title=title, **kwargs)
        

    def set_content(self):
        if self.login:
            if current_user is not None and current_user.is_authenticated:
                return self.report_content()
            else:
                return self.login_content()
        else:
            return self.report_content()
            

    def plot_content(self):
        return dcc.Graph(id={'type':self.id + 'plot','index': '1'}, 
                        config={
                            "displaylogo": False,
                            'watermark' : False,
                            "locale": "de"
                        })


    def table_content(self):
        return html.Div( children=[
            html.Br(),
            html.Div(id={'type':self.id + 'table','index': '1'}),
            html.Br()
            ])

    def kpi_content(self):
        return html.Div(
                children=[
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Toast(
                                        [
                                            html.P(children=[
                                                self.df["Umsatz in EUR"].sum()
                                            ],id={'type':self.id +'Umsatz','index': '1'}, className="mb-0")
                                        ],
                                        header="Umsatz in EUR",
                                        style={"marginBottom": ".75rem"}
                                    ),
                                    # html.Br(),
                                    dbc.Toast(
                                        [
                                            html.P(children=[
                                                self.df["Umsatz in EUR"].mean()
                                                ],
                                                id={'type':self.id +'durch_Umsatz','index':'1'}, 
                                                className="mb-0"
                                            )
                                        ],
                                        header="Durschnittlicher Umsatz in EUR",
                                        style={"marginBottom": ".75rem"}
                                    ),
                                    # html.Br(),
                                    dbc.Toast(
                                        [
                                        html.P(children=[
                                            self.df["Anzahl"].sum()
                                        ],
                                        id={'type':self.id +'zahl','index': '1'}, className="mb-0")
                                        ],
                                        header="Anzahl der verkauften Artikel",
                                    ),
                                ],
                            width=3
                            )
                        ],
                        justify="center"
                    ),
                    html.Br()
                ]
            )

    def download_content(self):
        return html.Div(
                children=[
                    html.Br(),
                    dbc.Row([
                        dbc.Col(
                            [
                                dbc.Alert(
                                    "Bitte wählen Sie mindestens eine Darstellungsform zum Download aus!", 
                                    id={"type": self.id+"download-alert", "index": "1"}, 
                                    color="danger", 
                                    is_open=False,
                                    fade=True,
                                    duration=4000
                                )
                            ]
                        )
                    ], justify = "center"),
                    html.Br(),
                    # dbc.Row(
                    #     [
                    #         dbc.Col(
                    #             [
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Checklist(
                                                    options=[
                                                        {"label": "Grafik", "value": 'plot'},
                                                        {"label": "Tabelle", "value": 'table'},
                                                        {"label": "KPIs", "value": 'kpi'},
                                                    ],
                                                    value=["plot", "table", "kpi"],
                                                    id={'type':self.id + "download_select", 'index': '1'},
                                                    className="custom-checkbox"
                                                ),
                                                width=2
                                            )
                                        ],
                                        justify="center"
                                    ),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                id={'type':self.id + "excel-download",'index': '1'},
                                                title="Download der Daten als Excel",
                                                target="_blank",
                                                download="Download.xlsx",
                                                children=[
                                                    html.I(className="fa fa-file-excel", style={"marginRight": "5px"}), 
                                                    "Download der Analyse"
                                                ],
                                                
                                            )],
                                            width=3
                                        ),
                                    ], justify="center"
                                    ),
                                    html.Br()
                                ]
                #             width=6
                #             )
                #         ],
                #         justify="center"
                #     )
                # ]
            )


    def report_content(self):
        return html.Div(
                    [   
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(dcc.Dropdown(["EU", "Non-EU"], ["EU", "Non-EU"], multi=True, id={'type':self.id + "eu_dropdown", 'index': '1'}, placeholder="Wählen Sie EU, Non-EU oder beides.")),
                                dbc.Col(Helper.help_button(
                                        id=self.id+"help",
                                        popover_header='EU oder Non-EU',
                                        popover_body="Bitte wählen Sie EU, Non-EU oder beides aus.",
                                        title="Information EU Dropdown"
                                        ),
                                        align="center"
                                    )
                            ]),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(dcc.Dropdown(self.countries, self.countries[0], multi=True, id={'type':self.id + "countries_dropdown", 'index': '1'}, placeholder="Wählen Sie ein Land aus.")),
                                dbc.Col(Helper.help_button(
                                        id=self.id+"help+spec",
                                        popover_header='Länder',
                                        popover_body="Bitte wählen Sie die gewünschten Länder aus.",
                                        title="Information Länder Dropdown"
                                        ),
                                        align="center"
                                    )
                            ]),
                        html.Br(),
                        dbc.Spinner(html.Div(id={'type': self.id+"loading-output",'index': '1'}), color="secondary"),
                        dbc.Tabs(
                            [
                                dbc.Tab(self.plot_content(), label='Grafik', tab_id=self.id+"tab-plot"),
                                dbc.Tab(self.table_content(), label='Tabelle', tab_id=self.id+"tab-table"),
                                dbc.Tab(self.kpi_content(), label='KPI', tab_id=self.id+"tab-kpi"),
                                dbc.Tab(self.download_content(), label="Download", tab_id=self.id+"tab-download")
                            ],
                            id={'type': self.id+"tabs",'index': '1'},
                            active_tab=self.id+"tab-plot"
                        ),
                    ]
                )

    def login_content(self):
        request_uri_google = self.google_cru(self.daisie_main)
        request_uri_github = self.github_cru(self.daisie_main)
        request_uri_linkedin = self.linkedin_cru(self.daisie_main)



        google_row = dbc.Row([
                                dbc.Col(
                                    dbc.Button(
                                            children=[
                                                html.I(className="fa-brands fa-google"),
                                                html.Span("Google Login", style={"marginLeft": "1ex"})
                                                ],                
                                            title="Bitte loggen Sie sich über Ihren Google Account ein.",
                                            href=request_uri_google,
                                            color="primary",
                                            outline=True,
                                            style={"width": "180px", "marginBottom": ".5rem"}
                                    ),        
                                    width=10,
                                    style={"textAlign": "center"}
                                ),        
                            ], justify="center", style=({"display": "none"} if not self.display_google else None))

        github_row = dbc.Row([ 
                                dbc.Col(
                                    dbc.Button(
                                            children=[
                                                html.I(className="fa-brands fa-linkedin"),
                                                html.Span("LinkedIn Login", style={"marginLeft": "1ex"}),
                                                ],                
                                            title="Bitte loggen Sie sich über Ihren LinkedIn Account ein.",
                                            color="primary",
                                            outline=True,
                                            href=request_uri_linkedin,
                                            style={"width": "180px", "marginBottom": ".5rem"}
                                            ),
                                    width=10,
                                    style={"textAlign": "center"}
                                ),
                            ], justify="center", style=({"display": "none"} if not self.display_github else None))

        linkedin_row = dbc.Row([
                                dbc.Col(
                                    dbc.Button(
                                            children=[
                                                html.I(className="fa-brands fa-github"),
                                                html.Span("Github Login", style={"marginLeft": "1ex"})
                                                ],                
                                            title="Bitte loggen Sie sich über Ihren Github Account ein.",
                                            color="primary",
                                            outline=True,
                                            href=request_uri_github,
                                            style={"width": "180px"}
                                    ),
                                    width=10,
                                    style={"textAlign": "center"}
                                )
                            ], justify="center", style=({"display": "none"} if not self.display_linkedin else None))

        return html.Div(
            children=[
                html.Br(),
                html.H3('Herzlich Willkommen zu Daisie.', className="text-primary"),
                html.P("Bitte loggen Sie sich über Ihren Google, LinkedIn oder Github Account ein!"),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Toast(header="Login mit OAuth", children=[
                            google_row, 
                            # html.Br(),
                            github_row, 
                            # html.Br(),
                            linkedin_row
                        ]),
                    ], width=4)
                ], justify="center")
            ])

    def register_callbacks(self):
        @self.main_app.callback(
            [
                Output({'type':self.id + "eu_dropdown", 'index': MATCH}, "disabled"),
                Output({'type':self.id + "countries_dropdown", 'index': MATCH}, "disabled")
            ],
            [
                Input({'type': self.id+"tabs",'index': MATCH}, "active_tab")
            ]
        )
        def disable_dropdowns_download_tab(at):
            if at == self.id+"tab-download":
                return True, True
            else:
                return False, False

        @self.main_app.callback(
            [
                Output({'type':self.id + "countries_dropdown", 'index': MATCH}, "options"),
                Output({'type':self.id + "countries_dropdown", 'index': MATCH}, "value")
            ],
            [
                Input({'type':self.id + "eu_dropdown", 'index': MATCH}, "value")
            ],
            [
                State({'type':self.id + "countries_dropdown", 'index': MATCH}, "value")
            ]
        )
        def disable_countries(eu_dropdown_vals, countries_vals):
            # if eu_dropdown_vals == ["EU", "Non-EU"] or eu_dropdown_vals == ["Non-EU", "EU"]:
            #     return [self.countries]
            # if eu_dropdown_vals == ["EU"]:
            #     selected_EU = list(set(self.countries).intersection(set(self.eu_countries)))
            #     return [selected_EU]
            # if eu_dropdown_vals == ["Non-EU"]:
            #     selected_Non_EU = list(set(self.countries).difference(set(self.eu_countries)))
            #     return [selected_Non_EU]
            # else:
            #     return [['Kein Land ausgewählt']]
            if countries_vals is None:
                countries_vals = []

            if len(eu_dropdown_vals) == 2:
                return [[{"label": c, "value": c} for c in sorted(self.countries)], countries_vals]
            elif eu_dropdown_vals == ["EU"]:
                return [
                    [{"label": c, "value": c, "disabled": (c not in self.eu_countries)} for c in sorted(self.countries)], 
                    [c for c in countries_vals if c in self.eu_countries]
                ]
            elif eu_dropdown_vals == ["Non-EU"]:
                return [
                    [{"label": c, "value": c, "disabled": (c in self.eu_countries)} for c in sorted(self.countries)], 
                    [c for c in countries_vals if c not in self.eu_countries]
                ]
            else:
                return [['Kein Land ausgewählt'], None]
           

        @self.main_app.callback(
            [
                Output({'type':self.id + 'table','index': MATCH}, 'children'),
                Output({'type':self.id + 'plot','index': MATCH}, "figure"),       
                Output({'type':self.id +'Umsatz','index': MATCH}, 'children'),
                Output({'type':self.id +'durch_Umsatz','index': MATCH}, 'children'),
                Output({'type':self.id +'zahl','index': MATCH}, 'children'),
                Output({'type':self.id + "excel-download",'index': MATCH}, 'href'),
                Output({'type': self.id+"loading-output",'index': MATCH}, "children")
            ],[
                Input({'type':self.id + "countries_dropdown", 'index': MATCH}, 'value'),
                Input({'type':self.id + "download_select", 'index': MATCH}, 'value'),
            ]
        )
        def create_table(countries, download_options):
            if countries is None:
                df = pd.DataFrame(columns=self.df.columns)
            else:
                if type(countries) is not list:
                    countries = [countries]
                df = self.df[self.df['Land'].isin(countries)]

            df_graphics = df.copy()
            df_graphics = df_graphics.groupby(by=["Datum", "Land"])["Umsatz in EUR"].agg('sum')
            df_graphics = df_graphics.reset_index()

            table_df = df.copy()
            if not table_df.empty:
                table_df["Datum"] = table_df["Datum"].dt.strftime("%d.%m.%Y")
                table_df["Umsatz in EUR"] = table_df["Umsatz in EUR"].apply(lambda x: f"{x:0.2f}")
                table_df["Umsatz in EUR"] = table_df["Umsatz in EUR"].apply(lambda x: x.replace(".", ","))

            umsatz = f'{round(df["Umsatz in EUR"].sum(),2)}'
            durch_Umsatz = f'{round(df["Umsatz in EUR"].mean(),2)}'
            anzahl = f'{int(df["Anzahl"].sum())}'
            umsatz = umsatz.replace(",", "_").replace(".",",").replace("_", ".")
            durch_Umsatz = durch_Umsatz.replace(",", "_").replace(".",",").replace("_", ".")
            anzahl = anzahl.replace(",", "_").replace(".",",").replace("_", ".")
            if durch_Umsatz == 'nan':
                durch_Umsatz = '0,0'
            
            fig = px.line(
                df_graphics, x="Datum", y="Umsatz in EUR", color="Land", markers=True, template="plotly_white"
            )

            kpi = { 
                'umsatz': umsatz,
                'durch_Umsatz': durch_Umsatz,
                'anzahl': anzahl
            }
            if len(download_options):
                download = HelperDownload.create_xlsx_for_download(table_df.reset_index(), fig=fig,  kpi=kpi, keys=download_options)
            else:
                download = None

            return [ 
                [
                    dash_table.DataTable(
                        table_df.to_dict('records'), 
                        [{"name": i, "id": i} for i in table_df.columns], 
                        style_as_list_view=False, 
                        style_cell={"fontFamily": "sans-serif", "fontSize": "13px", 'padding': '5px'}, 
                        style_header={"fontWeight": "bold", "textAlign": "center", "color": "var(--bs-primary)"},
                        style_cell_conditional=[
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Datum', 'Land', "Name", "Date", "Country"]
                        ],
                        style_data_conditional=[                
                            {
                                "if": {"state": "selected"}, # 'active' | 'selected'
                                "backgroundColor": "rgba(var(--bs-secondary-rgb), 0.2)",
                                "border": "1px solid var(--bs-secondary)",
                            },
                        ],
                        sort_action='native',
                        sort_mode='single'
                    )
                    # dbc.Table.from_dataframe(table_df, striped=True, bordered=True, hover=True)
                ],

                fig, 
                
                umsatz,
                durch_Umsatz,
                anzahl,

                download,

                ""
            ]
            
            
        @self.main_app.callback(
            [
                Output({"type": self.id+"download-alert", "index": MATCH}, "is_open")
            ],
            [
                Input({'type':self.id + "excel-download",'index': MATCH}, "n_clicks")
            ],
            [
                State({'type':self.id + "download_select", 'index': MATCH}, 'value'),
                State({"type": self.id+"download-alert", "index": MATCH}, "is_open"),
                
            ],
            prevent_initial_call=True)
        def no_download_alert(click, download_options, alert_state):
            if not len(download_options):
                return [not alert_state]
            else:
                return [alert_state]