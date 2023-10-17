import requests
import json
import pandas as pd

fields = [
    "file_name",
    "cases.submitter_id",
    "cases.samples.sample_type",
    "cases.disease_type",
    "cases.project.project_id",
    "cases.demographic.race",
    "cases.demographic.age_at_index",
    "cases.project.primary_site"
    ]

fields = ",".join(fields)

files_endpt = "https://api.gdc.cancer.gov/files"

# This set of filters is nested under an 'and' operator.
filters = {
    "op": "and",
    "content":[
        {
        "op": "in",
        "content":{
            "field": "cases.project.project_id",
            "value": ["TCGA-UCEC"]
            }
        },
        {
        "op": "in",
        "content":{
            "field": "files.experimental_strategy",
            "value": ["Methylation Array"]
            }
        },
        {
        "op": "in",
        "content":{
            "field": "files.data_format",
            "value": ["TXT"]
            }
        }
    ]
}

# A POST is used, so the filter parameters can be passed directly as a Dict object.
params = {
    "filters": filters,
    "fields": fields,
    "format": "CSV",
    "size": "2000"
    }

# The parameters are passed to 'json' rather than 'params' in this case
response = requests.post(files_endpt, headers = {"Content-Type": "application/json"}, json = params)

result_list = response.content.decode("utf-8").split('\n')
result_list = [f.replace("Cystic, Mucinous", "Cystic Mucinous") for f in result_list]
result_list = [f.replace("Neoplasms, NOS", "Neoplasms NOS") for f in result_list]
result_list = [f.split(',')[:-1] for f in result_list]
headers = result_list.pop(0)
cols = ['age', 'race', 'disease_type', 'primary_site', 'project_id','sample_type','submitter_id','methylation_file_id']

result_df = pd.DataFrame(result_list, columns = cols)
result_df.to_csv('data/ucec_metadata.csv')

