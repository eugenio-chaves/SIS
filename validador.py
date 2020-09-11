import re,string

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
    
#Regex para validar se o numero do cartao e valido
Cre = r'^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$'

#Basicamente remover os pontos e espacos em branco da string do cartao e depois validar com o regex "Cre"
def CC_Validator(CC):
    Cnumber = CC.translate(str.maketrans('', '', string.punctuation))
    pattern = re.compile(r'\s+')
    Cnum = re.sub(pattern, '',Cnumber)
    if re.search(Cre, Cnum) is None:
        print('[+] Possivel cartao de Credito achado, mas o numero e falso.')
    else:
        return True

#Cores
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == "__main__":
    CPF_validator()
    Email_validator()


