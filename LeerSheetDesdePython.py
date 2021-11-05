#https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\\alex5\\Downloads\\proyectopruebas-330717-919f78f2d4b3.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('PADRON DE ESTUDIANTES 2021  - UNFV PSICOLOGIA')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

# get all the records of the data
records_data = sheet_instance.get_all_records()

# view the data
#print(records_data)

# convert the json to dataframe
records_df = pd.DataFrame.from_dict(records_data)

# view the top records
print(records_df)