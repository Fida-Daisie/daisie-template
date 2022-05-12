from dash import html 
import dash_bootstrap_components as dbc

from daisie.apps import DaisieApp


class Login(DaisieApp):
    def __init__(self, id, title, is_fixed=False, **kwargs):
        super().__init__(id=id, title=title, is_fixed=is_fixed, **kwargs)
        self.daisie_main = kwargs.get('daisie_main')

    def login_content(self):
        authorization_endpoint = "https://github.com/login/oauth/authorize"
        request_uri = self.daisie_main.client2.prepare_request_uri(
        authorization_endpoint,
        redirect_uri='https://127.0.0.1:5000/github_login/callback',
        login="Freakbrain")
        return html.Div(
            children=[
                html.H1('Herzlich Willkommen zu Daisie Fida'),
                html.P("Bitte loggen Sie sich über Ihren Google, LinkedIn oder Github Accoun ein!"),
                html.Br(),
               dbc.Row([
                    dbc.Col(
                        dbc.Button(
                                children=[
                                    html.Img(src="assets/img/googleicon.png", className='icon_size'),
                                    "Google Sign-In",
                                    ],                
                                title="Bitte loggen Sie sich über Ihren Google Account ein",
                                href='/login',
                                color="dark",
                                outline=True
                        ),        
                        width=2      
                    ),        
                        
                    dbc.Col(
                        dbc.Button(
                                children=[
                                    html.Img(src='assets/img/linkedinicon.png', className='icon_size'),
                                    "LinkedIn Sign-In",
                                    ],                
                                title="Bitte loggen Sie sich über Ihren LinkedIn Account ein",
                                color="dark",
                                outline=True,
                                href="/linked_login"
                                ),
                        width=2
                    ),

                    dbc.Col(
                        dbc.Button(
                                children=[
                                    html.Img(src='assets/img/githubicon.png', className='icon_size'),
                                    "Github Sign-In",
                                    ],                
                                title="Bitte loggen Sie sich über Ihren Github Account ein",
                                color="dark",
                                outline=True,
                                href=request_uri
                        ),
                        width=2
                    )
            ], justify="center")
                ])
    def register_callbacks(self):
        pass
