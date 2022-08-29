import numpy as np
from daisie.core.misc import  config_reader

def read_config_for_oauth():
    config = config_reader().get_config()

    try: 
        if (config["google-oauth"].get('client_id') is None or config["google-oauth"].get('client_id') == ""
            or config["google-oauth"].get('client_secret') is None or config["google-oauth"].get('client_secret') == ""):
            display_google = False
        else:
            display_google = True
    except KeyError as e:
        display_google = False

    try:
        if (config["github-oauth"].get('client_id') is None or config["github-oauth"].get('client_id') == ""
            or config["github-oauth"].get('client_secret') is None or config["github-oauth"].get('client_secret') == ""):
            display_github = False
        else:
            display_github = True
    except KeyError as e:
        display_github = False
    
    try:
        if (config["linkedin-oauth"].get('client_id') is None or config["linkedin-oauth"].get('client_id') == ""
            or config["linkedin-oauth"].get('client_secret') is None or config["linkedin-oauth"].get('client_secret') == ""):
            display_linkedin = False
        else:
            display_linkedin = True
    except KeyError as e:
        display_linkedin = False

    return np.array([display_google, display_github, display_linkedin])