import pymongo
from pymongo import MongoClient
import re,subprocess,pyfiglet
from validador import bcolors

#Endereco do cluster
cluster = MongoClient('')


subprocess.call('clear', shell=True)
text = pyfiglet.figlet_format('SPYDB')
print(text)


#Busca por algo simples. Ex: teste@gmail.com
RegexInput = input('Digite um dado para ser filtrado no banco: ')
PasteLink = r'/\w{8}'

#Usar o regex inputado para fazer uma busca na collection pastebin, quando ele der um match ele vai retornar o conteudo inteiro do paste.
def mongosearch():
    db = cluster['SisHistory']
    collection = db['pastes']
    mongodata = collection.find({'Conteudo': { '$regex': RegexInput }})
    data = []
    for x in mongodata:
        data.append(x)
    return data


def dateformater(dia):
    pattern = re.compile(r'\s+')
    NoSpace = re.sub(pattern, '',dia)
    pattern2 = re.compile(r',')
    SubP = re.sub(pattern2, ':', NoSpace)
    return SubP


#Filtro para dar uma formatada na mensagem final
def mongofilter():
    PasteLink = r'/\w{8}'
    Date = r'\d{4}.\s\d{1,}.\s\d{1,}.\s\d{1,}.\s\d{1,}.\s\d{1,}'
    PasteMongo = str(mongosearch()) 
    match = re.search(RegexInput, PasteMongo)
    matchLink = re.search(PasteLink, PasteMongo)
    matchDate = re.search(Date, PasteMongo)
    if match:
        dado = match.group(0)
        PasteLink = matchLink.group(0)
        dia = matchDate.group(0)
        DiaCerto = dateformater(dia)
        print(bcolors.OKBLUE+'[+] '+bcolors.ENDC+'O seguinte dado foi encontrado: '+dado+'\n'' Esse dado foi publicado no paste a seguir https://pastebin.com'+PasteLink+'\n No dia: '+str(DiaCerto))
    else:
        print(bcolors.FAIL+'[-] '+bcolors.ENDC+ 'Dado nao encontrado')

mongofilter()
