import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import requests
import json
from lxml import html

from bs4 import BeautifulSoup

import urllib.request
from time import sleep
from random import randint

from urllib.request import urlopen

import os
import platform




def slaveFile(new_route):
    opts = Options()
    #opts.add_argument("--headless")
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0")

    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
    }

#-----------------------------------------------------------

    sistema = platform.system()


    if sistema == "Linux":
        print("Estamos en {}".format(sistema))
        driver = webdriver.Chrome('./firefox/geckodriver',options=opts)
    else:
        print("Estamos en {}".format(sistema))
        driver = webdriver.Chrome('./geckodriver.exe', options=opts)


    login_form_url = 'http://10.10.50.142:8010/register/'
    driver.get(login_form_url)


#-----------------------------------------------------------





    session = requests.Session()
    print(login_form_url)

    login_form_res = session.get(login_form_url, headers=headers)

    parser_login = html.fromstring(login_form_res.text)


    token_especial = parser_login.xpath('//input[@name="csrf_token"]/@value')
    print(token_especial)



    login_url = 'http://10.10.50.142:8010/upload/'


    login_data = {
        "login": "raven",
        "password": "reven",
        "csrf_token": token_especial
    }

    session.post(
        login_url, 
        data=login_data, 
        headers=headers
    )


    data_url = 'http://10.10.50.142:8010/reportsjson/'
    respuesta = session.get(
        data_url,
        headers=headers
    )


#----------------------------------------------------------------------

    input_user = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="login"]'))
    )
    # Obtengo los inputs de username
    input_pass = driver.find_element(By.XPATH, '//input[@name="password"]')

    # Escribo mi usuario input
    input_user.send_keys(login_data["login"])

    # Escribo mi contrasena en el input
    input_pass.send_keys(login_data["password"])

    # Obtengo el boton de login
    login_button = driver.find_element(By.XPATH, '//button[@class="btn"]')
    # Le doy click
    login_button.click()

#----------------------------------------------------------------------
    #Ruta para encontrar el archivo en carpeta file de nuestro proyecto
    ruta_archive = new_route


#----------------------------------------------------------------------
    #Analizar
    dropdown_button_analize = driver.find_element_by_partial_link_text('Analyze')
    # Le doy click
    dropdown_button_analize.click()
    # Obtengo para descubrir el boton de la url
    url_button = driver.find_element(By.XPATH, '//li//a[@href ="/upload/"]')
    # Le doy click
    url_button.click()




    sleep(5)
    print('Ya dejamos el 1 Sleep')


#-----------------------------------------------------------------------
    #Cargamos el archivo


    input_file = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@id="file"]'))
    )
    upload_button = driver.find_element(By.XPATH, '//input[@id="file"]').send_keys(ruta_archive)

    sleep(randint(4,6))
    print('Ya dejamos el 2 Sleep atr??s')

    #-----------Marcamos el tipo de an??lisi-------------------------------

    choisces_3 = driver.find_element(By.XPATH, '//input[@id ="choices-3"]')
    choisces_3.click()
    
    #Nota: quer??a hacer de esto algo un poco mas autom??tico... hacer un bugle para recorrer los choisces 
    # y as?? marcarlos todos, ofreciendo incluso mejoras en el c??digo 
    # anterior, si se pod??a claro, quer??a probarlos. 



    #Obtengo el boton de submitandwait
    submitandwait = driver.find_element(By.XPATH, '//input[@id ="submitandwait"]')
    # Le doy click
    submitandwait.click()


    sleep(randint(10,11))
    driver.back()



    print("Analisis realizado, vamos a la descarga")
    print("\n...ya pasaron los 33 segundos")
    
    #importante:
    #Queria detectar un evento, para detectar la finalizaci??n del an??lisis, pero no se si era posible dado que la app esta fuera de linea

    #---------------------------------------------------------------------------
    #Si todo esta como la anterior esto despu??s de el an??lisis recuperamos el reporte
    #c??digo:


    dropdown_button_reports = driver.find_element_by_partial_link_text('Reports')
    # Le doy click
    dropdown_button_reports.click()


    # Obtengo para descubrir el boton de los json
    json_button = driver.find_element(By.XPATH, '//li//a[@href ="/reportsjson/"]')
    # Le doy click
    json_button.click()



    #---------------------------------------------------------------
    #Descarga de los links
    #---------------------------------------------------------------

    data_url = 'http://10.10.50.142:8000/reportsjson/'
    respuesta = session.get(
        data_url,
        headers=headers
    )


    #aqui devolvemos el texto o nombre del identificador + su url corespondiente

    
    #Tenemos algunos problemas con la app y por ello, tengo casi el mismo codigo que la
    #app de la url, pero va casi igual, al obtener el an??lisi identificamos el id de el test
    #lo recorremos y recuperamoe n una variable que al limpiarla del html la pasamos a la vista
    #del proyecto en fastapi





    urls = []
    parser = html.fromstring(respuesta.text)
    descargas = parser.xpath('//td[@class="col-file"]/a/text()')
    for descarga in descargas:
        urls.append(descarga)


    links = driver.find_elements(By.XPATH, '//td[@class="col-file"]/a')
    links_hrefs = [link.get_attribute('href') for link in links]

    contador = 0

    temin = ''

    for i in links_hrefs:
        print(i)
        print(urls[contador])
        r = driver.get(i)
        pagina =  driver.page_source
        soup = BeautifulSoup(pagina, "html.parser")
        contenido_json = soup.find("div", attrs={"id":"json"}).get_text()
        contenido_json = contenido_json.replace('<div id="json">', '').replace('</div>','') #no tenia la app activa para poder detectarlo
        #print(contenido_json)
        temin = contenido_json
        driver.back()
        break
     

    





   #----------------------------------------------------------------------
    

    sleep(randint(10,11))
    print('Ya dejamos el 3 Sleep')

    #----------------------------------------------------------------------

    #Borrar el usuario para luego relogearnos

    url_button = driver.find_element(By.XPATH, '//li//a[@href ="/user/"]')
    # Le doy click
    url_button.click()


    input_user = driver.find_element(By.XPATH, '//input[@class="action-checkbox"]')

    input_user.click()

    with_selected = driver.find_element(By.XPATH, '//a[@class="btn dropdown-toggle"]')

    with_selected.click()

    delete_selected = driver.find_element(By.XPATH, '//ul[@class="dropdown-menu"]')

    delete_selected.click()


    #-----------------------------------------------------------------------------------
    sleep(randint(5,6))
    alert_obj = driver.switch_to.alert
    alert_obj.accept()


    print('Ya pasamos en javascript, Usuario eliminado')


    return temin  


    

#Importante :
 
#Me hubiese gustado probarla, dado que por mala suerte pueden cambiar algunas cosas para 
#recuperar los valores... pero debido al percance explico mi soluci??n a trav??s como:

#Como la principal dificultad era el usuario , decid?? que registrarse 
#siempre era la mejor opci??n, borrando al final de cada an??lisis que hici??ramos y as?? reutilizar las veces que quiera raven/raven.

#Por otro lado... en la vista dentro del proyecto "Test File" tenia la 
#opci??n de colocar la ruta del archivo, pero vi un poco m??s c??modo para el usuario 
#arrastrar o copiar todo lols archivos que deseara analizar a una carpeta dentro del proyecto 
#-> files para que dentro de la funci??n slaveFile, detecte la ruta del archivo y  pueda proceder a su an??lisis.

#El codigo que va a partir del Choise esta sujeto a cambios, dado que tengo que probarlo para ver si trae el resultado
#y si accedo de manera correcta a los xpat