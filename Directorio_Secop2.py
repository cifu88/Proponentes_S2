#Librerias:
from flask import Flask, request, make_response, redirect, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import psycopg2
import numpy as np

#------------------------------------------------------------------------------------------------------------------------------------------

#Variables almacenar datos:

## Directorios de códigos Secop 2
directorio = []
nuevo_directorio = []

## Contratista:
url_usuario = []
cod_entidad = []
proponentes_plurales = []
nombre_entidad = []
nombre_abreviado = []
tipo_doc = []
numero_doc = []
tipo_entidad = []
nom_rep_legal = []
id_rep_legal = []
nacionalidad_rep_legal = []
domicilio_rep_legal = []
tipo_documento_rep_legal = []
genero_rep_legal = []
mipyme = []
tamaño_empresarial = []
regimen_tributario = []
emprendimiento_mujer = []
pais = []
ubicacion = []
cod_postal = []
correo_electronico_oficina = []
tel_oficina = []
fax_oficina = []
pag_web = []
Lista_Xpath = [
    '//*[@id="frmMainForm_tblFormContainer_trContentRow_tdLeftColumn_divViewProfilePerspective_tblProfileDetails_trIsNotGroupContentRow_tdTitleCell"]', #0ProponentesPlurales
    '//*[@id="spnLegalName_0_0"]', 
    '//*[@id="spnCommercialName_0_1"]',
    '//*[@id="selTypeOfDocument_0_2"]',
    '//*[@id="spnVAT_0_3"]',
    '//*[@id="spnCompanyType_0_4"]',
    '//*[@id="spnCustomTextBox_1_0"]',
    '//*[@id="spnCustomTextBox_1_1"]',
    '//*[@id="spnCustomTextBox_1_2"]', 
    '//*[@id="spnCustomTextBox_1_3"]',
    '//*[@id="spnCustomSelectOptionValue_1_4"]',
    '//*[@id="spnCustomSelectOptionValue_1_5"]',
    '//*[@id="spnIsSmallCompany_2_0"]',
    '//*[@id="spnCompanySize_2_0"]',
    '//*[@id="selTaxSystem_2_1"]',
    '//*[@id="rdbgCustomTrueOrFalse_2_2_0"]',
    '//*[@id="txtCountryElement_3_0"]',
    '//*[@id="spnLocationElement1_3_1"]',
    '//*[@id="spnLocationElement2_3_1"]',
    '//*[@id="spnLocationElement3_3_1"]',
    '//*[@id="spnZipCode_3_2"]',
    '//*[@id="spnEmail_3_3"]',
    '//*[@id="spnPhone_3_4"]',
    '//*[@id="spnFax_3_5"]',
    '//*[@id="spnWebAddress_3_6"]']

## Unión temporal o Consorcio:
url_pro_plu = []
cod_pro_plu = []
nom_pro_plu = []
nom_abr_pro_plu = []
tip_ent_pro_plu = []
ubi_pro_plu = []
email_pro_plu = []
tel_pro_plu = []
url_pro_plu = []
Lista_Xpath_pro_plu = [
    '//*[@id="spnLegalName_0_0"]',
    '//*[@id="spnCommercialName_0_1"]',
    '//*[@id="frmMainForm_tblFormContainer_trContentRow_tdLeftColumn_divViewProfilePerspective_tblProfileDetails_trIsGroupContentRow_tdTitleCell_rptIsGroupRepeater_rpteIsGroupConditionalElements_lnkIsGroupConditionalSpan_0"]',
    '//*[@id="spnCompanyType_0_4"]',
    '//*[@id="spnLocationElement1_3_1"]',
    '//*[@id="spnEmail_3_3"]',
    '//*[@id="spnPhone_3_4"]']

## Tabla de unión:
cod_pro_plu = []
cod_contratista = []
porc_contratista = []
jefe = []

#------------------------------------------------------------------------------------------------------------------------------------------

# Funciones

