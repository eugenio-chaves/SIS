#!/usr/bin/env python3
#script desenvolvido primeiramente para ser executado em sistemas linux

import re
import os
import sys
import smtplib
from validador import CPF_validator,Email_validator,CC_Validator,bcolors

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')  #criar uma variavel no arquivo .bashrc ou .bash_profile com os dados de acesso, ou simplesmente colar no script mesmo.
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


#regex
CPF = r'([0-9]{2}[\.-]?[0-9]{3}[\.-]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.-]?[0-9]{3}[\.-]?[0-9]{3}[-\.]?[0-9]{2})'
EMAIL = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
CC = r'\b\d{4}(| |-|.)\d{4}\1\d{4}\1\d{4}\b'


def send_email(subject, msg): 
    try:
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
#tive que parar de usar por que nao estava dando para chamar a variavel "msgt"
#def Printar(subject, msg):
   # print(subject + msgt)

def Search(info,pasteName):
    try:
        CPFmatch = re.search(CPF, info)
        Emailmatch = re.search(EMAIL, info)
        CCmatch = re.search(CC, info)

        if Emailmatch:
            EndEmail = Emailmatch.group(0)
            print(bcolors.OKGREEN+'[+]'+bcolors.ENDC+' Formato de email achado nesse paste! -- Link direto https://pastebin.com'+ pasteName)
            subject = ' Possivel vazamento achado no pastebin'
            #a variavel "msg" vai para o email, entao nao tem formatacao de cores nela
            msg = 'Possivel leak de email no Pastebin\n'+'Email: '+EndEmail+'\nLink direto para o site https://pastebin.com'+pasteName
            msgt = 'Possivel leak de Emails no Pastebin \n'+bcolors.OKGREEN+'[+]'+bcolors.ENDC+' Email: '+EndEmail+'\n'+bcolors.OKGREEN+'[+]'+bcolors.ENDC+' Link direto para o site https://pastebin.com'+pasteName
            send_email(subject, msg)
            print(bcolors.OKGREEN+'[+]'+bcolors.ENDC+ subject, msgt)

        elif CCmatch:
            CCNumber = CCmatch.group() + '\n'
            if CC_Validator(CCNumber) is True:
                print(bcolors.OKGREEN+'[+]'+bcolors.ENDC+' CC Valido achado! -- Link direto https://pastebin.com'+ pasteName)
                subject = ' Possivel vazamento achado no pastebin'
                #a variavel "msg" vai para o email, entao nao tem formatacao de cores nela
                msg = 'Cartao de Credito valido publicado no Pastebin\n'+'[+] Cartao: '+CCNumber+'[+] Link direto para o Paste https://pastebin.com'+pasteName
                msgt = 'Vazamento de Cartao de Credito no pastebin\n'+bcolors.OKGREEN+'[+]'+bcolors.ENDC+' Cartao: '+CCNumber+bcolors.OKGREEN+'[+]'+bcolors.ENDC+' Link direto para o Paste https://pastebin.com'+pasteName
                send_email(subject, msg)
                print(bcolors.OKGREEN+'[+]'+bcolors.ENDC+ subject, msgt)


        elif CPFmatch:
            CPFnumber = CPFmatch.group() + '\n'
            if CPF_validator(CPFnumber) is True:
                print(bcolors.OKGREEN+'[+]'+bcolors.ENDC+' CPF Valido achado! -- Link direto https://pastebin.com'+ pasteName)
                subject = ' Possivel vazamento achado no pastebin'
                #a variavel "msg" vai para o email, entao nao tem formatacao de cores nela
                msg = 'CPF Valido publicado no Pastebin\n'+'[+] CPF: '+CPFnumber+'[+] Link direto para o Paste https://pastebin.com'+pasteName
                msgt = 'Vazamento de CPFs achado no Pastebin\n'+bcolors.OKGREEN+'[+]'+bcolors.ENDC+' CPF: '+CPFnumber+bcolors.OKGREEN+'[+]'+bcolors.ENDC+' Link direto para o Paste https://pastebin.com'+pasteName
                send_email(subject, msg)
                print(bcolors.OKGREEN+'[+]'+bcolors.ENDC+ subject, msgt)


        else:
            print(bcolors.FAIL+'[-] Pass'+bcolors.ENDC)      
    except UnicodeDecodeError:
        #Algumas vezes os pastes estao em outra lingua ou encodados, contendo malware na maioria dos casos.
        print('Paste codificado')


                                    