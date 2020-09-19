#!/usr/bin/env python3

#script desenvolvido primeiramente para ser executado em sistemas Linux.
#a longo prazo de uso e recomandavel usar em uma maquina na cloud, como a EC2 da amazon por exemplo, pois existe uma chance de ter o IP bloqueado no pastebin.
'''
Este script vai filtrar o codigo fonte da pagina https://pastebin.com/archive para pegar os pastes.
Ele vai buscar pelo 'Raw Data' que todo paste contem.
'''
import re
import getopt
import os
import sys
import requests
from html.parser import HTMLParser
import time
import random
import smtplib
import datetime
from validador import CPF_validator,Email_validator,CC_Validator,bcolors

##FILTRO

#regex
CPF = r'([0-9]{2}[\.-]?[0-9]{3}[\.-]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.-]?[0-9]{3}[\.-]?[0-9]{3}[-\.]?[0-9]{2})'
EMAIL = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
CC = r'\b\d{4}(| |-|.)\d{4}\1\d{4}\1\d{4}\b'
Custom = ''

def send_email(subject, msg): 
    print(subject,msg)
    '''
    print('Subject ' + str(subject) + ',Mensagem ' + msg)
    try:
        EMAIL_ADDRESS = os.environ.get('EMAIL_USER')  #criar uma variavel no arquivo .bashrc ou .bash_profile com os dados de acesso, ou simplesmente colar no script mesmo.
        EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message) #A segunda variavel é o email do destinatario, mas para para testar ele esta enviando para o proprio endereço.
        server.quit()
        print(bcolors.OKGREEN+bcolors.BOLD+'[+] Email enviado com sucesso.'+bcolors.ENDC)
    except:
        print('Falha no envio do email.')
    '''
    

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

        if CustomMatch:
            CustomInfo = CustomMatch.group(0) 
            Shortcut(pasteName,'Custom',CustomInfo)

        elif Emailmatch:
            EndEmail = Emailmatch.group(0)
            Shortcut(pasteName,'Email',EndEmail)

        elif CCmatch:
            CCNumber = CCmatch.group() + '\n'
            Shortcut(pasteName,'Cartão de credito',CCNumber)


        elif CPFmatch:
            CPFnumber = CPFmatch.group() + '\n'
            if CPF_validator(CPFnumber) is True:
                Shortcut(pasteName,'CPF',CPFnumber)           

        else:
            print(bcolors.FAIL+'[-] Pass'+bcolors.ENDC)      
    except UnicodeDecodeError:
        #Algumas vezes os pastes estao em outra lingua ou encodados, contendo malware na maioria dos casos.
        print('Paste codificado')

##COLETA DO PASTEBIN

#Headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:75.0) Gecko/20100101 Firefox/75.0',
}

#Classe para filtar a tag 'a' ná pagina do pastebin.
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
#Função para salvar o arquivo, cada arquivo tera o nome da sua hash.
    def handle_data(self, data):
        if self.inTextarea:
            print(bcolors.OKBLUE+"[+]"+bcolors.ENDC+" Lendo o Paste: https://pastebin.com" + self.paste_id)
            #print(data) possivel lugar para salvar o arquivo de log
            Search(data,self.paste_id)
            

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
            time.sleep(random.uniform(2, 10)) #interessante deixar o tempo minimo acima de 2 segundos, e um intervalo grande.

def Get_arguments():
    argv = sys.argv[1:]
    global Custom

    try:
        opts, args = getopt.getopt(argv, "c:")

    except:
        print("Error")

    for opt, arg in opts:
        #Caso for informado uma informação específica com -c
        #Exemplo: python3 scrape.py -c import
        #Exemplo: python3 scrape.py -c python
        if opt in ['-c']:
            Custom = arg

    if __name__ == "__main__":
        get_public_pastes()

Get_arguments()

'''
Scrape para buscar informacoes sensiveis dentro do pastebin e salvar em arquivos para depois serem filtrados
pela ferramenta SPYWEB do grupo SIS
'''
