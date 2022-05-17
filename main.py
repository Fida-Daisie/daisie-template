
from daisie.core.misc import config_reader
from layout.layout_standard import SimpleLayout
import dash_bootstrap_components as dbc

from daisie.core import DaisieMain

import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

# initialize main app
daisie_main = DaisieMain(__name__, 
        title='Daisie Example App',
        update_title=None,
        assets_folder="assets",
        external_stylesheets = [
            dbc.icons.FONT_AWESOME,
        ]
    )

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
from apps import create_appsInstances 
create_appsInstances(daisie_main, login=True)

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
    