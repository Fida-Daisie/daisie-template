from layout.layout_standard import SimpleLayout
from .new_reports.report_grid import ReportGrid

from .helper.misc import read_config_for_oauth

def create_appsInstances(daisie_main, login:bool=False):
    img = "/assets/img/FIDA1.jpg"
    daisie_main.create_navigator( 
        title="Home",
        id="home",
        url="/home",
        root=['root'],
        default_app=True,
        img_path=img,
        description='Navigator',
        layout=SimpleLayout
    )

    if all(~read_config_for_oauth()):
        login = False

    ReportGrid(
        title="Business Report",
        id="template_report_grid",
        url="/report",
        # parent="home",
        img_path=img,
        description='Ein Business Report zur Illustration der Möglichkeiten von Daisie. Zum Fortfahren ist ein Login bei Google, LinkedIn oder Github nötig.',
        daisie_main=daisie_main,
        layout=SimpleLayout,
        login=login
    )