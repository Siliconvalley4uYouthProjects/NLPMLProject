import json
from firebase import firebase
import pandas as pd
myDB = firebase.FirebaseApplication("https://lightsource-1171-default-rtdb.firebaseio.com/", None)
# read file
companyName = input("Enter the company name: ")
cN = companyName
companyName = companyName.lower()

dataPiece = {}

with open('nvdcve-1.1-2021.json', 'r') as myfile:
    data=myfile.read()

x = json.loads(data)

dataSets = x["CVE_Items"]

for x in dataSets:
    if len(x['cve']['references']['reference_data']) > 0 and len(x['cve']['description']['description_data']) > 0:
        if companyName in x['cve']['references']['reference_data'][0]["url"].lower() or companyName in x['cve']['description']['description_data'][0]["value"].lower():
            print(type(x['cve']['references']['reference_data'][0]["url"].lower()))
            print(companyName in x['cve']['references']['reference_data'][0]["url"])
            print("__________")

            print(x['cve']['references']['reference_data'][0]["url"].lower())
            dataPiece["companyName"] = cN
            dataPiece["cveID"] = x['cve']['CVE_data_meta']['ID']
            dataPiece["description"] = x['cve']['description']['description_data'][0]['value']
            dataPiece["url"] = x['cve']['references']['reference_data'][0]["url"].lower()

            if 'baseMetricV2' in x['impact']:
                severity = x['impact']['baseMetricV2']['severity']
                dataPiece["severity"] = severity
            result = myDB.post("CVE", dataPiece)
            dataPiece = {}

with open('nvdcve-1.1-2020.json', 'r') as myfile:
    data=myfile.read()

x = json.loads(data)

dataSets = x["CVE_Items"]

for x in dataSets:
    if len(x['cve']['references']['reference_data']) > 0 and len(x['cve']['description']['description_data']) > 0:
        if companyName in x['cve']['references']['reference_data'][0]["url"].lower() or companyName in x['cve']['description']['description_data'][0]["value"].lower():
            dataPiece["companyName"] = cN
            dataPiece["cveID"] = x['cve']['CVE_data_meta']['ID']
            dataPiece["description"] = x['cve']['description']['description_data'][0]['value']

            if 'baseMetricV2' in x['impact']:
                severity = x['impact']['baseMetricV2']['severity']
                dataPiece["severity"] = severity
            result = myDB.post("CVE", dataPiece)
            dataPiece = {}

getData = myDB.get("CVE", None)

for key in getData:
    print(getData[key])
    print()
    print()