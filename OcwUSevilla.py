# coding: utf-8
#-*- encoding utf-8 -*-
from bs4 import *
from urllib import urlopen
import re
from URLs import *

#Ambiguedades comunes de los valores 
DesDpto = ["Dpto", "dpto", "Departamento", "departamento", "epartment"]
DesArea = ["Área", "Area", "AREA", "ÁREA"]
DesFacu = ["Facultad", "facultad"]
DesDate = ["fecha","Fecha"]
DesScho = ["Escuela","ETS"]

def CompruebaOer(UrlOer, ListOERs ):
    if len(UrlOer) < 3:
        return False

    for ind in ListOERs:
        if UrlOer == ind['UrlOer']:
            return False
    return True

def QuitaSalto(cadena):
    if cadena != None and len(cadena) > 0:
        #if (cadena[0] == '\n'): 
            #cadena = cadena[1:]
        while '\n' in cadena:
            cadena = cadena[:(cadena.index('\n'))] + cadena[(cadena.index('\n'))+1:]

    return cadena

def analiza(cadena):
    if len(cadena) > 0:
        if (cadena[0] == '\n'): 
            cadena == cadena[1:]

        for d in DesDpto:
            if d in cadena:
                OCW['Department'].append(cadena)
                return True
            
        for d in DesArea:
            if d in cadena.encode("utf-8"):
                OCW['Area'].append(cadena)
                return True   

        for d in DesFacu:
            if d in cadena:
                OCW['Faculty'].append(cadena)
                return True

        for d in DesDate:
            if d in cadena:
                OCW['Date'] = cadena
                return True
        for d in DesScho:
            if d in cadena:
                OCW['School'].append(cadena)
                return True    
    return False
       
#Host
host = "" #"http://localhost/ocw/" degree
#paginas web
pages = pagesUSevilla
pagasaux = ['']
for page in pages:    
    #LISTA PRINCIPAL [{OCW},{OCW},{OCW},{OCW}]
    ListaOcw = []
    #DICCIONARIO DE CADA OCW {'Url':www, 'Title': TituOcw}
    OCW = {'url':"",'urlStatus':True,'Department':[],'Autor':[],'School':[],'Area':[],'Faculty':[],'UrlProgram':"",'Material':{'Url':"",'ListOERs':[]},'Date':"",'ExtraData':[]}
    
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
    data = soup.select('#aboutDeptInfo p')
    if data == []:
        data = soup.select('#aboutInfo p')   
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
    #Scrap URL Material y URL Programa
    for i in soup.select('div#portlet-eduCommonsNavigation a'):
        if "Material de clase" in i.get_text() or "Material del curso" in i.get_text() or "Material de Clase" in i.get_text():
            OCW['Material']['Url'] = i.get('href')
        if "Programa" in i.get_text():
            OCW['UrlProgram'] = i.get('href')
    readPage = urlopen(OCW['Material']['Url']).read()       #Leer pagina de Materiales del Curso
    soupMat = BeautifulSoup(readPage)                       #crear estructura BS4
    cont = soupMat.select('div#region-content div.plain')   #busca OERs dentro
    aa = cont[0].select('a')
    latestOer = ""
    for a in aa:
        if latestOer != "" and latestOer == a.get('href'):
            OCW['Material']['ListOERs'][len(OCW['Material']['ListOERs'])-1]['Text'] = QuitaSalto(a.get_text())
        else:
            Oer['UrlOer']=QuitaSalto(a.get('href'))
            Oer['Text']=QuitaSalto(a.get_text())
            OCW['Material']['ListOERs'].append(Oer)
            Oer = {'Text':"",'UrlOer':""} 
        latestOer = a.get('href')

    #IMPRIMIR
    print "> ",OCW['url']
    """for d in OCW['Department']:
        print "> ",d
    for autor in OCW['Autor']:
        print "> ",QuitaSalto(autor)
    for s in OCW['School']:
        print "> ",s 
    for area in OCW['Area']:
        print "> ",area 
    for f in OCW['Faculty']:
        print "> ",f 
    print "> ",OCW['UrlProgram']
    print "> ",OCW['Material']['Url']
    print "> ",OCW['Date']
    for mat in OCW['Material']['ListOERs']:
        for ind in mat:
            print ind , ": ", mat[ind]"""


    for ind in OCW['ExtraData']:
        print "> ",ind

