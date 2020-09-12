#!/usr/bin/env python3
#script desenvolvido primeiramente para ser executado em sistemas linux

import re
import os
import sys
import smtplib
from validador import CPF_validator,Email_validator,CC_Validator,bcolors

#regex
CPF = r'([0-9]{2}[\.-]?[0-9]{3}[\.-]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.-]?[0-9]{3}[\.-]?[0-9]{3}[-\.]?[0-9]{2})'
EMAIL = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
CC = r'\b\d{4}(| |-|.)\d{4}\1\d{4}\1\d{4}\b'

def send_email(subject, msg): 
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
    

def Shortcut(pasteName,category,category_val):
    print(bcolors.OKGREEN + '[+]' + bcolors.ENDC + category + ' Válido achado! -- Link direto https://pastebin.com' + pasteName)
    subject = 'Possivel vazamento achado no pastebin'
    msg = category + ': ' + category_val
    send_email(subject, msg)
    print(bcolors.OKGREEN + '[+]' + bcolors.ENDC + msg)

def Search(info,pasteName):
    try:
        CPFmatch = re.search(CPF, info)
        Emailmatch = re.search(EMAIL, info)
        CCmatch = re.search(CC, info)

        if Emailmatch:
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


                                    