
import time
import requests
import re
import pandas as pd
import openpyxl
import gspread
import pandas as pd
import json 
from bs4.element import Stylesheet
from gspread.models import Worksheet
from pandas.core.frame import DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

def actualizarExcel(fila,dni):
    archivo = openpyxl.load_workbook(ruta_excel)
    hoja = archivo.get_sheet_by_name(nombre_hoja)
    hoja.cell(row=fila,column=10).value = dni
    archivo.save(ruta_excel)
    
def actualizarSheet(fila,dni):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\\alex5\\Downloads\\proyectopruebas-330717-919f78f2d4b3.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('PADRON DE ESTUDIANTES 2021  - UNFV PSICOLOGIA')
    sheet_instance = sheet.get_worksheet(0)
    sheet_instance.update_cell(fila, 5, dni)

def buscarDNIenWEB(nombres, ape_p, ape_m):
    s = Service("C:\\Users\\alex5\\Downloads\\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    driver.get("https://eldni.com/pe/buscar-por-nombres")
    driver.find_element_by_id("nombres").send_keys(nombres)
    driver.find_element_by_id("apellido_p").send_keys(ape_p)
    driver.find_element_by_id("apellido_m").send_keys(ape_m)
    driver.find_element_by_css_selector("button[type='submit']").click()
    time.sleep(0.5)
    soup = BeautifulSoup(driver.page_source,'lxml')
    try :
        thDNI = soup.find_all('th')[4]
        resultDNI = re.findall('<th>(\d*)<\/th>',str(thDNI))[0]
        return resultDNI
    except : 
        resultDNI = ""
        return resultDNI
    
def cargarDatosDesdeExcel():
    ruta_excel = "C:\\Users\\alex5\\Downloads\\PADRON DE ESTUDIANTES 2021.xlsx"
    nombre_hoja = "Padron Estudiantes 2021"
    dfDatos = pd.read_excel(io=ruta_excel,sheet_name=nombre_hoja)
    lista = dfDatos.to_dict('list')

    nombres = lista['Nombres'] 
    apellidos_P = lista['Apellido Paterno']
    apellidos_M = lista['Apellido Materno']
    docIden = lista['DNI']

    combo = zip(nombres,apellidos_P, apellidos_M, docIden) 
    fila = 2
    for nombres, apellidos_P, apellidos_M, docIden in combo:
        print("Fila " + str(fila) + " " + str(docIden))
        if (pd.isna(docIden)):
            dni = buscarDNIenWEB(nombres,apellidos_P,apellidos_M)
            print(str(dni) +"\t"+ nombres," ",apellidos_P," ",apellidos_M)
            actualizarSheet(fila,dni)
        fila = fila + 1
    
def cargarDatosDesdeSheet():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\\alex5\\Downloads\\proyectopruebas-330717-919f78f2d4b3.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('PADRON DE ESTUDIANTES 2021  - UNFV PSICOLOGIA')
    id = sheet.get_worksheet(0).col_values(1)
    nombresyapellidos = sheet.get_worksheet(0).col_values(3)
    docIden = sheet.get_worksheet(0).col_values(4)
    combo = zip(id,nombresyapellidos, docIden) 
    
    for id, nombresyapellidos, docIden in combo:
        if id == "ID":
            continue
        if docIden == "" :
            lista = str(nombresyapellidos).split()
            ap = lista[0]
            am = lista[1]
            nombres = []
            cantNom = len(lista) - 2
            while cantNom > 0:
                nombres.append(lista[len(lista) - cantNom])
                cantNom = cantNom - 1
            print("ID " + str(id) + " " + str(docIden) + " " + ap + " " + am + " " + " ".join(nombres))
            dni = buscarDNIenWEB(" ".join(nombres),ap,am)
            actualizarSheet(int(id)+1,dni)
    
print("Iniciando scraper")
cargarDatosDesdeSheet()