## Funcion para validar la existencia de los datos:
def validar(Lista_Xpath, Lista_Guardar):
    for Xpath in Lista_Xpath:
        try:
            elemen = driver.find_element(by=By.XPATH, value=Xpath)
            Lista_Guardar.append(elemen.text)
        except NoSuchElementException:
            elemen = 'N/A'
            Lista_Guardar.append(elemen)
    return(Lista_Guardar)


#------------------------------------------------------------------------------------------------------------------------------------------

# Extraer información del directorio en bd:
try:
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='Santi913752',
        database='Proponentes'
    )
    print("Conectado")
    #Contrato
    cursor = connection.cursor()
    cursor.execute('SELECT cod_num FROM public."Codigos_s2"')
    for fila in cursor:
        codigo = str(fila[0])
        directorio.append(codigo)
        print(type(codigo))
except Exception as ex:
    print(ex)
finally:
    connection.close()

#Scrapping:



## Creación del robot (driver):
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
driver = webdriver.Chrome(options=options)
try:
    for codigo in directorio:
        url_directorio = 'https://community.secop.gov.co/Directory/Profile/' + codigo
        
        driver.get(url_directorio)
        if driver.current_url != url_directorio:
            user = 'cifu888'
            passw = 'Cifu06022002;::'
            input_user = driver.find_element(by=By.XPATH, value='//*[@id="txtUserName"]').send_keys(user)
            input_passw = driver.find_element(by=By.XPATH, value='//*[@id="txtPassword"]').send_keys(passw)
            Btn_Entrar = driver.find_element(by=By.XPATH, value='//*[@id="btnLoginButton"]').click()
            time.sleep(5)
            ## Verificar si es contratista o consorcio

            xpath_contratista = '//*[@id="spnGroupsThatCompanyIsMemberGen"]'
            try:
                if xpath_contratista in driver.page_source:
                    print('Contratista')
                    lista_proponente = []
                    validar(Lista_Xpath,lista_proponente)
                    url_usuario.append(driver.current_url)
                    for i in range (len(lista_proponente)):
                        if i == 0:
                            proponentes=driver.find_elements(by=By.XPATH, value='//*[@id="frmMainForm_tblFormContainer_trContentRow_tdLeftColumn_divViewProfilePerspective_tblProfileDetails_trIsNotGroupContentRow_tdTitleCell"]')
                            if len(proponentes) > 1:
                                conjunto_proponentes = []
                                for proponente in proponentes:
                                    conjunto_proponentes.append(proponente.text)
                                proponentes_plurales.append(conjunto_proponentes)
                                print(proponentes_plurales)
                                for pro_plu in range(len(proponentes_plurales)):
                                    consorcio = driver.find_element(by=By.XPATH(f'//*[@id="lnkIsNotGroupConditionalSpan_{pro_plu}"]'))
                                    time.sleep(2)
                                    nom_pro_plu.append(consorcio.get_attribute('supportOptions'))
                                print(nom_pro_plu)                           
                            else:
                                proponentes_plurales.append(lista_proponente[i])
                            print(proponentes_plurales)
                        elif i == 1:
                            nombre_entidad.append(lista_proponente[i])
                            print(nombre_entidad)
                        elif i == 2:
                            nombre_abreviado.append(lista_proponente[i])
                            print(nombre_abreviado)
                        elif i == 3:
                            tipo_doc.append(lista_proponente[i])
                            print(tipo_doc)
                        elif i == 4:
                            numero_doc.append(lista_proponente[i])
                            print(numero_doc)
                        elif i == 5:
                            tipo_entidad.append(lista_proponente[i])
                            print(tipo_entidad)
                        elif i == 6:
                            nom_rep_legal.append(lista_proponente[i])
                            print(nom_rep_legal)
                        elif i == 7:
                            id_rep_legal.append(lista_proponente[i])
                            print(id_rep_legal)
                        elif i == 8:
                            nacionalidad_rep_legal.append(lista_proponente[i])
                            print(nacionalidad_rep_legal)
                        elif i == 9:
                            domicilio_rep_legal.append(lista_proponente[i])
                            print(domicilio_rep_legal)
                        elif i == 10:
                            tipo_documento_rep_legal.append(lista_proponente[i])
                            print(tipo_documento_rep_legal)
                        elif i == 11:
                            genero_rep_legal.append(lista_proponente[i])
                            print(genero_rep_legal)
                        elif i == 12:
                            mipyme.append(lista_proponente[i])
                            print(mipyme)
                        elif i == 13:
                            tamaño_empresarial.append(lista_proponente[i])
                            print(tamaño_empresarial)
                        elif i == 14:
                            regimen_tributario.append(lista_proponente[i])
                            print(regimen_tributario)
                        elif i == 15:
                            try:
                                mujer = driver.find_element(by=By.XPATH, value='//*[@id="rdbgCustomTrueOrFalse_2_2_0"]').get_attribute(name='checked')
                                if mujer == True:    
                                    emprendimiento_mujer.append('Si')
                                else:
                                    emprendimiento_mujer.append('No')
                            except Exception as ex:
                                print(ex)
                            print(emprendimiento_mujer)
                        elif i == 16:
                            pais.append(lista_proponente[i])
                            print(pais)
                        elif i == 17:
                            ubi = lista_proponente[i]
                            if lista_proponente[18] != 'N/A':
                                ubi += "" + lista_proponente[18]
                            if lista_proponente[19] != 'N/A':
                                ubi += "" + lista_proponente[19]
                            ubi = ubi.replace('N/A',"")
                            ubicacion.append(ubi)
                            print(ubicacion)
                        elif i == 20:
                            cod_postal.append(lista_proponente[i])
                            print(cod_postal)
                        elif i == 21:
                            correo_electronico_oficina.append(lista_proponente[i])
                            print(correo_electronico_oficina)
                        elif i == 22:
                            tel_oficina.append(lista_proponente[i])
                            print(tel_oficina)
                        elif i == 23:
                            fax_oficina.append(lista_proponente[i])
                            print(fax_oficina)
                        elif i == 24:
                            pag_web.append(lista_proponente[i])
                            print(pag_web)
                        
                        

                       
                        time.sleep(5)
                
            except Exception as ex:
                print(ex)
        print('Exito para el contratista: ', codigo)
        
