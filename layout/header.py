from xml.dom.minidom import Childless
from daisie.core.presentation.layouts.layout_fundamental import LayoutFundamental
import dash_bootstrap_components as dbc
from dash import html



class SingleHeader(LayoutFundamental):
    def __init__(self, id, 
            title=None, 
            logo_link='https://www.fida.de',
            ):
        
        super().__init__(id=id + '-header', title=title)
        self.logo_link = logo_link
        


    def get_layout(self):
        header_layout = html.Div(
                    children=[
                        dbc.Row(
                            children=[
                                html.H4('Daisie Beispielapp', style={"margin-left": "1rem", "margin-top": "1rem"})
                                ], 
                            className='header-title'
                        ),
                     dbc.Row(
                                children=[               
                                    dbc.Col(
                                        className='header-right',
                                        children=[
                                            html.Div(
                                                html.A(
                                                    id=self.id + '_banner-logo',
                                                    children=[html.Img(src='/assets/img/Logo_FIDA_Software_RGB.png', className='logo-img')],
                                                    className="banner-logo",
                                                    href=self.logo_link,
                                                    target="_blank"
                                                    )
                                                )
                                            ],
                                        width=3,
                                        style={"textAlign": "right"}
                                        ),
                                    ],
                                justify="end",
                                #className='header_logo_row'
                                )
                    ],
                    className = 'header'
                    ) 
                
        return header_layout
