#!/usr/bin/env python3

#script desenvolvido primeiramente para ser executado em sistemas Linux.
#a longo prazo de uso e recomandavel usar em uma maquina na cloud, como a EC2 da amazon por exemplo, pois existe uma chance de ter o IP bloqueado no pastebin.
'''
Este script vai filtrar o codigo fonte da pagina https://pastebin.com/archive para pegar os pastes.
Ele vai buscar pelo 'Raw Data' que todo paste contem.
'''

import requests
from html.parser import HTMLParser
import time
import random
import datetime


#header para se passar como um navegador na hora de dar request no site, para diminuir a chance de um IP ban.
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:75.0) Gecko/20100101 Firefox/75.0',
}

#diretorio onde os pastes serao salvos. Eu recomendo criar um diretório só para isso.
save_dir =  ''

#class para filtar a tag 'a' ná pagina do pastebin.
class LinkParser(HTMLParser):
    def __init__(self):
        self.links = []
        HTMLParser.__init__(self)
        
    def handle_starttag(self, tag, attrs):         
        if tag=="a":
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])

#é nessa class que o conteudo 'raw' do paste é tirado, basicamente o conteudo final.
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
#função para salvar o arquivo, cada arquivo tera o nome da sua hash.
    def handle_data(self, data):
        if self.inTextarea:
            fname = save_dir + self.paste_id
            with open (fname, 'w') as f:
                f.write('*'*100)
                f.write('\n')
                f.write(data)
                f.write('\n')
                f.write('*'*100)
                f.write('\n')

#aqui é feito um request para cada link filtrado do paste(a hash com 9 digitos)
def get_paste_by_id(paste_id):
    r = requests.get('https://pastebin.com'+paste_id, headers=headers)  
    tp = TextAreaParser(paste_id)
    tp.feed(r.text)

#primeiro request no pastebin.
def get_public_pastes():
    r = requests.get('https://pastebin.com/archive', headers=headers)
    lp = LinkParser()
    lp.feed(r.text)
    #cada paste tem uma hash no fim, aqui ela é filtrada e depois um arquivo e criado com o nome igual sua hash(total de 50 pastes).
    for link in lp.links:
        if len(link) == 9:
            get_paste_by_id(link,)
            time.sleep(random.uniform(2, 10)) #interssante deixar o tempo minimo acima de 2 segundos, e um intervalo grande.

if __name__ == "__main__":
    get_public_pastes()




'''
Scrape para buscar informacoes sensiveis dentro do pastebin e salvar em arquivos para depois serem filtrados
pela ferramenta SPYWEB do grupo SIS
'''