# coding: utf-8
#-*- encoding utf-8 -*-
from bs4 import *
from urllib import urlopen
import re
from URLs import *

#Ambiguedades comunes de los valores 
DesDpto = ["Dpto", "dpto", "Departamento", "departamento", "epartment", "epartamiento"]
DesArea = ["Área", "Area", "AREA", "ÁREA"]
DesFacu = ["Facultad", "facultad"]
DesDate = ["fecha","Fecha"]
DesScho = ["Escuela","ETS"]

def CompruebaOer(UrlOer, ListOERs ):
    if UrlOer == None or len(UrlOer) < 3:
        return False    #DEVUELVE FASO EN CASO DE QUE EL OER SEA MUY CORTO EN TASL COSO NO ES UN LINK

    for ind in ListOERs:
        if UrlOer == ind['UrlOer']:
            return False # DEVUELVE FALSO EN CASO DE QUE EL OER YA EXISTA EN TAL CASO NO SE INSERTA
    return True #DEVUELVE FALSO EN CASO DE QUE EL OER NO EXISTA EN LISTA PARA SER INSERTADO

def LimpiaText(cadena):
    if cadena != None and len(cadena) > 2:
        while '\r' in cadena:
            cadena = cadena[:(cadena.index('\r'))] + cadena[(cadena.index('\r'))+1:]
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
host = "" #"http://localhost/ocw/" 
#paginas web
pages = PagesUCalifornia
pagesaux = ['http://ocwus.us.es/ciencias-y-tecnicas-historiograficas/archivistica-y-biblioteconomia']
for page in pages:    
    #LISTA PRINCIPAL [{OCW},{OCW},{OCW},{OCW}]
    ListaOcw = []
    #DICCIONARIO DE CADA OCW {'Url':www, 'Title': TituOcw}
    OCW = {'url':"",'urlStatus':True,'Title':"" ,'Department':"",'Author':"",'AutURL':"",'AutTitle':"",'Area':[],'Faculty':[],'UrlProgram':"",'Material':{'Url':"",'ListOERs':[]},'Date':"",'ExtraData':[]}
    
    Auth = {'Name':"",'URL':""}
    Oer = {'Text':"",'UrlOer':""}           #Diccionario de la lista OCW['Material']['ListOERs'] 
    
    OCW['url'] = page
        
    readPage = urlopen(page).read()         #Leer pagina
    soup = BeautifulSoup(readPage)          #crear estructura BS4
    page_on = soup.find(text=re.compile("o matches were found for your search crite"))
    
    
    if (page_on != None):
        OCW['urlStatus']= False
        print page, " ",OCW['urlStatus']
        continue
                
    print "URL> ",OCW['url']
    OCW['Title'] = LimpiaText(soup.title.get_text())
    
    #Scrap Autores
    
    data = soup.select('div.columnleft_nomiddle blockquote table')[0]
    
    by = data.find(text=re.compile("Author")).parent.parent
    if by == None: by = data.find(text=re.compile("author")).parent.parent
    
    
    OCW['Author'] = LimpiaText(by.select('a')[0].get_text())
    OCW['AutURL'] = by.select('a')[0].get('href')
    
    
    title = data.find(text=re.compile("Title")).parent.parent
    if title == None: title = data.find(text=re.compile("title")).parent.parent
    
    OCW['AutTitle'] = LimpiaText(title.get_text())
    
    Dept = data.find(text=re.compile("Department")).parent.parent
    if Dept == None: Dept = data.find(text=re.compile("department")).parent.parent
    
    OCW['Department'] = LimpiaText(Dept.get_text())
    
    print OCW['Author']
    print OCW['AutURL']
    print OCW['AutTitle']
    print OCW['Department']
    print "\n"
    
    
    
    
    #OCW['Autor'].append(by[0].get_text())
    
    
    """#Procesar texto de Autores  (elimina ':' ',')  
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
                    if len(textp[:textp.index('\n')]) > 3: OCW['ExtraData'].append(textp[:textp.index('\n')])
                textp = textp[textp.index('\n')+1:]
        if analiza(textp) != True:
                if len(textp) > 3: OCW['ExtraData'].append(textp)
    #Scrap URL Material y URL Programa
    for i in soup.select('div#portlet-eduCommonsNavigation a'):
        if "Material de clase" in i.get_text() or "Material del curso" in i.get_text() or "Material de Clase" in i.get_text():
            OCW['Material']['Url'] = i.get('href')
        if "Programa" in i.get_text():
            OCW['UrlProgram'] = i.get('href')
    readPage = urlopen(OCW['Material']['Url']).read()       #Leer pagina de Materiales del Curso
    soupMat = BeautifulSoup(readPage)                       #crear estructura BS4
    cont = soupMat.select('div#region-content div.plain')   #busca OERs dentro
    for a in cont[0].select('a'):
        if len(OCW['Material']['ListOERs']) > 0 != None and OCW['Material']['ListOERs'][len(OCW['Material']['ListOERs'])-1]['UrlOer'] == a.get('href'):
            OCW['Material']['ListOERs'][len(OCW['Material']['ListOERs'])-1]['Text'] = LimpiaText(a.get_text())
        else:
            if CompruebaOer(a.get('href'), OCW['Material']['ListOERs']):
                Oer['UrlOer']=a.get('href')
                Oer['Text'] = LimpiaText(a.get_text())
                OCW['Material']['ListOERs'].append(Oer)
                Oer = {'Text':"",'UrlOer':""} 
    #IMPRIMIR
    
    print "TL> ", OCW['Title']
    for d in OCW['Department']:
        print "DP> ",d

    for autor in OCW['Autor']:
        print "AU> ",LimpiaText(autor)
    for s in OCW['School']:
        print "SH> ",s 
    for area in OCW['Area']:
        print "AR> ",area 
    for f in OCW['Faculty']:
        print "FA> ",f 
    print "UP> ",OCW['UrlProgram']
    print "UM> ",OCW['Material']['Url']
    if OCW['Date'] != "":   print "FE> ",OCW['Date']
    for mat in OCW['Material']['ListOERs']:
        for ind in mat:
            print "  > ", ind , ": ", mat[ind]

    for ind in OCW['ExtraData']:
        print "EX> ",ind"""
