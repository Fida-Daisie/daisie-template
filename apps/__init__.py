

# import data

from layout.layout_standard import SimpleLayout


def create_appsInstances(daisie_main):
    
   
    appInstances = []


    # from .daisie_description import DaisieDescription
    # appInstances.append(DaisieDescription(
    #         title="DAISIE",
    #         id="daisie_description ",
    #         url="/description",
    #         parent="/home",
    #         img_path="assets/img/FIDA1.jpg",
    #         description='Daisie',
    #         layout=SimpleLayout,
            
    #     ))


    from .new_reports.report_grid import ReportGrid

    appInstances.append(ReportGrid(
            title="Business Report",
            id="template_report_grid",
            url="/report",
            parent="navigation",
            img_path="/assets/img/FIDA1.jpg",
            description='Ein Business Report zur Illustration der Möglichkeiten von Daisie. Zum Fortfahren ist ein Login bei Google, LinkedIn oder Github nötig.',
            daisie_main =daisie_main,
            #security = True,
            #alternative='/googlelogin',
            layout=SimpleLayout,
        ))



    for App_Instance in appInstances:
        daisie_main.register_app(App_Instance)