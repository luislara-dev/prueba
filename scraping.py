
import time
import re
import pandas as pd
import openpyxl
import gspread
import pandas as pd
import json 
from SepararNombres import SepararNombres
from bs4.element import Stylesheet
from gspread.models import Worksheet
from pandas.core.frame import DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

ruta_excel = "C:\\Users\\alex5\\Downloads\\PADRON DE ESTUDIANTES 2021.xlsx"
nombre_hoja = "Padron Estudiantes 2021"

### GOOGLE API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\\alex5\\Downloads\\proyectopruebas-330717-919f78f2d4b3.json', scope)
client = gspread.authorize(creds)
sheet = client.open('PADRON DE ESTUDIANTES 2021  - UNFV PSICOLOGIA')

def actualizarExcel(fila,dni):
    archivo = openpyxl.load_workbook(ruta_excel)
    hoja = archivo.get_sheet_by_name(nombre_hoja)
    hoja.cell(row=fila,column=4).value = dni
    archivo.save(ruta_excel)
    
def actualizarSheet(fila,dni):
    # scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\\alex5\\Downloads\\proyectopruebas-330717-919f78f2d4b3.json', scope)
    # client = gspread.authorize(creds)
    sheet = client.open('PADRON DE ESTUDIANTES 2021  - UNFV PSICOLOGIA')
    sheet_instance = sheet.get_worksheet(0)
    sheet_instance.update_cell(fila, 4, dni)

def buscarDNIenWEB(nombres, ape_p, ape_m):
    s = Service("C:\\Users\\alex5\\Downloads\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_experimental_option('excludeSwitches',['enable-logging']);
    driver = webdriver.Chrome(service=s, chrome_options=options)
    driver.get("https://eldni.com/pe/buscar-por-nombres")
    driver.find_element_by_id("nombres").send_keys(nombres)
    driver.find_element_by_id("apellido_p").send_keys(ape_p)
    driver.find_element_by_id("apellido_m").send_keys(ape_m)
    driver.find_element_by_css_selector("button[type='submit']").click()
    time.sleep(0.1)
    soup = BeautifulSoup(driver.page_source,'lxml')
    try :
        thDNI = soup.find_all('th')[4]
        resultDNI = re.findall('<th>(\d*)<\/th>',str(thDNI))[0]
        return resultDNI
    except : 
        resultDNI = ""
        return resultDNI
    
def cargarDatosDesdeExcel():
    
    dfDatos = pd.read_excel(io=ruta_excel,sheet_name=nombre_hoja)
    lista = dfDatos.to_dict('list')

    id = lista["ID"]
    nombresyapellidos = lista['Apellidos y Nombres'] 
    docIden = lista['DNI']
    totalFilas = len(id)
    contDniVacios = 0
    for i in docIden:
        if pd.isnull(i):
            contDniVacios+=1
            
    combo = zip(id,nombresyapellidos, docIden) 
    fila = 2
            
    for id,nombresyapellidos, docIden in combo:
        if (fila > 242):
            if (pd.isna(docIden)):
                nombrescompleto = SepararNombres(nombresyapellidos)
                ap = nombrescompleto[0]
                am = nombrescompleto[1]
                nombres = nombrescompleto[2]
                dni = buscarDNIenWEB(nombres,ap,am)
                if (dni == ""):
                    print("Fila: "+ str(fila) + "\tID " + str(id) + "\t" + str(docIden) +" --> [No se encontro DNI] " + ap + " " + am + " " + nombres)
                    contDniVacios -= 1
                else :
                    print("Fila: "+ str(fila) + "\tID " + str(id) + "\t" + str(docIden) +" --> [SE ENCONTRÓ] " + dni + " " + ap + " " + am + " " + nombres +
                          " --- Faltan buscar " + str(contDniVacios) + " registros")
                    #actualizarExcel(fila,dni)
                    actualizarSheet(fila,dni)
                    contDniVacios -= 1
        fila = fila + 1
    
def cargarDatosDesdeSheet():
    id = sheet.get_worksheet(0).col_values(1)
    nombresyapellidos = sheet.get_worksheet(0).col_values(3)
    docIden = sheet.get_worksheet(0).col_values(4)
    combo = zip(id,nombresyapellidos, docIden) 
    contDniVacios = docIden.count("")
    
    fila = 1
    for id, nombresyapellidos, docIden in combo:
        if (fila >= 2 ):
            if docIden == "" :
                nombrescompleto = SepararNombres(nombresyapellidos)
                ap = nombrescompleto[0]
                am = nombrescompleto[1]
                nombres = nombrescompleto[2]
                dni = buscarDNIenWEB(nombres,ap,am)
                if (dni == ""):
                    print("Fila: "+ str(fila) + "\tID " + str(id) + "\t" + str(docIden) +" --> [No se encontro DNI] " + ap + " " + am + " " + nombres +
                          " --- Faltan buscar " + str(contDniVacios) + " registros")
                    contDniVacios -= 1
                else :
                    print("Fila: "+ str(fila) + "\tID " + str(id) + "\t" + str(docIden) +" --> [SE ENCONTRÓ] " + dni + " " + ap + " " + am + " " + nombres +
                          " --- Faltan buscar " + str(contDniVacios) + " registros")
                    #actualizarExcel(fila,dni)
                    actualizarSheet(fila,dni)
                    contDniVacios -= 1
        fila = fila + 1
    
print("Iniciando scraper")
cargarDatosDesdeSheet()
#cargarDatosDesdeExcel()








