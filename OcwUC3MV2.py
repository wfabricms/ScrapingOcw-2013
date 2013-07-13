# coding: utf-8
#-*- encoding utf-8 -*-
from bs4 import *
from urllib import urlopen
import re
from URLs import *

#Descripciones de la categorías en las páginas
DesDpto = ["Dpto", "dpto", "Departamento", "departamento", "epartment"]
DesArea = ["Área", "Area", "AREA", "ÁREA"]
DesCurs = ["Curso", "CURSO", "curso"]
DesTitu = ["Titulaci", "TITULACI", "titulaci"]
DesUniv = ["Universidad", "universidad"]


def analiza(cadena):
    for d in DesDpto:
        if d in cadena:
            OCW['Department'] = cadena
            return True
        
    for d in DesArea:
        if d in cadena.encode("utf-8"):
            OCW['Area'] = cadena
            return True
    for d in DesCurs:
        if d in cadena:
            OCW['Curso'] = cadena
            return True    
    for d in DesTitu:
        if d in cadena:
            OCW['Title'] = cadena
            return True    
    for d in DesUniv:
        if d in cadena:
            OCW['University'] = cadena
            return True
    return False
       
#Host
host = "" #"http://localhost/ocw/"

#paginas web
pages = PagesUC3M
pagasaux = ['http://ocw.uc3m.es/ciencia-e-oin/tecnologia-de-materiales-industriales']
for page in pages:    
    print  "\n"
    #LISTA PRINCIPAL [{OCW},{OCW},{OCW},{OCW}]
    ListaOcw = []
        
    #DICCIONARIO DE CADA OCW {'Url':www, 'Title': TituOcw}
    OCW = {'url':"",'urlStatus':True,'Title':"",'University':"",'Department':[],'Autor':[],'Area':[],'UrlPrograma':[],'Material':{'Url':"",'ListOERs':[]},'Curso':[],'Date':"",'ExtraData':[]}
    
    Oer = {'Text':"",'UrlOer':""}           #Diccionario de la lista OCW['Material']['ListOERs'] 
    
    OCW['url'] = page
        
    readPage = urlopen(page).read()         #Leer pagina
    soup = BeautifulSoup(readPage)          #crear estructura BS4
    page_on = soup.find(text=re.compile("gina no existe"))
    if (page_on != None):
        OCW['urlStatus']= False
        print page, " ",OCW['urlStatus']
        continue

    #Scrap Autores
    by = soup.select('#authors div')
    #Procesar texto de Autores  (elimina ':' ',')  
    autoresText = by[0].string
    aut = autoresText[(autoresText.index(':')+2):]
    while ',' in aut:
        OCW['Autor'].append(aut[:(aut.index(','))])
        aut = aut[(aut.index(',')+2):]
    OCW['Autor'].append(aut)    
    data = soup.select('#aboutDeptInfo p')    
    for i in data:
        br = []
        br = i.select("br")
        if len(br) >= 1:
            for i_br in br:
                if (analiza(i_br.find_previous(text = True)) == False):
                    OCW['ExtraData'].append(i_br.find_previous(text = True))
                if (i_br.find_next(text = True) == br[len(br)-1].find_next(text = True)):  
                    if (analiza(i_br.find_next(text = True)) == False):
                        OCW['ExtraData'].append(i_br.find_next(text = True))
            continue
        if (analiza(i.get_text()) == False):
            OCW['ExtraData'].append(i.get_text())
    OCW['Date'] =  i.get_text()
    
    #Scrap URL Programa - Programme 
    for i in soup.select('dl#portlet-simple-nav dd.portletItem a[title="Programa"]'):
        OCW['UrlPrograma'] = i.get('href')
    for i in soup.select('dl#portlet-simple-nav dd.portletItem a[title="Programme"]'): #Ingles
        OCW['UrlPrograma'] = i.get('href')
    
    #Scrap URL Material
    for i in soup.select('dl#portlet-simple-nav dd.portletItem a[title^="Material"]'):
        OCW['Material']['Url'] = i.get('href')
    
    print OCW['url']
    print OCW['Material']['Url']
    
    if OCW['Material']['Url'] != "" and OCW['Material']['Url'] != OCW['url']:
        readPage = urlopen(OCW['Material']['Url']).read()       #Leer pagina de Materiales del Curso
        soupMat = BeautifulSoup(readPage)                       #crear estructura BS4
        cont = soupMat.select('#content-core #parent-fieldname-text')   #busca id que contien OERs dentro
        lis = cont[0].find_all('li')                            #busca etiquetas li 
        for i in lis:  
            Oer['Text']=i.get_text()
            if i.a != None:
                Oer['UrlOer']=i.a.get('href')
            OCW['Material']['ListOERs'].append(Oer)
            Oer = {'Text':"",'UrlOer':""}     
            
        

    for i in OCW['Material']['ListOERs']:
        print i['Text'], " > ",i['UrlOer']
