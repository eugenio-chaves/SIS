#!/usr/bin/env python3
#script desenvolvido primeiramente para ser executado em sistemas Linux.

import re
import getopt
import os
import sys
import requests
from html.parser import HTMLParser
import time
import random
import smtplib
import datetime,pytz
import pymongo
from pymongo import MongoClient
from validador import CPF_validator,Email_validator,CC_Validator,bcolors

##PYMONGO DB
cluster = MongoClient("")

db = cluster['SisHistory']
collection = db['pastes']

##FILTRO
CPF = r'([0-9]{2}[\.-]?[0-9]{3}[\.-]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.-]?[0-9]{3}[\.-]?[0-9]{3}[-\.]?[0-9]{2})'
EMAIL = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
CC = r'\b\d{4}(| |-|.)\d{4}\1\d{4}\1\d{4}\b'
Leaked = 'leaked'
Custom = ''

##Timezone GMT-3
brasil = pytz.timezone('Etc/GMT-3')
aware_datetime = brasil.localize(datetime.datetime.utcnow())

def send_email(subject, msg): 
    try:
        EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)
        server.quit()
        print(bcolors.OKGREEN+bcolors.BOLD+'[+] Email enviado com sucesso.'+bcolors.ENDC)
    except:
        print('Falha no envio do email.')
    

def Shortcut(pasteName,category,category_val):
    print(bcolors.OKGREEN + '[+]' + bcolors.ENDC + category + ' Válido achado! -- Link direto https://pastebin.com' + pasteName)
    subject = 'Possivel vazamento achado no pastebin'
    msg = category + ': ' + category_val
    send_email(subject, msg)
    print(bcolors.OKGREEN + '[+]' + bcolors.ENDC + msg)

def Search(info,pasteName):
    try:
        global Custom
        CustomMatch = False
        CustomMatch = re.search(Custom,info) if Custom != '' else CustomMatch
       
        CPFmatch = re.search(CPF, info)
        Emailmatch = re.search(EMAIL, info)
        CCmatch = re.search(CC, info)
        Leakedmatch = re.search(Leaked,info)

        if CustomMatch:
            Shortcut(pasteName,'Custom',Custom)

        elif Leakedmatch:
            Shortcut(pasteName,'Leaked',Leaked)

        elif Emailmatch:
            EndEmail = Emailmatch.group(0)
            Shortcut(pasteName,'Email',EndEmail)

        elif CCmatch:
            CCNumber = CCmatch.group() + '\n'
            if CC_Validator(CCNumber) is True:
                Shortcut(pasteName,'Cartao',CCNumber)


        elif CPFmatch:
            CPFnumber = CPFmatch.group() + '\n'
            if CPF_validator(CPFnumber) is True:
                Shortcut(pasteName,'CPF',CPFnumber)           

        else:
            print(bcolors.FAIL+'[-] Pass'+bcolors.ENDC)      
    except UnicodeDecodeError:
        #Algumas vezes os pastes estao em outra lingua ou encodados, contendo malware na maioria dos casos.
        print('Paste codificado')
    except TypeError:
        print('formato invalido')


##COLETA DO PASTEBIN
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:75.0) Gecko/20100101 Firefox/75.0',
}

class LinkParser(HTMLParser):
    def __init__(self):
        self.links = []
        HTMLParser.__init__(self)
        
    def handle_starttag(self, tag, attrs):         
        if tag == "a":
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])

#É nessa classe que o conteudo 'raw' do paste é tirado, basicamente o conteudo final.
class TextAreaParser(HTMLParser):
    def __init__(self, paste_id):
        self.paste_id = paste_id
        self.inTextarea = False
        HTMLParser.__init__(self)
        
    def handle_starttag(self, tag, attrs):
        if tag=="textarea":
            self.inTextarea = True
    
    def handle_endtag(self, tag):
        if tag=="textarea":
            self.inTextarea = False
#Função para lidar com os dados.
    def handle_data(self, data):
        global Quantities
        if Quantities > 0:       
            if self.inTextarea:
                print(bcolors.OKBLUE+"[+]"+bcolors.ENDC+" Lendo o Paste: https://pastebin.com" + self.paste_id)
                #print(data) possivel lugar para salvar o arquivo de log
                Search(data,self.paste_id)
                #ARMAZENANDO NO MONGODB (caso nao seja repetido)
                dupli_check = collection.find({ "Link": { "$regex": str(self.paste_id) } })
                try:
                    dupli_val = dupli_check[0]
                    print(bcolors.FAIL+'[-] Paste repetido'+bcolors.ENDC)
                except:
                    post = {'Link': self.paste_id, 'Conteudo': data, 'last_modified': aware_datetime}
                    collection.insert_one(post)
                    print(bcolors.OKBLUE+"[+] Paste armazenado no Banco de dados"+bcolors.ENDC)
                Quantities -= 1 if Quantities > 0 else Quantities
        else:
            print("Finalizando....")
            sys.exit()
                
            
            

#Aqui é feito um request para cada link filtrado do paste(a hash com 9 digitos)
def get_paste_by_id(paste_id):
    r = requests.get('https://pastebin.com'+paste_id, headers=headers)  
    tp = TextAreaParser(paste_id)
    tp.feed(r.text)

#Primeiro request no pastebin.
def get_public_pastes():
    r = requests.get('https://pastebin.com/archive', headers=headers)
    lp = LinkParser()
    lp.feed(r.text)
    #Cada paste tem uma hash no fim, aqui ela é filtrada e depois um arquivo e criado com o nome igual sua hash(total de 50 pastes).
    for link in lp.links:
        if len(link) == 9:
            get_paste_by_id(link)
            time.sleep(random.uniform(4, 18))

def Get_arguments():
    argv = sys.argv[1:]
    global Custom
    global Quantities
    Quantities = 50

    try:
        opts, args = getopt.getopt(argv, "c:q:")

    except:
        print(bcolors.FAIL+'[-] Error'+bcolors.ENDC)

    for opt, arg in opts:
        #Caso for informado uma informação específica com -c
        #Exemplo: python3 scrape.py -c import
        #Exemplo: python3 scrape.py -c python
        if opt in ['-c']:
            Custom = arg
        elif opt in ['-q']:
            Quantities = int(arg)
            print("Procurar em " + str(Quantities) + " Pastes")

    if __name__ == "__main__":
        get_public_pastes()

Get_arguments()
