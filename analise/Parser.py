import re

class Parser:
    def __init__(self, tokens):
        self.tokens  = tokens
        self.indice_atual = 0
        self.erros = []
        self.tabela = [
            ['', 'rem', 'input', 'print', 'goto', 'if', 'let', 'end', '[a-z]', '[0-9]+', '=', 'LF', 'ETX', '+', '-', '*', '/', '%', '==', '!=', '>', '<', '>=', '<='],
            ['<programa>', '','','','','','','','','<numero> <comando>','','','','','','','','','','','','','',''],
            ['<comando>','<rem>','<input>','<print>','<goto>','<if/goto>','<let>','<end>','<let>','','','','','','','','','','','','','','',''],
            ['<rem>', 'rem <fim>','','','','','','','','','','','','','','','','','','','','','',''],
            ['<input>','','input <identificador> <fim>','','','','','','','','','','','','','','','','','','','','',''],
            ['<let>', '','','','','','let <identificador> <atribuicao> <expressao>','','let <identificador> <atribuicao> <expressao> <fim>','','','','','','','','','','','','','','',''],
            ['<expressao>', '','','','','','','','<identificador> <operacao>','<numero> <operacao>','','','','','','','','','','','','','',''],
            ['<operacao>', '','','','','','','','','','','<fim>','','<operador_aritmetico> <operando>','<operador_aritmetico> <operando>','<operador_aritmetico> <operando>','<operador_aritmetico> <operando>','<operador_aritmetico> <operando>','','','','','',''],
            ['<operando>', '','','','sinq','','','','<identificador>','<numero>','','','','','','','','','','','','','',''],
            ['<print>', '','','print <identificador> <fim>','','','','','','','','','','','','','','','','','','','',''],
            ['<goto>', '','','','goto <numero> <fim>','','','','','','','','','','','','','','','','','','',''],
            ['<if/goto>', '','','','','if <identificador> <operador_relacional> <operando> <goto>','','','','','','','','','','','','','','','','','',''],
            ['<end>','','','','','','','end <fim>','','','','','','','','','','','','','','','',''],
            ['<identificador>', '','','','sinq','','','','[a-z]','','sinq','sinq','sinq','sinq','sinq','sinq','sinq','sinq','','','','','',''],
            ['<numero>', 'sinq','sinq','sinq','sinq','sinq','sinq','sinq','',"[0-9]+",'','sinq','sinq','sinq','sinq','sinq','sinq','sinq','','','','','',''],
            ['<atribuicao>', '','','','','','','','sinq','sinq','=','','','','','','','','','','','','',''],
            ['<operador_aritmetico>', '','','','','','','','sinq','sinq','','','','+','-','*','/','%','','','','','',''],
            ['<fim>','','','','','','','','','','','LF','ETX','','','','','','','','','','',''],
            ['<operador_relacional>', '','','','','','','','sinq','','','','','','','','','','==','!=','>','<','>=','<=']
        ]
        self.terminais = ['rem', 'input', 'print', 'goto', 'if', 'end', '[a-z]', '[0-9]+', '=', 'LF', 'ETX', '+', '-', '*', '/', '%', '==', '!=', '>', '<', '>=', '<=']
        self.naoterminais = ['<programa>','<comando>','<rem>','<input>','<let>','<operacao>','<operando>','<expressao>','<print>','<goto>','<if/goto>','<end>',"<identificador>",'<numero>','<atribuicao>','<operador_aritmetico>','<operador_relacional>']

    def pegaRegra(self,token,producao):
        n_linha = 0
        n_coluna = 0
        max_linha = len(self.tabela)


        for linha in self.tabela:
            if linha[0] == producao:
                break
            if n_linha < max_linha-1:
                n_linha+=1
        for coluna in self.tabela[0]:
            if re.fullmatch('-?[0-9]+', token):
                n_coluna = 9
                break
            if re.fullmatch('[a-z]', token):
                n_coluna = 8
                break
            if coluna == token:
                n_coluna  = self.tabela[0].index(coluna)
                break

        return self.tabela[n_linha][n_coluna]

    def empilhaRegra(self, regra):
        regra = regra.split(' ')
        regra.reverse()
        for palavra in regra:
            self.pilha.append(palavra)

    def validalinha(self,linha):
        pilha = ['$', '<programa>']
        indice = 0
        indice_max = len(linha)-1
        while True:
            topo = pilha.pop()
            token = linha[indice]
            if token.codigo == 0:
                errormessage = f'Erro de sintaxe: encontrado {token.value} na posicao {token.posicao}'
                self.erros.append(errormessage)
                return
            if topo in self.naoterminais:
                regra = self.pegaRegra(token.value,topo)
                if regra == 'sinq':
                    errormessage = f'Erro de sintaxe: encontrado {token.value} na posicao {token.posicao}'
                    self.erros.append(errormessage)
                    return
                if ' ' in regra:
                    regra = regra.split(' ')
                    regra.reverse()
                    for palavra in regra:
                        pilha.append(palavra)
                else:
                    pilha.append(regra)
            elif re.fullmatch(r'[a-z]+',token.value) and topo == '[a-z]':
                if indice < indice_max:
                    indice += 1
            elif re.fullmatch('-?[0-9]+', token.value) and topo == '[0-9]+':
                if indice < indice_max:
                    indice +=1
            elif token.value == topo:
                indice +=1
            elif topo == '<fim>' and (token.value == 'LF'or token.value =='ETX'):
                pass
            elif topo == '$':
                break
            else:
                errormessage = f'Erro de sintaxe: encontrado {token.value} na posicao {token.posicao}'
                self.erros.append(errormessage)
                return
