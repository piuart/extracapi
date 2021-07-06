from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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

import platform

def slaveUrl(url):
  opts = Options()
  opts.add_argument("--headless")
  opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0")

  headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
  }

  sistema = platform.system()


  if sistema == "Linux":
    print("Estamos en {}".format(sistema))
    driver = webdriver.Chrome('./firefox/geckodriver',options=opts)
  else:
    print("Estamos en {}".format(sistema))
    driver = webdriver.Chrome('./geckodriver.exe', options=opts)
    
    
    


  login_form_url = 'http://10.10.50.142:8000/login/'
  driver.get(login_form_url)

  session = requests.Session()
  print(login_form_url)

  login_form_res = session.get(login_form_url, headers=headers)

  parser_login = html.fromstring(login_form_res.text)


  token_especial = parser_login.xpath('//input[@name="csrf_token"]/@value')
  print(token_especial)

  login_url = 'http://10.10.50.142:8000/login'


  login_data = {
    "login": "raven",
    "password": "raven",
    "csrf_token": token_especial
  }

  session.post(
    login_url, 
    data=login_data, 
    headers=headers
  )


  data_url = 'http://10.10.50.142:8000/reportsjson/'
  respuesta = session.get(
    data_url, 
    headers=headers
  )

  #------------------------------------------


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

  #-------------------------------------------

  # Obtengo para descubrir el boton de la url
  #dropdown_button = driver.find_element(By.XPATH, '//li//a[@class="dropdown-toggle custom-dropdown-toggle"]')
  dropdown_button_analize = driver.find_element_by_partial_link_text('Analyze')
  # Le doy click
  dropdown_button_analize.click()

  # Obtengo para descubrir el boton de la url
  url_button = driver.find_element(By.XPATH, '//li//a[@href ="/url/"]')
  # Le doy click
  url_button.click()

  #-----------------------------------------------------------
  #rellenamos Scan URL



  analizer = url



  textarea_url = driver.find_element_by_css_selector('textarea')
  textarea_url.send_keys(analizer)

  #Choices
  choisces_0 = driver.find_element(By.XPATH, '//input[@id ="choices-0"]')
  choisces_0.click()

  choisces_2 = driver.find_element(By.XPATH, '//input[@id ="choices-2"]')
  choisces_2.click()

  choisces_3 = driver.find_element(By.XPATH, '//input[@id ="choices-3"]')
  choisces_3.click()

  choisces_4 = driver.find_element(By.XPATH, '//input[@id ="choices-4"]')
  choisces_4.click()

  choisces_5 = driver.find_element(By.XPATH, '//input[@id ="choices-5"]')
  choisces_5.click()


  select_id_tiempo= driver.find_element(By.XPATH, '//select[@id ="urltimeout"]/option[@value="5"]')
  select_id_tiempo.click()


  select_id= driver.find_element(By.XPATH, '//select[@id ="analyzertimeout"]/option[@value="30"]')
  select_id.click()

  #-------------------------------------------------------------

  # Obtengo el boton de submitandwait
  submitandwait = driver.find_element(By.XPATH, '//input[@id ="submitandwait"]')
  # Le doy click
  submitandwait.click()

  #--------------------------------------------------------------



  sleep(randint(30,33)) #quiero ver si se puede optimizar mejor






  #--------------------------------------------------------------
  print("Analisis realizado, vamos a la descarga")
  print("\n...ya pasaron los 33 segundos")







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
    contenido_json = contenido_json.replace('<div id="json">', '').replace('</div>','')
    #print(contenido_json)
    temin = contenido_json
    driver.back()
    break
  return temin  