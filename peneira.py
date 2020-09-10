#!/usr/bin/env python3
#script desenvolvido primeiramente para ser executado em sistemas linux

import re
import os
import sys
import smtplib
from validador import CPF_validator, Email_validator

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')  #criar uma variavel no arquivo .bashrc ou .bash_profile com os dados de acesso, ou simplesmente colar no script mesmo.
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


#regex
CPF = r'([0-9]{2}[\.-]?[0-9]{3}[\.-]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.-]?[0-9]{3}[\.-]?[0-9]{3}[-\.]?[0-9]{2})'
EMAIL = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

def send_email(subject, msg): 
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message) #A segunda variavel é o email do destinatario, mas para para testar ele esta enviando para o proprio endereço.
        server.quit()
        print('Email enviado com sucesso.')
    except:
        print('Falha no envio do email.')

def Printar(subject, msg):
    print(subject + "--" +msg)

def Search(info,pasteName):
    try:
        CPFmatch = re.search(CPF, info)
        Emailmatch = re.search(EMAIL, info)

        if Emailmatch:
            print('[+] Tem coisa aqui! -- Link direto https://pastebin.com'+ pasteName)
            subject = 'Possivel vazamento achado no pastebin'
            msg = 'Possivel leak no Pastebin, link direto para o site https://pastebin.com' + pasteName
            send_email(subject, msg)
            Printar(subject, msg)
                
        elif CPFmatch:
            CPFnumber = CPFmatch.group() + '\n'
            if CPF_validator(CPFnumber) is True:
                print('[+] CPF Valido achado! -- Link direto https://pastebin.com/'+ pasteName)
                subject = 'Possivel vazamento achado no pastebin'
                msg = 'CPF Valido publicado no Pastebin, link direto para o Paste https://pastebin.com/'+ pasteName
                send_email(subject, msg)
                Printar(subject, msg)
                    
        else:
            print('[-] Pass')      
    except UnicodeDecodeError:
        #Algumas vezes os pastes estao em outra lingua ou encodados, contendo malware na maioria das vezes.
        print('Paste codificado')


                                    