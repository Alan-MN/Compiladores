class Token:
    def __init__(self, codigo, classe,posicao,value = None):
        self.codigo = codigo
        self.classe = classe
        self.posicao = posicao
        self.value = value

    def toString(self):
        return f'{self.codigo}, {self.classe}, {self.posicao}, {self.value}'
