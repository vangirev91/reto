from typing import Sequence
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd 
from google.oauth2 import service_account
import numpy as np
from Google import Create_Service

##CREANDO LA INSTANCIA PARA LA AUTENTICACIÓN DEL API
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds=None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

#ID DEL FILE DEL DRIVE 
SAMPLE_SPREADSHEET_ID = '1ZO-upikO2t_ISZODnLURbsxflylYnW_tOtMbe_DWZZQ'

try:
    service = build('sheets', 'v4', credentials=creds)
    #LLAMADA DEL API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Reto1!A2:D16").execute()
    #OBTENIENDO LO VALORES
    values = result.get('values', [])
except HttpError as err:
    print(err)


# INSTALAMOS PANDAS (pip install pandas) PARA EJECUCIÓN DEL PIVOT
#CONVIRTIENDO LA INFORMACIÓN EN DATAFRAME PARA USO DE LA BIBLIOTECA
df = pd.DataFrame(np.array(values),
                   columns=['Author', 'Sentiment', 'Country','Theme']) 
#Pivot Table                   
country=df.pivot_table(index=['Author','Sentiment'],columns=['Country'],values=['Country'],aggfunc={"Country":any}).fillna(False)
theme=df.pivot_table(index=['Author','Sentiment'],columns=['Theme'],values=['Theme'],aggfunc={"Theme":any}).fillna(False)
out = pd.concat([country, theme], axis=1).fillna(False)
out=str(out)
print(out)
splitT= out.split("\n")
arrayTemp=[]
for value in splitT:
    list=value.replace(" ",",")
    list=list.split(",")
    listTmp=[]
    for temp in list:
        if len(temp)>0:
            listTmp.append(temp)
            if temp=='Country':
                listTmp.append(" ")
    arrayTemp.append(listTmp)
#CREANDO UN NUEVO SHEET FILE PARA INGRESOS DE LOS RESULTADOS
CLIENT_SECRET_FILE="client_secret.json"
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
sheet_body = {
    'properties': {
        'title': 'Resultado del Primer Reto',
        'autoRecalc': 'ON_CHANGE', 
        'timeZone': 'America/Guayaquil'
        }
    ,
    'sheets': [
        {
            'properties': {
                'title': 'Pivot_Table'
            }
        }
    ]
}

nuevo_file = service.spreadsheets().create(body=sheet_body).execute()
idfile=nuevo_file['spreadsheetId']
#URL DEL FILE
print(nuevo_file['spreadsheetUrl'])
values = [["arrayTemp","dd"]]
body = {
    'values': arrayTemp
}
result = service.spreadsheets().values().update(
    spreadsheetId=idfile, range="Pivot_table!A1",
    valueInputOption="USER_ENTERED", body=body).execute()
