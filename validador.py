import re

# CPF Válido:
#156.421.746-90

def Email_validator():
    #Verificando se a string possui pelo menos um @ e um .
    if email.find("@") > 0 and email.find(".") > 0:
        return True
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
    
def CPF_validator(cpf):
    #Deixando apenas números
    num_cpf = re.sub('[^0-9]','',cpf)
    
    #Pegando os nove primeiros digitos do cpf
    slice_cpf = num_cpf[:9]

    #Verificando se é uma sequencia Ex:111111111,222222222 ...
    sequencia = slice_cpf[0] * len(slice_cpf)
    if sequencia == slice_cpf:
        print("Invalid Cpf")
    else:
        etapa1 = CPF_calculo(slice_cpf)
        etapa2 = CPF_calculo(etapa1)

        if etapa2 ==  num_cpf:
            return True
        else:
            print("CPF invalido")
    

if __name__ == "__main__":
    CPF_validator()
    Email_validator()


