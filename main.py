from daisie.core import DaisieMain
from apps import create_appsInstances 

import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

oauth = True

# initialize main app
daisie_main = DaisieMain(__name__, 
        title='Daisie Example App',
        update_title=None,
        assets_folder="assets",
        oauth=oauth
    )

# creates all app instances
create_appsInstances(daisie_main, login=oauth)

# Update the Navigator Layout to make sure, all navigation cards are generated/all apps are registered
daisie_main.update_navigator()

# Collect the layouts from all apps
daisie_main.set_validation_layout()

# traverse through the apps and register all callbacks
daisie_main.initiate_callbacks()

daisie_main.showTree()

# server variable needed for gunicorn or AWS
server = daisie_main.server
# application = server
# app = application


# run debug server for local execution under http://127.0.0.1:8051
if __name__ == '__main__':
    daisie_main.run_server(debug=True, host="127.0.0.1", port=5000)
    
