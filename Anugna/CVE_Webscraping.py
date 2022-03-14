import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import numpy as np

##################################################
headers = dict()
headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
###################################################
# Defining of the dataframe
#, 'CWE_ID','No_of_Exploits','Vulnerability_Type(s)','Publish_Date','Update_Date','Score','Gained_Access_Level','Access','Complexity','Authentication','Conf','Integ','Avail'])
df = pd.DataFrame(columns=['S_no', 'CVE_ID'])
pages = np.arange(1, 10, 1)
for page in pages:
    url = "https://www.cvedetails.com/vulnerability-list.php?vendor_id=16&product_id=&version_id=&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year=0&month=0&cweid=0&order=1&trc=4159&sha=b6b9f0966b7dbca88b729e5b85a1f8fffc37d986"
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html.parser")
    table = soup.find('table', class_="searchresults sortable", id="vulnslisttable")
    print(page)
###################################################
table1 = soup.find('table', class_="searchresults sortable", id="vulnslisttable")
# print("hi.........")
# print(table1)

# Obtain every title of columns with tag <th>
headers = []
for i in table1.find_all('th'):
    title = i.text
    headers.append(title)
    # print(headers)

headers.append('\n\t\t\t\tDesc.\n\t\t\t')
#mydata = pd.DataFrame(columns = headers)
#print(mydata)
headers2 = []
for element in headers:
    temp_str=""
    for char in element:
        if char =="\n" or char=="\t":
            continue
        temp_str+=char
    headers2.append(temp_str)
print(headers2)



# Create a for loop to fill mydata
data1 = []
temp_row = []
count = 0
for j in table1.find_all('tr')[1:]: # need the data in this tag
    count += 1
    row_data = j.find_all('td')
    row = [i.text for i in row_data]
    if count % 2 != 0:

        temp_row = []
    temp_row += row

    if count % 2 == 0:
        #print(temp_row)
        details = []
        for element in temp_row:
            temp_str = ""
            for char in element:
                if char == "\n" or char == "\t":
                    continue
                temp_str += char
            details.append(temp_str)
        print(details)
        data1.append(details)

        #mydata.loc[len(mydata)] = temp_row
mydata= pd.DataFrame(data1,columns = headers2)
print(mydata)

csv_data = mydata.to_csv()
print(csv_data)

    #length = len(mydata)
    #mydata.loc[length] = row






