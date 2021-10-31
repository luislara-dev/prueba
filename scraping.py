
import time
from pandas.core.frame import DataFrame
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common import by
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import pandas as pd
import openpyxl

print("Iniciando scraper")
ruta_excel = "C:\\Users\\alex5\\Downloads\\PADRON DE ESTUDIANTES 2021.xlsx"
nombre_hoja = "Padron Estudiantes 2021"
dfDatos = pd.read_excel(io=ruta_excel,sheet_name=nombre_hoja)
lista = dfDatos.to_dict('lista')

nombres = lista['Nombres'] 
apellidos_P = lista['Apellido Paterno']
apellidos_M = lista['Apellido Materno']
docIden = lista['DNI']

combo = zip(nombres,apellidos_P, apellidos_M, docIden) 

def buscarDNIenWEB(nombres, ape_p, ape_m):
    s = Service("C:\\Users\\alex5\\Downloads\\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    driver.get("https://eldni.com/pe/buscar-por-nombres")
    driver.find_element(By.ID,'nombres').send_keys(nombres)
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

fila = 2
for nombres, apellidos_P, apellidos_M, docIden in combo:
    print("Fila " + str(fila) + " " + str(docIden))
    if (pd.isna(docIden)):
        dni = buscarDNIenWEB(nombres,apellidos_P,apellidos_M)
        print (print(dni +"\t"+ nombres," ",apellidos_P," ",apellidos_M))
        archivo = openpyxl.load_workbook(ruta_excel)
        hoja = archivo.get_sheet_by_name(nombre_hoja)
        hoja.cell(row=fila,column=10).value = dni
        archivo.save(ruta_excel)
    fila = fila + 1

#####








