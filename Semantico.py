from TabelaSimbolos import TabelaSimbolos


class Semantico:
    def __init__(self, tokens):
        self.tabela = TabelaSimbolos()
        self.linhas = {}
        self.tokens = tokens
        self.errors = []


    def addLinha(self, linha):
        index = len(self.linhas)
        self.linhas[index + 1] = linha

    def addError(self, mensagem):
        self.errors.append(mensagem)

    def verificaSemantico(self):
        linha_ant = 0
        self.linhas = [linha[0] for linha in self.tokens]
        for linha in self.tokens:
            linha_atual = int(linha[0].value)
            if linha_atual <= linha_ant:
                self.addError(f'Erro semantico: Numero da linha {linha_atual} não é maior que o {linha_ant}')

            if linha[1].codigo == 62:
                self.tabela.addTabela(linha[2].value)

            if linha[1].codigo == 61:
                if len(linha) == 6:
                    if linha[2].codigo == 41:
                        self.tabela.addTabela(linha[2].value)

                    if linha[3].codigo == 41:
                        if linha[3].value not in self.tabela.tabela:
                            self.addError(f'Erro semantico: uso de variavel não declarada {linha[3].posicao}')

                if len(linha) == 7:
                    if linha[2].codigo == 41:
                        self.tabela.addTabela(linha[2].value)

                    if linha[3].codigo == 41:
                        if linha[3].value not in self.tabela.tabela:
                            self.addError(f'Erro semantico: uso de variavel não declarada {linha[3].posicao}')

                    if linha[5].codigo == 41:
                        if linha[5].value not in self.tabela.tabela:
                            self.addError(f'Erro semantico: uso de variavel não declarada {linha[3].posicao}')

                if linha[1].codigo == 65:
                    if linha[2].value not in self.linhas:
                        self.addError(f'Erro semantico: goto em {linha[2].posicao} aponta para linha inexistente')

                if linha[1].codigo == 66:
                    if linha[2].value not in self.tabela.tabela:
                        self.addError(f'Erro semantico: uso de variavel não declarada {linha[2].posicao}')

                    if linha[4].codigo == 41 and linha[4].value not in self.tabela.tabela:
                        self.addError(f'Erro semantico: uso de variavel não declarada {linha[4].posicao}')

                    if linha[6].value not in self.tabela.tabela:
                        self.addError(f'Erro semantico: goto em {linha[6].posicao} aponta para linha inexistente')



