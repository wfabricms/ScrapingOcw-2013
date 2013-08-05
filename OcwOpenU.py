# coding: utf-8
#-*- encoding utf-8 -*-
from bs4 import *
from urllib import urlopen
import re
from URLs import *

#Ambiguedades comunes de los valores 
DesDur = ["Duration"]
DesLev = ["Level"]
DesPub = ["Published"]

def CompruebaOer(UrlOer, ListOERs ):
    if UrlOer == None or len(UrlOer) < 3:
        return False    #DEVUELVE FASO EN CASO DE QUE EL OER SEA MUY CORTO EN TASL COSO NO ES UN LINK

    for ind in ListOERs:
        if UrlOer == ind['UrlOer']:
            return False # DEVUELVE FALSO EN CASO DE QUE EL OER YA EXISTA EN TAL CASO NO SE INSERTA
    return True #DEVUELVE FALSO EN CASO DE QUE EL OER NO EXISTA EN LISTA PARA SER INSERTADO

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
    if len(cadena) > 0:
        if (cadena[0] == '\n'): 
            cadena == cadena[1:]

        for d in DesDur:
            if d in cadena:
                OCW['Duration'] = cadena
                return True
            
        for d in DesLev:
            if d in cadena:
                OCW['Level'] = cadena
                return True   

        for d in DesPub:
            if d in cadena:
                OCW['Date'] = cadena
                return True

    return False
       
#Host
host = "" #"http://localhost/ocw/" 
#paginas web
pages = PagesOpenU
pagesaux = ['http://ocwus.us.es/ciencias-y-tecnicas-historiograficas/archivistica-y-biblioteconomia']
for page in pages:    
    #LISTA PRINCIPAL [{OCW},{OCW},{OCW},{OCW}]
    ListaOcw = []
    #DICCIONARIO DE CADA OCW {'Url':www, 'Title': TituOcw}
    OCW = {'url':"",'urlStatus':True,'Title':"" ,'Department':[],'Autor':[],'Duration':"",'Level':"",'Faculty':[],'UrlProgram':"",'Material':{'Url':"",'ListOERs':[]},'Date':"",'ExtraData':[]}
    
    Oer = {'Text':"",'UrlOer':""}           #Diccionario de la lista OCW['Material']['ListOERs'] 
    
    OCW['url'] = page
        
    readPage = urlopen(page).read()         #Leer pagina
    soup = BeautifulSoup(readPage)          #crear estructura BS4
    page_on = soup.find(text=re.compile("tem requested could not be found"))
    
    if (page_on != None):
        OCW['urlStatus']= False
        print page, " ",OCW['urlStatus']
        continue
        
    print "URL> ",OCW['url']
    OCW['Title'] = LimpiaText(soup.select('#content_title')[0].get_text())
    
    OCW['Autor'].append(LimpiaText(soup.select('#summary_details .author_title a')[0].get_text()))
    
    data = soup.select('#summary_details .clearfix li')
    for d in data:
        analiza(d.get_text())

    data = soup.select('#region-pre')[0].select('.content')[0].select('a')

    for a in data:
       print "MENU>", LimpiaText(a.get_text())

    """print "TIL>", OCW['Title']
    for a in OCW['Autor']:
        print "AUT>", a
    print "DUR>", OCW['Duration']
    print "LEV>", OCW['Level']
    print "DAT>", OCW['Date']"""
    print ""
