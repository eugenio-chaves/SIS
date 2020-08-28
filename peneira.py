#!/usr/bin/env python3
#script desenvolvido primeiramente para ser executado em sistemas linux

import re
import os
import sys
import smtplib
from validador import CPF_validator, Email_validator

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')  #criar uma variavel no arquivo .bashrc ou .bash_profile com os dados de acesso, ou simplesmente colar no script mesmo.
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
MY_DIR = '' #precisa ser o mesmo diretorio em que o scraper salva os arquivos.
RESULT = [] #espaço para salvar o nome do arquivo atual do loop, para depois concatenar com a string e montar o link completo do pastebin.
#regex
CPF = r'\d{3}[\.*-_]\d{3}[\.*-_]\d{3}[\.*-_]\d{2}'
CHAVES = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
EMAIL = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'


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
            CPFmatch = re.search(CPF, files)
            #Emailmatch = re.search(EMAIL, files)

            if re.search(CHAVES, files,) is not None:
                print('[+] Tem coisa aqui! -- Link direto https://pastebin.com/'+RESULT[-1])
                subject = 'Possivel vazamento achado no pastebin'
                msg = 'Possivel leak no Pastebin, link direto para o site https://pastebin.com/'+RESULT[-1]
                send_email(subject, msg)
                
            elif CPFmatch:
                CPFnumber = CPFmatch.group() + '\n'
                if CPF_validator(CPFnumber) is True:
                    print('[+] CPF Valido achado! -- Link direto https://pastebin.com/'+RESULT[-1])
                    subject = 'Possivel vazamento achado no pastebin'
                    msg = 'CPF Valido publicado no Pastebin, link direto para o Paste https://pastebin.com/'+RESULT[-1]
                    send_email(subject, msg)
                    
            #elif Emailmatch:
                #NewEmail = Emailmatch.group() + '\n'       #trabalho em progresso
                #if Email_validator(NewEmail) is True:
              
                
            else:
                print('[-] Pass')
        print('-----------------------------------------')
    except UnicodeDecodeError:
        #algumas vezes os pastes estao em outra lingua ou encodados, contendo malware na maioria das vezes.
        print('Paste codificado')


'''
Filtro para buscar informacoes sensiveis dentro de pastes postados no pastebin para a ferramenta SPYWEB do grupo SIS

27/08/20 - Eugenio
* Filtro para CPF adicionado junto com o validador
* Mudei o retorno do validador de cpf para algo ser feito quando o cpf for valido
* Achei um regex para multiplos cartoes de credito, mas para ele funcionar o numero precisa estar limpo, sem pontos e espaco
* Tirei a maioria dos regex CHAVES, estava gerando muito falso-positivos
* A parte que trata do email esta parada por agora, meio que nao sei o que fazer direito
'''

                                    