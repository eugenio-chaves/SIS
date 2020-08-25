import re

'''
* Obter primeiro dígito:
    1 - Multiplicar os 9 primeiros dígitos do CPF por uma contagem
        regressiva iniciando de 10 e terminando em 2
    2 - Somar todos os valores das multiplicações do passo 1
    3 - Obter o resto da divisão entre a soma e 11 do passo 2
    4 - Subtrair o resultado do passo 3 por 11
    5 - Se o resultado do passo 4 for maior que nove, o dígito é zero,
        caso contrário, o dígito é o valor do passo 4

* Obter segundo dígito:
    1 - Multiplicar os 9 primeiros dígitos do CPF, MAIS O PRIMEIRO DIGITO
        obtido anteriormente por uma contagem regressiva iniciando de 11
        e terminando em 2
    2 - Mesma lógica do passo 2 do primeiro dígito em diante.
'''

#156.421.746-90
cpf = '156.421.746-90'
email = 'email@email.com'


def Email_validator():
    #Verificando se a string possui pelo menos um @ e um .
    if email.find("@") > 0 and email.find(".") > 0:
        print("Valid E-mail")
    else:
        print("Invalid E-mail")

def CPF_calculo(cpf):
    soma = 0
    resto = 0
    for chave,multiplicador in enumerate(range(len(cpf)+1,1,-1)):
        soma += int(cpf[chave]) * multiplicador
    resto = 11 - soma % 11
    resto = resto if resto <= 9 else 0
    novo_cpf = cpf + str(resto)
    return novo_cpf
    
        

def CPF_validator():
    #Deixando apenas números
    num_cpf = re.sub('[^0-9]','',cpf)
    
    #Pegando os nove primeiros digitos do cpf
    slice_cpf = num_cpf[:9]

    #Verificando se a sequencia Ex:111111111,222222222 ...
    sequencia = slice_cpf[0] * len(slice_cpf)
    if sequencia == slice_cpf:
        print("Invalid Cpf")
    else:
        etapa1 = CPF_calculo(slice_cpf)
        etapa2 = CPF_calculo(etapa1)

        if etapa2 ==  num_cpf:
            print("Valid Cpf")
        else:
            print("Invalid Cpf")
    

     

Email_validator()
CPF_validator()