except Exception as ex:
    print(ex)

"""## Verificar si es contratista o consorcio

xpath_contratista = '//*[@id="spnGroupsThatCompanyIsMemberGen"]'
try:
    if xpath_contratista in driver.page_source:
        print('Contratista')
        lista_proponente = []
        validar(Lista_Xpath,lista_proponente)
        url_usuario.append(driver.current_url)
        for i in range (len(lista_proponente)):
            if i == 0:
                proponentes=driver.find_elements(by=By.XPATH, value='//*[@id="frmMainForm_tblFormContainer_trContentRow_tdLeftColumn_divViewProfilePerspective_tblProfileDetails_trIsNotGroupContentRow_tdTitleCell"]')
                if len(proponentes) > 1:
                    conjunto_proponentes = []
                    for proponente in proponentes:
                        conjunto_proponentes.append(proponente.text)
                    proponentes_plurales.append(conjunto_proponentes)
                    for pro_plu in range(len(proponentes_plurales)):
                        driver.find_element(by=By.XPATH(f'//*[@id="lnkIsNotGroupConditionalSpan_{pro_plu}"]'))
                        time.sleep(2)
                        nom_pro_plu.append()                              
                else:
                    proponentes_plurales.append(lista_proponente[i])
            elif i == 1:
                nombre_entidad.append(lista_proponente[i])
            elif i == 2:
                nombre_abreviado.append(lista_proponente[i])
            elif i == 3:
                tipo_doc.append(lista_proponente[i])
            elif i == 4:
                numero_doc.append(lista_proponente[i])
            elif i == 5:
                tipo_entidad.append(lista_proponente[i])
            elif i == 6:
                nom_rep_legal.append(lista_proponente[i])
            elif i == 7:
                id_rep_legal.append(lista_proponente[i])
            elif i == 8:
                nacionalidad_rep_legal.append(lista_proponente[i])
            elif i == 9:
                domicilio_rep_legal.append(lista_proponente[i])
            elif i == 10:
                tipo_documento_rep_legal.append(lista_proponente[i])
            elif i == 11:
                genero_rep_legal.append(lista_proponente[i])
            elif i == 12:
                mipyme.append(lista_proponente[i])
            elif i == 13:
                tamaño_empresarial.append(lista_proponente[i])
            elif i == 14:
                regimen_tributario.append(lista_proponente[i])
            elif i == 15:
                try:
                    mujer = driver.find_element(by=By.XPATH, value='//*[@id="rdbgCustomTrueOrFalse_2_2_0"]').get_attribute(name='checked')
                    if mujer == True:    
                        emprendimiento_mujer.append('Si')
                    else:
                        emprendimiento_mujer.append('No')
                except Exception as ex:
                    print(ex)
            elif i == 16:
                pais.append(lista_proponente[i])
            elif i == 17:
                ubi = lista_proponente[i]
                if lista_proponente[18] != 'N/A':
                    ubi += "" + lista_proponente[18]
                if lista_proponente[19] != 'N/A':
                    ubi += "" + lista_proponente[19]
                ubi = ubi.replace('N/A',"")
                ubicacion.append(ubi)
            elif i == 20:
                cod_postal.append(lista_proponente[i])
            elif i == 21:
                correo_electronico_oficina.append(lista_proponente[i])
            elif i == 22:
                tel_oficina.append(lista_proponente[i])
            elif i == 23:
                fax_oficina.append(lista_proponente[i])
            elif i == 24:
                pag_web.append(lista_proponente[i])
            
            valores_contratista= {
            'Url usuario':url_usuario,
            'Proponentes plurales':proponentes_plurales,
            'Nombre entidad':nombre_entidad,
            'Nombre abreviado':nombre_abreviado,
            'Tipo documento':tipo_doc,
            'Numero documento':numero_doc,
            'Tipo entidad':tipo_entidad,
            'Representante legal':nom_rep_legal,
            'Doc representante legal':id_rep_legal,
            'Nacionalidad Representante legal':nacionalidad_rep_legal,
            'Domicilio representante legal':domicilio_rep_legal,
            'Tipo documento rep legal':tipo_documento_rep_legal,
            'genero':genero_rep_legal,
            'MiPymes':mipyme,
            'Tamaño empresarial':tamaño_empresarial,
            'Regimen tributario':regimen_tributario,
            'Emprendimiento mujer':emprendimiento_mujer,
            'Pais':pais,
            'Ubicacion':ubicacion,
            'Codigo postal':cod_postal,
            'Correo':correo_electronico_oficina,
            'Telefono':tel_oficina,
            'Fax':fax_oficina,
            'Pagina':pag_web}

            
            time.sleep(5)
    
except Exception as ex:
    print(ex)"""
    
