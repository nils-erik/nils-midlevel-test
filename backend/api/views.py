from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict
import requests
from datetime import datetime
from .models import inspector_model, inspection_model

def ingest_inspections():
    """This module simply retrieves the inspections in JSON format."""
    inspections_endpoint = "https://6244305b3da3ac772b0c7854.mockapi.io/fakeSolar/3rdParty/inspections"
    get_response = requests.get(inspections_endpoint)
    return get_response.json()


def ingest_inspectors():
    """This module simply retrieves the inspectors in JSON format."""
    inspectors_endpoint = "https://6244305b3da3ac772b0c7854.mockapi.io/fakeSolar/3rdParty/inspectors"
    get_response = requests.get(inspectors_endpoint)
    return get_response.json()


def filter_inspections(inspectors, inspections):
    """This filters out the inspections that have Inspector IDs for Inspectors
       that aren't labeled with SolarGrade, and selects the inspectors that
       have completed SolargGrade inspections."""
    # select appropriate inspectors
    sg_inspectors = [
        inspector
        for inspector in inspectors
        if "SolarGrade" in inspector["availableIntegrations"]
    ]
    # select appropriate inspections
    sg_inspections = [
        inspection
        for inspection in inspections
        if int(inspection["inspectorId"]) in [
            int(inspector["id"])
            for inspector in sg_inspectors
        ]
    ]
    # remove the inspectors that haven't done solargrade inspections
    filt_sg_inspectors = [
        inspector
        for inspector in sg_inspectors
        if int(inspector["id"]) in [
            inspection["inspectorId"]
            for inspection in sg_inspections
        ]
    ]
    return filt_sg_inspectors, sg_inspections


# Create your views here.
@api_view(['GET', 'POST'])
def api_home(request):
    """
    The data is either retrieved from the external API, or if it is not found,
    called from the database.
    """
    # get the inspectors from external API
    ext_inspectors = ingest_inspectors()
    # get the inspections from external API
    ext_inspections = ingest_inspections()
    # get data from the DB if not found from external API
    # Set the company name here, then filter out this company from the database
    company = "FakeSolar_Co"
    if ext_inspectors == 'Not found' or ext_inspections == 'Not found':
        ext_inspectors = []
        db_inspectors = inspector_model.objects.all()
        for inspector_obj in db_inspectors:
            if inspector_obj.company == company:
                ext_inspectors.append(model_to_dict(inspector_obj))
        ext_inspections = []
        db_inspections = inspection_model.objects.all()
        for inspection_obj in db_inspections:
            if inspection_obj.company == company:
                ext_inspections.append(model_to_dict(inspection_obj))

    # filter the data
    filt_inspectors, filt_inspections = filter_inspections(ext_inspectors,
                                                           ext_inspections)
    itemsOk = len([inspection['items'][0]['isIssue'] == 'false' for inspection in filt_inspections if
                   len(inspection['items']) > 0])
    issuesWarningCount = len([inspection['items'][0]['isIssue'] == 'true' for inspection in filt_inspections if
                   len(inspection['items']) > 0 and int(inspection['items'][0]['severity']) < 60])
    issuesCriticalCount = len([inspection['items'][0]['isIssue'] == 'true' for inspection in filt_inspections if
                   len(inspection['items']) > 0 and int(inspection['items'][0]['severity']) > 60])
    inspection_data = [{"itemsOk": itemsOk, "issuesWarningCount": issuesWarningCount,
                        "issuesCriticalCount": issuesCriticalCount}]
    for inspection in filt_inspections:
        row = {}
        dt = inspection["createdAt"]
        time_format = datetime.strptime(dt[0:10], '%Y-%m-%d')
        inspectorName = [
            inspector["name"] for inspector in filt_inspectors if int(inspector["id"]) == inspection['inspectorId']
        ][0]
        title = f"{inspection['city']} - {datetime.strftime(time_format, '%Y/%m/%d')}"
        warning = 0
        critical = 0
        if len(inspection['items']) > 0:
            for item in inspection['items']:
                if item['severity'] > 60:
                    critical += 1
                elif item['severity'] < 60:
                    warning += 1
        row["title"] = title
        row["inspectorName"] = inspectorName
        row["Warning"] = warning
        row["Critical"] = critical
        inspection_data.append(row)
    return Response(inspection_data)
