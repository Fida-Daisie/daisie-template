from layout.layout_standard import SimpleLayout
from .new_reports.report_grid import ReportGrid

def create_appsInstances(daisie_main):
    login = daisie_main.oauth

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