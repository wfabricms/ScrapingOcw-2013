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
    CaractBorrar = ['\r','\n','  ','\t',]
    if cadena != None and len(cadena) > 2:
        for caract in CaractBorrar:
            while caract in cadena:
                cadena = cadena[:(cadena.index(caract))] + cadena[(cadena.index(caract))+1:]
        if len(cadena)>2:
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
       
def GetHost(url):
    indice = 0
    indSlash = 0
    for u in url:
        indSlash = indSlash +1
        if u == '/':
            indice = indice + 1
            if indice == 3:
                return url[:indSlash-1]

#paginas web
pages = PagesUCataluya1
pagesaux = ['http://ocw.camins.upc.edu/ocw/home.htm?p_codiUpcUd=250233&p_idIdioma=2']
host = GetHost(pages[1])
print "HOST>", host
for page in pages: 
    #LISTA PRINCIPAL [{OCW},{OCW},{OCW},{OCW}]
    ListaOcw = []
    #DICCIONARIO DE CADA OCW {'Url':www, 'Title': TituOcw}
    OCW = {'url':"",'urlStatus':True,'Title':"" ,'Department':[],'MainProfesor':[],'Profesores':[],'Date':"",'Credits':"",'Lenguages':[],"Titulaciones":[],"Description":"",'ExtraData':[]}
    
    
    Nav = {'Text':"",'Url':""}           #Diccionario de la lista OCW['Material']['ListOERs'] 
    
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

    for li in data1[1].select('li'):
        OCW['Profesores'].append(LimpiaText(li.get_text()))

    data1 = soup.select('div.span-20.last.prepend-1')[0]
    OCW['Credits'] = data1.find(text=re.compile('ditos:'))
    
    lengs = LimpiaText(data1.find(text=re.compile(' en que se imparte')).parent.next_sibling.next_sibling.get_text())

    while ';' in lengs:
        OCW['Lenguages'].append(lengs[:lengs.index(';')])
        lengs = lengs[lengs.index(';')+1:]
    if len(lengs) > 1: OCW['Lenguages'].append(lengs)
    
    deps = data1.find(text=re.compile('epartamento')).parent.next_sibling.next_sibling.get_text()
    
    while '\n' in deps:
        if len(LimpiaText(deps[:deps.index('\n')]))>5: OCW['Department'].append(LimpiaText(deps[:deps.index('\n')]))
        deps = deps[deps.index('\n')+1:]
    if len(LimpiaText(deps)) > 5: OCW['Department'].append(LimpiaText(deps))
    
    titu = data1.find(text=re.compile('itulacion')).parent.next_sibling.next_sibling.get_text()
    
    while '\n' in titu:
        if len(LimpiaText(titu[:titu.index('\n')]))>5: OCW['Titulaciones'].append(LimpiaText(titu[:titu.index('\n')]))
        titu = titu[titu.index('\n')+1:]
    if len(LimpiaText(titu)) > 5: OCW['Titulaciones'].append(LimpiaText(titu))
    
    if data1.find(text=re.compile('escripc')) != None: OCW['Description'] = LimpiaText(data1.find(text=re.compile('escripc')).parent.next_sibling.next_sibling.get_text())
    
    dataMenu = soup.select('div.menuEsquerre.ui-corner-all ul li')

    for menu in dataMenu:
        Nav['Text'] = LimpiaText(menu.get_text())
        if menu.a.get('href')[0] == '/':
            Nav['Url'] = host + menu.a.get('href')
        else:
            Nav['Url'] = menu.a.get('href')

        print "MENUTexto>",Nav['Text']
        print "MENUurl>",Nav['Url']
        if 'Inicio' in Nav['Text'] or 'Syllabus' in  Nav['Text']: 
            print ""
        else:
            readNav = urlopen(Nav['Url']).read()
            soupNav = BeautifulSoup(readNav)
            dataMenu = soupNav.select('div.span-20.last.prepend-1')[0].select('a')
            for a in dataMenu:
                if a.get('href')  != '#':
                    print "TEXOERS>", LimpiaText(a.get_text())
                    print "URLOERS>", a.get('href')
            print ""

    
    print "TL>", OCW['Title']
    for p in OCW['MainProfesor']:
        print "MP>",p
    for p in OCW['Profesores']:
        print "SP>",p
    print OCW['Credits']
    for l in OCW['Lenguages']:
        print "LG>",l

    for t in OCW['Titulaciones']:
        print "TI>",t
    for d in OCW['Department']:
        print "DP>",d
    print "DS>", OCW['Description'] 
    print "\n"
    