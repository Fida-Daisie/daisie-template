from http import client
from flask import request
import json
import requests
from flask import redirect, request
from daisie.core.misc import  config_reader
from daisie.core.authentification.User import User
from flask_login import login_user
from random import randint


def oauth_routes(daisie_main):
    server = daisie_main.server
    config = config_reader().get_config()
    callback_url = config['oauth3'].get('callback_url')

    @server.route('/linked_login')
    
    def login_linkedin():
        
        authorization_endpoint = "https://www.linkedin.com/oauth/v2/authorization"
        request_uri = daisie_main.client3.prepare_request_uri(
        authorization_endpoint,
        redirect_uri= config['url'].get('base_url') + callback_url,
        scope="r_liteprofile")
        
        return redirect(request_uri)
    



    @server.route(callback_url)
    def callback_linkedin():
        # Get authorization code provider sent back to you
        code = request.args.get("code")
        token_url="https://www.linkedin.com/oauth/v2/accessToken"
        
        
        header = {'Accept': 'application/json'}
        params={
            'grant_type':'authorization_code',    
            'code':code,
            'client_secret': config['oauth3'].get('client_secret'),
            'client_id': config['oauth3'].get('client_id'),
            'redirect_uri':config['url'].get('base_url') + callback_url
            }
        
        token_response = requests.post(token_url, headers=header, params=params)
        
        

        # Parse the tokens!
        daisie_main.client3.parse_request_body_response(json.dumps(token_response.json()))
        userinfo_endpoint = 'https://api.linkedin.com/v2/me'
        uri, headers, body = daisie_main.client3.add_token(userinfo_endpoint)
        
        userinfo_response = requests.get(uri, headers=headers)
        if userinfo_response.status_code == 200:
            userinfo_dict =userinfo_response.json()
            unique_id = userinfo_dict.get("id_linked", randint(0, 100000000000000000))
            users_email = userinfo_dict.get("id")
            users_name = userinfo_dict.get("localizedLastName")
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