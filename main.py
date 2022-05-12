
from oauthlib.oauth2 import WebApplicationClient
import daisie
from daisie.core.misc import config_reader
from layout.layout_standard import SimpleLayout
import dash_bootstrap_components as dbc

from daisie.core import DaisieMain

import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

# initialize main app
daisie_main = DaisieMain(__name__, 
        title='Daisie Example App',
        assets_folder="assets",
        external_stylesheets = [
            {
                'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
                'rel': 'stylesheet',
                'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
                'crossorigin': 'anonymous'
            },
            dbc.themes.BOOTSTRAP
        ],
        external_scripts = [
            {"src": "assets/plotly-locale-de.js"}
            # ["https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"]
            # 'https://www.google-analytics.com/analytics.js',
            # {
            #     'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
            #     'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
            #     'crossorigin': 'anonymous'
            # }
        ]
    )
#config = config_reader().get_config()
#client_id = config['oauth'].get('client_id')        
#daisie_main.client = WebApplicationClient(client_id)
#client_id2 = config['oauth2'].get('client_id')
#daisie_main.client2 = WebApplicationClient(client_id2)
#client_id3 = config['oauth3'].get('client_id')
#daisie_main.client3 = WebApplicationClient(client_id3)

img = '/assets/core/static/assets/img/FIDA1.jpg'


daisie_main.create_navigator( 
        title="Apps", # "Navigator"
        id="navigation",
        url="/home",
        root=['navigation'],
        parent = '/home',
        default_app =True,
        img_path="/assets/img/FIDA1.jpg",
        description='Navigator',
        layout=SimpleLayout
        #kwargs_layout = {        }
        )


#creates all app instances
#from apps import create_appsInstances 
#create_appsInstances(daisie_main)

# Flask routes for login with google oauth
#from daisie.routes.oauth import oauth_routes
#oauth_routes(daisie_main)

#from apps.routes.oauth_github import oauth_routes
#oauth_routes(daisie_main)
#from apps.routes.oauth_linked import oauth_routes
#oauth_routes(daisie_main)

#print(daisie_main._apps.keys())

#daisie_main.showTree()

# Update the Navigator Layout to make sure, all navigation cards are generated/all apps are registered
daisie_main.update_navigator()

# Collect the layouts from all apps
daisie_main.set_validation_layout()



# traverse through the apps and register all callbacks
daisie_main.initiate_callbacks()

daisie_main.showTree()
#print(daisie_main.tree.get_dict_for_breadcrumbs('excel-app'))

# server variable needed for gunicorn or AWS
server = daisie_main.server
# application = server
# app = application


# run debug server for local execution under http://127.0.0.1:8051
if __name__ == '__main__':
    daisie_main.run_server(debug=True, host="127.0.0.1", port=5000)#, ssl_context = "adhoc")
    
