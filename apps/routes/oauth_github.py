
from http import client
from flask import request
import json
import requests
from flask import redirect, request
from daisie.core.misc import  config_reader
from daisie.core.authentification.User import User
from flask_login import login_user


def oauth_routes(daisie_main):
    server = daisie_main.server
    config = config_reader().get_config()
    callback_url = config['oauth2'].get('callback_url')
    
    @server.route('/github_login')

    def login_github():
        authorization_endpoint = "https://github.com/login/oauth/authorize"
        request_uri = daisie_main.client2.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=config['url'].get('base_url') + callback_url,
        login=config['oauth2'].get('login'))
        return redirect(request_uri)
    



    @server.route(callback_url)
    def callback_github():
        # Get authorization code provider sent back to you
        code = request.args.get("code")
        token_url="https://github.com/login/oauth/access_token"

        header = {'Accept': 'application/json'}
        params={    
            'code':code,
            'client_secret':config['oauth2'].get('client_secret'),
            'client_id':config['oauth2'].get('client_id'),
            'redirect_uri':config['url'].get('base_url') + callback_url
            }
        

        token_response = requests.post(token_url, headers=header, params=params)
        
        

        # Parse the tokens!
        daisie_main.client2.parse_request_body_response(json.dumps(token_response.json()))
        userinfo_endpoint = 'https://api.github.com/user'
        uri, headers, body = daisie_main.client2.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        if userinfo_response.status_code == 200:
            unique_id = userinfo_response.json()["id"]
            users_email = userinfo_response.json()["email"]
            users_name = userinfo_response.json()["login"]
        else:
            return "User email not available or not verified by the Oauth provider.", 400
        user = User(
        id=unique_id, name=users_name, email=users_email
        )

        # Doesn't exist? Add it to the database.
        if not User.get(unique_id):
            User.create(unique_id, users_name, users_email)

        # Begin user session by logging the user in
        login_user(user)

        # Send user back to homepage
        
        return redirect("/report")