valores_contratista= {
                        'Url usuario':url_usuario,
                        'Proponentes plurales':proponentes_plurales,
                        'Nombre entidad':nombre_entidad,
                        'Nombre abreviado':nombre_abreviado,
                        'Tipo documento':tipo_doc,
                        'Numero documento':numero_doc,
                        'Tipo entidad':tipo_entidad,
                        'Representante legal':nom_rep_legal,
                        'Doc representante legal':id_rep_legal,
                        'Nacionalidad Representante legal':nacionalidad_rep_legal,
                        'Domicilio representante legal':domicilio_rep_legal,
                        'Tipo documento rep legal':tipo_documento_rep_legal,
                        'genero':genero_rep_legal,
                        'MiPymes':mipyme,
                        'Tamaño empresarial':tamaño_empresarial,
                        'Regimen tributario':regimen_tributario,
                        'Emprendimiento mujer':emprendimiento_mujer,
                        'Pais':pais,
                        'Ubicacion':ubicacion,
                        'Codigo postal':cod_postal,
                        'Correo':correo_electronico_oficina,
                        'Telefono':tel_oficina,
                        'Fax':fax_oficina,
                        'Pagina':pag_web}
df_secopii_contratista = pd.DataFrame(valores_contratista)
print(df_secopii_contratista)
driver.close()