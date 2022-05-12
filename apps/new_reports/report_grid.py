from dash import html, dcc, Input, Output, State, MATCH, dash_table
import dash_bootstrap_components as dbc
from daisie.apps import DaisieApp
from daisie.core.presentation.components.Helpbutton import Helper 
from flask_login import current_user
from .common_components import get_cards
from .common_components import get_table_with_heading
import pandas as pd
import plotly_express as px
from daisie.core.export_import import OfficeDownloader
from daisie.core.database.db import db_alchemy
import requests
import numpy as np
from daisie.core.misc import config_reader
from flask import request
from ..helper.downloads import HelperDownload
import locale
class ReportGrid(DaisieApp):
    def __init__(self, id, title, is_fixed=False, **kwargs):
        self.eu_countries = "Belgien, Bulgarien, Dänemark, Deutschland, Estland, Finnland, Frankreich, Griechenland, Irland, Italien, Kroatien, Lettland, Litauen, Luxemburg, Malta, Niederlande, Österreich, Polen, Portugal, Rumänien, Schweden, Slowakei, Slowenien, Spanien, Tschechische Republik, Ungarn, Zypern".split(", ")
        self.daisie_main = kwargs.get('daisie_main')
        self.db_engine = db_alchemy('database').get_engine()
        self.df = pd.read_sql_table('v_mart_artikelverkauf', con=self.db_engine, schema='dwh')
        self.df=self.df.rename(columns={
            "fakt_anzahl_artikel": 'Anzahl', 
            "fakt_preis_artikel": "Umsatz in EUR", 
            "artikelbeschreibung": "Name", 
            "name_land": "Land", 
            "datum": "Datum"
        })
        self.df = self.df[["Name", "Land", "Datum", "Anzahl", "Umsatz in EUR"]]
        self.countries = list(set(self.df['Land'].values.tolist()))
        super().__init__(id=id, title=title, is_fixed=is_fixed, **kwargs)
        

    def set_content(self):
        if current_user is not None:
            if current_user.is_authenticated or not self.security:
                return self.report_content()
        return self.login_content()
        
        

    def plot_content(self):
        return dcc.Graph(id={'type':self.id + 'plot','index': '1'}, 
                        config={
                            "displaylogo": False,
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
                                    ),
                                    # html.Br(),
                                    dbc.Toast(
                                        [
                                        html.P(children=[
                                            self.df["Anzahl"].sum()
                                        ],
                                        id={'type':self.id +'zahl','index': '1'}, className="mb-0")
                                        ],
                                        header="Anzahl der Verkauften Artikel",
                                    ),
                                ],
                            width=3
                            )
                        ],
                        justify="center"
                    )
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
                                                children=[html.I(className="fa fa-file-excel", style={"marginRight": "5px"}), "Download der Analyse"],
                                                
                                            )],
                                            width=3
                                        ),
                                    ], justify="center")
                                ],
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
                                dbc.Col(html.Div(
                                    children=Helper.help_button(
                                        id=self.id+"help",
                                        popover_header='EU oder Non-EU',
                                        popover_body="Bitte wählen Sie EU, Non-EU oder beides aus.",
                                        title="Information EU Dropdown"
                                        )
                                    ))
                            ]),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(dcc.Dropdown(self.countries, self.countries[0], multi=True, id={'type':self.id + "countries_dropdown", 'index': '1'}, placeholder="Wählen Sie ein Land aus.")),
                                dbc.Col(html.Div(
                                    children=Helper.help_button(
                                        id=self.id+"help+spec",
                                        popover_header='Länder',
                                        popover_body="Bitte wählen Sie die gewünschten Länder aus.",
                                        title="Information Länder Dropdown"
                                        )
                                    ))
                            ]),

                        dbc.Tabs(
                            [
                                dbc.Tab(self.plot_content(), label='Grafik', id=self.id+"tab-plot"),
                                dbc.Tab(self.table_content(), label='Tabelle', id=self.id+"tab-table"),
                                dbc.Tab(self.kpi_content(), label='KPI', id=self.id+"tab-kpi"),
                                dbc.Tab(self.download_content(), label="Download", id=self.id+"tab-download")
                            ],
                            id=self.id+"tabs"
                        ),
                    ]
                )

    def login_content(self):

        config = config_reader().get_config()
        

        config = config_reader().get_config()
        open_id = config['oauth'].get('openid_configuration')
        provider_cfg=requests.get(open_id).json()
        authorization_endpoint = provider_cfg["authorization_endpoint"]
        request_uri_google = self.daisie_main.client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=config['url'].get('base_url') + config['oauth'].get('callback_url'),
        scope=["openid", "email", "profile"],
        )
        
        
        authorization_endpoint = "https://www.linkedin.com/oauth/v2/authorization"
        request_uri_linkedin = self.daisie_main.client3.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=config['url'].get('base_url') + config['oauth3'].get('callback_url'),
        scope="r_liteprofile")
        
        
        
        authorization_endpoint = "https://github.com/login/oauth/authorize"
        request_uri_github = self.daisie_main.client2.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=config['url'].get('base_url') + config['oauth2'].get('callback_url'),
        login=config['oauth2'].get('login'))
        return html.Div(
            children=[
                html.H1('Herzlich Willkommen zu Daisie Fida'),
                html.P("Bitte loggen Sie sich über Ihren Google, LinkedIn oder Github Accoun ein!"),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Toast([
                            dbc.Row([
                                dbc.Col(
                                    dbc.Button(
                                            children=[
                                                html.Img(src="assets/img/googleicon.png", className='icon_size'),
                                                "Google Sign-In",
                                                ],                
                                            title="Bitte loggen Sie sich über Ihren Google Account ein",
                                            href=request_uri_google,
                                            color="dark",
                                            outline=True,
                                            style={"width": "180px"}
                                    ),        
                                    width=8    
                                ),        
                            ], justify="center"), dbc.Row([ 
                                dbc.Col(
                                    dbc.Button(
                                            children=[
                                                html.Img(src='assets/img/linkedinicon.png', className='icon_size'),
                                                "LinkedIn Sign-In",
                                                ],                
                                            title="Bitte loggen Sie sich über Ihren LinkedIn Account ein",
                                            color="dark",
                                            outline=True,
                                            href=request_uri_linkedin,
                                            style={"width": "180px"}
                                            ),
                                    width=8
                                ),
                            ], justify="center"), dbc.Row([
                                dbc.Col(
                                    dbc.Button(
                                            children=[
                                                html.Img(src='assets/img/githubicon.png', className='icon_size'),
                                                "Github Sign-In",
                                                ],                
                                            title="Bitte loggen Sie sich über Ihren Github Account ein",
                                            color="dark",
                                            outline=True,
                                            href=request_uri_github,
                                            style={"width": "180px"}
                                    ),
                                    width=8
                                )
                            ], justify="center")
                        ], header="Sign-In mit OAuth"),
                    ], width=4)
                ], justify="center")
            ])

    def register_callbacks(self):
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
                return [[{"label": c, "value": c} for c in self.countries], countries_vals]
            elif eu_dropdown_vals == ["EU"]:
                return [
                    [{"label": c, "value": c, "disabled": (c not in self.eu_countries)} for c in self.countries], 
                    [c for c in countries_vals if c in self.eu_countries]
                ]
            elif eu_dropdown_vals == ["Non-EU"]:
                return [
                    [{"label": c, "value": c, "disabled": (c in self.eu_countries)} for c in self.countries], 
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
                Output({'type':self.id + "excel-download",'index': MATCH}, 'href')
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
                table_df["Umsatz in EUR"] = table_df["Umsatz in EUR"].apply(lambda x: f"{x:0.2f}".replace(".", ","))
            
            umsatz = f'{round(df["Umsatz in EUR"].sum(),2):_}'.replace(".",",").replace("_", ".")
            durch_Umsatz = f'{round(df["Umsatz in EUR"].mean(),2):_}'.replace(".",",").replace("_", ".")
            anzahl = f'{int(df["Anzahl"].sum()):,}'.replace(",", ".")
            if durch_Umsatz == 'nan':
                durch_Umsatz = '0,0'
            fig = px.line(df_graphics, x="Datum", y="Umsatz in EUR", color="Land", markers=True)

            kpi = { 
                'umsatz': umsatz,
                'durch_Umsatz': durch_Umsatz,
                'anzahl': anzahl
            }
            if len(download_options):
                download = HelperDownload.create_xlsx_for_download(table_df, fig=fig,  kpi=kpi, keys=download_options)
            else:
                download = None

            return [ 
                [dash_table.DataTable(
                    table_df.to_dict('records'), 
                    [{"name": i, "id": i} for i in df.columns], 
                    style_as_list_view=False, 
                    style_cell={"fontFamily": "sans-serif", "fontSize": "13px", 'padding': '5px'}, 
                    style_header={"fontWeight": "bold", "textAlign": "center"},
                    style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['Datum', 'Land', "Name"]
                    ],
                    sort_action='native',
                    sort_mode='single'
                )],

                fig, 
                
                umsatz,
                durch_Umsatz,
                anzahl,

                download
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