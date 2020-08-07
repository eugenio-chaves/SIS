#!/usr/bin/env python3
#script desenvolvido primeiramente para ser executado em sistemas linux

import re
import os
import sys
import smtplib

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')  #criar uma variavel no arquivo .bashrc ou .bash_profile com os dados de acesso, ou simplesmente colar no script mesmo.
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
MY_DIR = '' #precisa ser o mesmo diretorio em que o scraper salva os arquivos.
RESULT = [] #espaço para salvar o nome do arquivo atual do loop, para depois concatenar com a string e montar o link completo do pastebin.

CHAVES = r'[pP][aA4][sS5][sS5][Ww][o0O][Rr][dD]|\d{3}[\.*-_]\d{3}[\.*-_]\d{3}[\.*-_]\d{2}|4[0-9]{12}(?:[0-9]{3})?|(5[1-5][0-9]{14}|2(22[1-9][0-9]{12}|2[3-9][0-9]{13}|[3-6][0-9]{14}|7[0-1][0-9]{13}|720[0-9]{12}))'

#função para mandar email
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

#loop para filtar os arquivos usando regex. e se caso der positivo enviar um email.
for files in os.listdir(MY_DIR):
    RESULT.append(files)
    try:
        with open (MY_DIR + files, encoding='utf-8') as f: 
            files = f.read()
            if re.search(CHAVES, files,) is not None:
                print('[+] Tem coisa aqui! -- Link direto https://pastebin.com/'+RESULT[-1])
                subject = 'Possivel vazamento achado no pastebin'
                msg = 'Possivel leak no Pastebin, link direto para o site https://pastebin.com/'+RESULT[-1]
                send_email(subject, msg)
                
            else:
                print('[-] Pass')
        print('-----------------------------------------')
    except UnicodeDecodeError:
        #algumas vezes os pastes estao em outra lingua ou encodados, contendo malware na maioria das vezes.
        print('Paste codificado')


'''
Filtro para buscar informacoes sensiveis dentro de pastes postados no pastebin para a ferramenta SPYWEB do grupo SIS

'''
