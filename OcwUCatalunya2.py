# coding: utf-8
#-*- encoding utf-8 -*-
from bs4 import *
from urllib import urlopen
import re
from URLs import *

#Ambiguedades comunes de los valores 
DesAny = ["Any" ]
DesCode = ["Codi de"]
DesType = ["ipus d'assignatura"]
DesLeng = ["dioma d'impartic"]
DesCoor = ["Coordinador de"]
DesPro = ["Professorat"]


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

def Analiza(cadena):
    if len(cadena) > 0:
        if (cadena[0] == '\n'): 
            cadena == cadena[1:]
            
        for d in DesType:
            if d in cadena:
                OCW['type'].append(cadena)
                return True   

        for d in DesCode:
            if d in cadena:
                OCW['Code'].append(cadena)
                return True

        for d in DesAny:
            if d in cadena:
                OCW['Any'] = cadena
                return True
        for d in DesLeng:
            if d in cadena:
                OCW['Lenguages'].append(cadena)
                return True
        for d in DesCoor:
            if d in line.get_text():
                for br in line.select('br'):
                    if len(br.find_next(text = True)) > 5: 
                        OCW['Coordinador'].append(br.find_next(text = True))
                return True
        for d in DesPro:
            if d in line.get_text():
                for br in line.select('br'):
                    if len(br.find_next(text = True)) > 5 and br.find_next(text = True) != d: 
                        OCW['Profesores'].append(br.find_next(text = True))
                return True            
            
    return False
       
#Host
host = "" #"http://localhost/ocw/" 
#paginas web
pages = PagesUCataluya2
pagesaux = ['http://ocw.camins.upc.edu/ocw/home.htm?p_codiUpcUd=250233&p_idIdioma=2']
for page in pages:    
    #LISTA PRINCIPAL [{OCW},{OCW},{OCW},{OCW}]
    ListaOcw = []
    #DICCIONARIO DE CADA OCW {'Url':www, 'Title': TituOcw}
    OCW = {'url':"",'urlStatus':True,'TitlePage':"",'TitleOCW':"",'Coordinador':[],'Profesores':[],'Any':"",'Lenguages':[],"Code":[],"type":[],'UrlAsigAccess':"",'Materiales':[],'ExtraData':[]}
    
    OerMater = {'Text':"",'UrlOer':""}           #Diccionario de la lista OCW['Material']['ListOERs'] 
    
    OCW['url'] = page
        
    readPage = urlopen(page).read()         #Leer pagina
    soup = BeautifulSoup(readPage)          #crear estructura BS4
    page_on = soup.find(text=re.compile("quest curs no es troba"))
    
    if (page_on != None):
        OCW['urlStatus']= False
        print page, " ",OCW['urlStatus']
        continue

    print "URL> ",OCW['url']
    OCW['TitlePage'] = LimpiaText(soup.title.get_text())
    
    data1 = soup.select('div#content-content')[0]
    OCW['titleOCW'] = LimpiaText(data1.div.get_text())
    
    dataAsig = data1.div.next_sibling.next_sibling.tr.td.next_sibling
    if dataAsig != None:
        for line in dataAsig.select('span.field-content'):
            if Analiza(LimpiaText(line.get_text())) == False:
                OCW['ExtraData'].append(line.get_text())

    OCW['UrlAsigAccess'] = data1.find(text=re.compile("s de la assignatura")).parent.get('href')
    datMenu = soup.select('#block-ocw-0 div div')[0]
    datMater = datMenu.find(text=re.compile("Materials del curs")).parent.next_sibling('li')
    for li in datMater:
        OerMater['Text'] = li.a.get_text()
        OerMater['UrlOer'] = li.a.get('href')
        OCW['Materiales'].append(OerMater)
         
    for m in OCW['Materiales']:
        if 'Apunts' in m['Text']:
            print "APUNTS "
            webB = urlopen(page + 'Apunts').read()
            soupApunts = BeautifulSoup(webB)
        print m['Text'], " > ",m['UrlOer']
    
    print ""

    """print "TLE>", OCW['TitlePage']
    print "TLO>", OCW['titleOCW']
    if OCW['Any'] != "": print "ANY>", OCW['Any']

    for p in OCW['Lenguages']:
        print "LEG>",p
    for l in OCW['Code']:
        print "COD>",l
    for t in OCW['type']:
        print "TIY>",t
    for d in OCW['Coordinador']:
        print "COR>",d
    for p in OCW['Profesores']:
        print "PRO>",p

    print "ACC>", OCW['UrlAsigAccess']    
    for p in OCW['ExtraData']:
        print "EXT>",p
    print """
