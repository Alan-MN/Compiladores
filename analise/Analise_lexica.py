from .Token import Token
import re
def validaToken(palavra, posicao):
    value = palavra
    classe = ''
    codigo = 0
    lista_delimitadores = {
        'LF' : 10,
        'ETX' : 0o3,
    }
    lista_operador= {
        '=': 11
    }
    lista_operadores_aritmeticos ={
        "+": 21,
        "-": 22,
        "*": 23,
        "/": 24,
        "%": 25
    }
    lista_operadores_relacional = {
        "==": 31,
        "!=": 32,
        ">": 33,
        "<": 34,
        ">=": 35,
        "<=": 36
    }
    lista_identificador = {
        "var": 41
    }
    lista_constantes={
        "const": 51
    }
    lista_palavra_reservada = {
        "rem": 61,
        "input": 62,
        "let": 63,
        "print": 64,
        "goto": 65,
        "if": 66,
        "end": 67
    }

    #checa se é constante numérica
    if re.fullmatch('-?[0-9]+', palavra):
        palavra = 'const'
        codigo = lista_constantes[palavra]
        classe = 'numero'

    #checa se é variavel
    if palavra.isalpha() and len(palavra) == 1 :
        palavra = 'var'
        codigo = lista_identificador[palavra]
        classe = 'identificador'

    #checa se é delimitador
    if lista_delimitadores.get(palavra):
        codigo =lista_delimitadores[palavra]
        classe = 'delimitador'

    # checa se é operador
    if lista_operador.get(palavra):
        codigo = lista_operador[palavra]
        classe = 'operador'

    # checa se é operador aritmetico
    if lista_operadores_aritmeticos.get(palavra):
        codigo = lista_operadores_aritmeticos[palavra]
        classe = 'operador aritmetico'
    # checa se é operadores relacionais
    if lista_operadores_relacional.get(palavra):
        codigo = lista_operadores_relacional[palavra]
        classe = 'operadores relacional'

    # checa se é operadores relacionais
    if lista_palavra_reservada.get(palavra):
        codigo = lista_palavra_reservada[palavra]
        classe = 'comando'


    try :
        return Token(codigo, classe, posicao , value)
    except:
        return Token(0, classe,posicao, value)

def lidaRem(string):
    rem = ' rem'
    tam_rem = len(rem)
    indiceRem = string.find(rem)
    if indiceRem == -1:
        return string, 0

    string_cortada =string[:indiceRem+(tam_rem)]
    offset = len(string) - len(string_cortada)
    string_final = string_cortada + ' LF'

    return string_final, offset

def formataLinha(linha):
    linha = linha.replace('\n', ' LF')
    linha, offset = lidaRem(linha)
    return linha.split(' '), offset

def analiseLexica():
    lista_tokens_validados = []
    try:
        arquivo = open('./source.txt', 'r')
    except:
        raise Exception('No input file found')

    n_linha = 1
    linhas = arquivo.readlines()
    linhas[-1] += ' ETX'
    for linha in linhas:
        tokens_linha = []
        n_coluna = 1
        output = []
        linha, offset = formataLinha(linha)
        for palavra in linha:
            espaco = 1
            if palavra == linha[-1]:
                espaco = 0

            palavra_validada = validaToken(palavra,(n_linha,n_coluna))
           # if palavra_validada.codigo == 0:
                #print(f"Token nao reconhecido '{palavra_validada.value}', na posicao {palavra_validada.posicao}")

            tokens_linha.append(palavra_validada)
            #checa se é o numero da linha
            if palavra_validada.codigo == 51 and n_coluna == 1:
                output.append([palavra_validada.codigo, palavra_validada.value , palavra_validada.posicao])
            else:
                output.append([palavra_validada.codigo, ' ', palavra_validada.posicao])

            if palavra != 'rem':
                n_coluna += len(palavra) + espaco
            else:
                n_coluna += offset
        n_linha +=1
        lista_tokens_validados.append(tokens_linha)
    return lista_tokens_validados

if __name__ == "__main__":
    analiseLexica()