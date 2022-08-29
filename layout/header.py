from daisie.core.presentation.components import DaisieComponent
import dash_bootstrap_components as dbc
from dash import html

class SingleHeader(DaisieComponent):
    def __init__(self, id, 
            logo_link='https://www.fida.de',
            ):
        
        super().__init__(id=id)
        self.logo_link = logo_link
        
    def register_callbacks(self):
        pass
    
    def get_layout(self):
        header_layout = html.Div(
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col([
                                    html.H2('DAISIE Beispielapp', className="text-primary"
                                    )
                                    ], 
                                    className='header-title',
                                    width=4
                                ),
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
                                        )
                                ], 
                        justify="between"
                        ),
                    #  dbc.Row(
                    #             children=[               
                    #                 ,
                    #                 ],
                    #             justify="end",
                    #             )
                    ],
                    className = 'header'
                    ) 
                
        return header_layout
