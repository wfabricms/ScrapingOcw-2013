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
pages = PagesUCataluya1
pagesaux = ['http://ocw.camins.upc.edu/ocw/home.htm?execution=e11s1']
for page in pages:    
    #LISTA PRINCIPAL [{OCW},{OCW},{OCW},{OCW}]
    ListaOcw = []
    #DICCIONARIO DE CADA OCW {'Url':www, 'Title': TituOcw}
    OCW = {'url':"",'urlStatus':True,'Title':"" ,'Department':"",'MainProfesor':[],'Profesores':[],'AutURL':"",'AutTitle':"",'VideoUrl':"",'VideoTitle':"",'Date':"",'BeginC':"",'ExtraData':[]}
    
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
    
    data1 = soup.select('div.span-20.last.prepend-1 div.span-11.last ul')
    for li in data1[0].select('li'):
        OCW['MainProfesor'].append(LimpiaText(li.get_text()))
    
    for p in OCW['MainProfesor']:
        print p
        
    print "\n"
    
    
    """
    if soup.select('div.columnleft_nomiddle blockquote table') != []:
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

    if soup.select('.columnleft_nomiddle p a') != []:
        OCW['BeginC'] =  soup.select('.columnleft_nomiddle p a')[0].get('href')

    if soup.select('#div.video iframe') != []:
        OCW['VideoUrl'] = soup.select('#div.video iframe')[0].get('src')

        if  OCW['VideoUrl'][0] =='/':
            webVideo = urlopen("http://ocw.uci.edu/" + OCW['VideoUrl']).read()
        else:
            webVideo = urlopen(OCW['VideoUrl']).read()
        
        soupvideo = BeautifulSoup(webVideo)
        OCW['VideoTitle'] = soupvideo.title.get_text()
    else:
        OCW['VideoUrl']=""
        OCW['VideoTitle']=""

    #print data.select('a')[a]get_text()

    print "TL>",OCW['Title']
    print "AU>",OCW['Author']
    print "AL>",OCW['AutURL']
    print "AT>",OCW['AutTitle']
    print "DP>",OCW['Department']
    print "VT>",OCW['VideoTitle']
    print "VU>",OCW['VideoUrl']
    print "BC>",OCW['BeginC']
    print "\n" 
    """
