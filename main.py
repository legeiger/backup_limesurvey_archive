# %%
import httpx
from urllib.parse import unquote
from bs4 import BeautifulSoup
from datetime import datetime
import os

## This will throw an error if not set
# $env:LS_URL = 'https://befragungen.isv.uni-stuttgart.de'
host = os.environ['LS_URL']
username = os.environ['username']
password = os.environ['password']
date_time = os.environ['timestamp']

# now = datetime.now() # current date and time
# date_time = now.strftime("%Y_%m_%d_%H_%M_%S")

#default to data path for saving → we defined this inside docker as well
file_save_path = r'/data/'

headers = {
"Accept-Encoding" : "gzip, deflate, br",
"Accept-Language" : "de,en-US;q=0.7,en;q=0.3",
"Connection" : "keep-alive",
"DNT" : "1",
"Host" : "befragungen.isv.uni-stuttgart.de",
"Sec-Fetch-Dest" : "document",
"Sec-Fetch-Mode" : "navigate",
"Sec-Fetch-Site" : "same-origin",
"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
}

# %%
with httpx.Client() as client:
    # %%
    url = host +  r'/index.php/admin/authentication/sa/login'
    r = client.get(url, headers=headers)    
    TOKEN = unquote(r.cookies['YII_CSRF_TOKEN'])
    PHPSESSID = unquote(r.cookies['PHPSESSID'])
    # print(r.cookies)
    form_data = {
    "YII_CSRF_TOKEN": TOKEN,
    "authMethod": "Authdb",
    "user": username,
    "password": password,
    "loginlang": "default",
    "action": "login",
    "width": "1825",
    "login_submit": "login"
}
    # form_data = {
    # "YII_CSRF_TOKEN": TOKEN,
    # "PHPSESSID": PHPSESSID,
    # "authMethod": "Authdb",
    # "user": username,
    # "password": password,
    # "loginlang": "default",
    # "action": "login",
    # "width": "1825",
    # "login_submit": "login"
    # }
    r = client.post(url, data=form_data, headers=headers)
    print(r, r.status_code, r.cookies, r.headers)
    url = host +  r'/index.php/surveyAdministration/listsurveys'
    # ?ajax=survey-grid&pageSize=100
    params={"ajax": "survey-grid", "pageSize": 100}
    r = client.get(url, headers=headers, params=params)
    print(r, r.status_code, r.cookies, r.headers)
    soup = BeautifulSoup(r.text, "html.parser")
    data = soup.find('table', class_="items table table-hover table table-hover").findAll('td', class_="d-none d-sm-table-cell has-link")
    surveys = []
    for d in data:
        try:
            surveys.append(int(d.text))
        except ValueError:
            pass
    print("\n")
    print(surveys)
    print("\n")
    for id in surveys:
        for archivetype in ["exportarchive", "exportstructurexml"]:
            extension = ".lsa" if archivetype == "exportarchive" else ".lss"
            dl_url  = host + f"/index.php/admin/export/sa/survey/action/{archivetype}/surveyid/{id}"
            r = client.get(dl_url, headers=headers)
            # Save file data to local copy survey_archive_819872.lsa
            with open(file_save_path + date_time + "_survey_archive_" + str(id) + extension, 'wb') as file:
                for chunk in r.iter_bytes(1024):
                    file.write(chunk)


