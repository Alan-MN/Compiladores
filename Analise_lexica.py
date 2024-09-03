def validaToken(Token):
    lista_reservados = {
        'LF' : 10,
        'ETX' : 0o3,
        '=' : 11,
        "+": 21,
        "-": 22,
        "*": 23,
        "/": 24,
        "%": 25,
        "==": 31,
        "!=": 32,
        ">": 33,
        "<": 34,
        ">=": 35,
        "<=": 36,
        "var": 41,
        "const":51,
        "rem": 61,
        "input": 62,
        "let": 63,
        "print": 64,
        "goto": 65,
        "if": 66,
        "end": 67
    }
    if Token.isdigit():
        Token = 'const'
    if Token.isalpha() and len(Token) == 1 :
        Token = 'var'
    try :
        return lista_reservados[Token]
    except:
        return 0

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
    arquivo = open('input.txt','r')
    n_linha = 1
    linhas = arquivo.readlines()
    linhas[-1] += ' ETX'
    for linha in linhas:
        n_coluna = 1
        output = []
        linha, offset = formataLinha(linha)
        for palavra in linha:
            espaco = 1
            if palavra == linha[-1]:
                espaco = 0

            codigo = validaToken(palavra)
            if codigo == 0:
                print(f"Token nao reconhecido '{palavra}', na posicao ({n_linha},{n_coluna})")

            lista_tokens_validados.append([palavra , (n_linha, n_coluna)])
            #checa se é o numero da linha
            if codigo == 51 and n_coluna == 1:
                output.append([codigo, palavra , (n_linha, n_coluna)])
            else:
                output.append([codigo, ' ', (n_linha, n_coluna)])

            if palavra != 'rem':
                n_coluna += len(palavra) + espaco
            else:
                n_coluna += offset
        print(output)
        n_linha +=1
if __name__ == "__main__":
    analiseLexica()