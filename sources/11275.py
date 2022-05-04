'''
Los enlaces se deben generar usando el siguiente formato:
http://svrpubindc.imprenta.gov.co/senado/index2.xhtml?ent=Cámara&fec=20-8-2020&num=754

donde:

* Cámara lleva acento, ej. ent=Cámara
* Día y mes no anteponen 0, ej. fec=1-1-2020
* Número de gaceta antepone 0 si es un dígito, ej. num=03
'''

import time
from selenium import webdriver


driver = webdriver.Safari()

with open('/Users/santiagofacchini/Downloads/enlaces-2020.txt', 'r') as txt_file:
    txt_content = txt_file.read()

links = txt_content.split('\n')

for link in links:
    print(link)
    driver.get(link)

    # Esperar hasta que comience la descarga
    time.sleep(1)

driver.close()
