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

def LimpiaText(cadena):
    if cadena != None and len(cadena) > 2:
        while '\n' in cadena:
            cadena = cadena[:(cadena.index('\n'))] + cadena[(cadena.index('\n'))+1:]
        
        while '  ' in cadena:
            cadena = cadena[:(cadena.index('  '))] + cadena[(cadena.index('  '))+1:]
        
        if ' ' in cadena[0] or '\n' in cadena[0]:
            cadena = cadena[1:]

        if ' ' in cadena[len(cadena)-1] or '\n' in cadena[len(cadena)-1]:
            cadena = cadena[:-1]

    return cadena
def analiza(cadena):
    for d in DesDpto:
        if d in cadena:
            OCW['Department'].append(cadena)
            return True
        
    for d in DesArea:
        if d in cadena.encode("utf-8"):
            OCW['Area'] = cadena
            return True
    for d in DesCurs:
        if d in cadena:
            OCW['Curso'].append(cadena)
            return True    
    for d in DesTitu:
        if d in cadena:
            OCW['Titulacion'] = cadena
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
        
    #DICCIONARIO DE CADA OCW {'Url':www, 'Titulacion': TituOcw}
    OCW = {'url':"",'urlStatus':True,'Titulacion':"",'University':"",'Department':[],'Autor':[],'Area':[],'UrlPrograma':"",'Material':{'Url':"",'ListOERs':[]},'Curso':[],'Date':"",'ExtraData':[]}
    
    Oer = {'Text':"",'UrlOer':""}           #Diccionario de la lista OCW['Material']['ListOERs'] 
    
    OCW['url'] = page
        
    readPage = urlopen(page).read()         #Leer pagina
    soup = BeautifulSoup(readPage)          #crear estructura BS4
    page_on = soup.find(text=re.compile("gina no existe"))
    if (page_on != None):
        OCW['urlStatus']= False
        print page, " ",OCW['urlStatus']
        continue

    
    print OCW['url']#Scrap Autores
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
                prev = LimpiaText(i_br.find_previous(text = True))
                next = LimpiaText(i_br.find_next(text = True))
                if analiza(prev) == False:
                    if len(prev) > 3: OCW['ExtraData'].append(prev)
                
                if next == br[len(br)-1].find_next(text = True):  
                    if (analiza(next) == False):
                        if len(next) > 5: OCW['ExtraData'].append(next)
            continue
        i_aux = LimpiaText(i.get_text())
        if (analiza(i_aux) == False):
            if len(i_aux) > 5: OCW['ExtraData'].append(i_aux)
    OCW['Date'] =  LimpiaText(i.get_text())
    
    #Scrap URL Programa - Programme 
    for i in soup.select('dl#portlet-simple-nav dd.portletItem a[title="Programa"]'):
        OCW['UrlPrograma'] = i.get('href')
    for i in soup.select('dl#portlet-simple-nav dd.portletItem a[title="Programme"]'): #Ingles
        OCW['UrlPrograma'] = i.get('href')
    
    #Scrap URL Material
    for i in soup.select('dl#portlet-simple-nav dd.portletItem a[title^="Material"]'):
        OCW['Material']['Url'] = i.get('href')

    if OCW['Material']['Url'] != "" and OCW['Material']['Url'] != OCW['url']:
        readPage = urlopen(OCW['Material']['Url']).read()       #Leer pagina de Materiales del Curso
        soupMat = BeautifulSoup(readPage)                       #crear estructura BS4
        cont = soupMat.select('#content-core #parent-fieldname-text')   #busca id que contien OERs dentro
        lis = cont[0].find_all('li')                            #busca etiquetas li 
        for i in lis:  
            Oer['Text']=LimpiaText(i.get_text())
            if i.a != None:
                Oer['UrlOer']=i.a.get('href')
            OCW['Material']['ListOERs'].append(Oer)
            Oer = {'Text':"",'UrlOer':""}     
        
    print "TIT>",OCW['Titulacion']
    print "UNI>",OCW['University']
    for d in OCW['Department']:
        print "DEP>", d
    for d in OCW['Autor']:
        print "AUT>", d
    for d in OCW['Curso']:
        print "CUR>", d
    print "UPR>",OCW['UrlPrograma']
    print "UMT>",OCW['Material']['Url']
    print "FCH>",OCW['Date']
    for d in OCW['Curso']:
        print "CUR>", d
    for i in OCW['Material']['ListOERs']:
        print "*OERT>",i['Text']
        print "*OERU>",i['UrlOer']
        print ""
    for d in OCW['ExtraData']:
        print "EXT>", d
    print "\n"
