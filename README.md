## Instalação

```console
# Clonar o repositório
$ git clone https://github.com/g3ng3n/SIS.git

# Mudar para o diretório do SIS
$ cd SIS/
```

## Como usar spyweb
**Deve ser adicionada a url do mongo db!**
```console

$ python3 spyweb.py -h
usage: spyweb [-h] [-c [-q]

Spyweb: Pastebin scraper

Argumentos opcionais:
-h               Mostra a mensagem de ajuda e fecha.
-c VALOR         Utiliza um valor informado pelo usuário para fazer o filtro no pastebin.
-q QUANTIDADE    Limita a quantidade de pastes que serão procurados.

```

### Exemplo:
Para procurar em apenas 10 pastes 
```console
$ python3 spyweb.py -q 10
```

Para procurar pela palavra visa
```console
$ python3 spyweb.py -c visa
```
                                    
## Como usar spydb
**Deve ser adicionada a url do mongo db!**
```console

$ python3 spydb.py 

# Digite a seguir a informação que deseja procurar no banco de dados
```

### Exemplo:
Para filtrar pela palavra cpf
```console
$ python3 spydb.py 

Digite um dado para ser filtrado no banco: cpf
...
```
