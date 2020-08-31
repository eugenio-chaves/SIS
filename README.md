# SIS

## Como usar
- Executar o scrape.py primeiro e deixar rodando por uns 10 minutos, no Linux:$ ./scrape.py
- Colocar as credenciais do email no codigo peneira.py, no linux eu criei uma variavel para o
email e password, ex:(EMAIL_USER="lalala@gmail") no arquivo .bashrc ou .bash_profile caso eu precise 
compartilhar o codigo.

**Obs: Tem a chance de tomar bloqueio no pastebin se ficar pingando direto la, eu testei bastante
no meu IP e ate agora nada, mas a longo prazo acho uma boa colocar em uma EC2.**                            
                                    
## Scrape.py

Na página https://pastebin.com/archive tem os ultimos 50 pastes publicos que foram postados.
O script scrape.py vai analisar os pastes 1 por 1 e verificar se possui alguma informação 
sensível.

De inicio, o intervalo para cada paste ser armazenado é um numero random de no minimo 2 segundos 
e maximo 10, foi colocado esse intervalo para evitar um banimento. Então, leva mais ou menos 7 minutos 
para verificar uma pagina inteira contendo os 50 pastes.

Esse script sera automatizado usando cronjobs (https://www.youtube.com/watch?v=Qf5SPjHzvyw), 
de inicio, estou testando invocar ele a cada 15 minutos.

é recomendavel o uso de uma instância na EC2 quando for testar o código por um longo tempo, só para evitar uma chance de tomar um bloqueio no seu IP. 

## Peneira.py


Esse script vai fazer o filtro nos pastes usando regex, e se caso ele der
um match ele vai enviar um email notificando que deu um match positivo e vai montar o link original 
do paste no email, exemplo:

secureinfo59@gmail.com
3:15 PM (48 minutes ago)
to bcc: me

Possivel leak no Pastebin, link direto para o site https://pastebin.com/xEv0PmeN

Dentro do código, possui mais informações sobre o funcionamento.

## Lista de Regex

Regex para o formato do CPF: \d{3}[\.*-_]\d{3}[\.*-_]\d{3}[\.*-_]\d{2}

Regex para o formato de email simples: [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+

Regex para buscar por 'password': [pP][aA4][sS5][sS5][Ww][o0O][Rr][dD]

Regex para a palavra usuário: [uU][sS][uU][aAáÁ][rR][iIl][oO0]

Regex para qualquer cartao de credito(somente numeros sem .- ou ' '): ^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$


