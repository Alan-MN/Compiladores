class TabelaSimbolos:
    def __init__(self):
        self.tabela = {}


    def addTabela(self,simbolo):
        index = len(self.tabela)
        if simbolo not in self.tabela.values():
            self.tabela[index+1] = simbolo

    def getSimbolos(self, simbolo):
        for chave , valor in self.tabela.items():
            if simbolo == valor:
                return chave

    def __str__(self):
        return str(self.tabela)