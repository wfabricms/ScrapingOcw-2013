# coding: utf-8
#-*- encoding utf-8 -*-
from bs4 import *
from urllib import urlopen
import re
from URLs import *

#Descripciones de la categorías en las páginas
DesDpto = ["Dpto", "dpto", "Departamento", "departamento", "epartment"]
DesArea = ["Área", "Area", "AREA", "ÁREA"]
DesFacu = ["Facultad", "facultad","Escuela","escuela"]
DesDate = ["fecha","Fecha"]

def QuitaSalto(cadena):
    print "cadena: ",cadena
    if cadena != None and len(cadena) > 0:
        if (cadena[0] == '\n'): 
            cadena = cadena[1:]
    return cadena

def analiza(cadena):
    #print len(cadena)," ", cadena
    if len(cadena) > 0:
        if (cadena[0] == '\n'): 
            cadena == cadena[1:]

        for d in DesDpto:
            if d in cadena:
                OCW['Department'] = cadena
                return True
            
        for d in DesArea:
            if d in cadena.encode("utf-8"):
                OCW['Area'] = cadena
                return True   

        for d in DesFacu:
            if d in cadena:
                OCW['Facultad'] = cadena
                return True

        for d in DesDate:
            if d in cadena:
                OCW['Date'] = cadena
                return True    
    return False
       
#Host
host = "" #"http://localhost/ocw/" degree

#paginas web
pages = pagesUSevilla
pagasaux = ['']
for page in pages:    
    # print  "\n"
    #LISTA PRINCIPAL [{OCW},{OCW},{OCW},{OCW}]
    ListaOcw = []
        
    #DICCIONARIO DE CADA OCW {'Url':www, 'Title': TituOcw}
    OCW = {'url':"",'urlStatus':True,'Department':[],'Autor':[],'Area':[],'Facultad':"",'UrlPrograma':[],'Material':{'Url':"",'ListOERs':[]},'Date':"",'ExtraData':[]}
    
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
    by = soup.select('div.objectMetadata')
    #Procesar texto de Autores  (elimina ':' ',')  
    autoresText = by[0].get_text()
    aut = autoresText[(autoresText.index(':')+2):]
    while ',' in aut:
        OCW['Autor'].append(aut[:(aut.index(','))])
        aut = aut[(aut.index(',')+2):]
    OCW['Autor'].append(aut) 
    
    #for i in OCW['Autor']: 
    #    print ">>",i
       
    data = soup.select('#aboutDeptInfo p')
    #print "DATA", data   
    if data == []:
        data = soup.select('#aboutInfo p')   
    #print page 
    for i in data:
        textp = i.get_text()
        index = 0
        if '\n' in textp:
            while '\n' in textp:
                if analiza(textp[:textp.index('\n')]) != True:
                    OCW['ExtraData'].append(textp[:textp.index('\n')])
                textp = textp[textp.index('\n')+1:]

        if analiza(textp) != True:
                OCW['ExtraData'].append(textp)
    
    #Scrap URL Programa - Programme 
    for i in soup.select('dl#portlet-simple-nav dd.portletItem a[href="Programa"]'):
        OCW['UrlPrograma'] = i.get('href')
    for i in soup.select('dl#portlet-simple-nav dd.portletItem a[href="Programme"]'): #Ingles
        OCW['UrlPrograma'] = i.get('href')
    
    #Scrap URL Material
    for i in soup.select('div#portlet-eduCommonsNavigation a'):
        if "Material de clase" in i.get_text() or "Material del curso" in i.get_text() or "Material de Clase" in i.get_text():
            #print "Material - ", i
            OCW['Material']['Url'] = i.get('href')

    if (OCW['Material']['Url'] == ""):
        print page
        print OCW['Material']['Url']
    #for i in OCW.keys():
        #print ">>",i," - ", OCW[i]
        
    readPage = urlopen(OCW['Material']['Url']).read()       #Leer pagina de Materiales del Curso
    soupMat = BeautifulSoup(readPage)                       #crear estructura BS4
    cont = soupMat.select('div#region-content div.plain')   #busca OERs dentro
    print OCW['Material']['Url']
    aa = cont[0].select('a')
    for a in aa:
        print a
        Oer['UrlOer']=QuitaSalto(a.get('href'))
        Oer['Text']=QuitaSalto(a.get_text())
        OCW['Material']['ListOERs'].append(Oer)
        Oer = {'Text':"",'UrlOer':""}   

    for i in OCW['Material']['ListOERs']:
        print "> ",i['Text'], " : ",i['UrlOer']
