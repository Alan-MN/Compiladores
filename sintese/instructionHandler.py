from unicodedata import numeric


class instructionHandler:
    def __init__(self):
        self.current_line = 0
        self.placeholders = {}
        self.lineEquivalents = {}
        self.codigo_intermediario =[]

    def setPlaceholder(self,id):
        if id not in self.placeholders:
            self.placeholders[id] = 0

    def checkLine(self,lineNumber, goto = False):

        # chega depois de um goto
        if lineNumber not in self.lineEquivalents and goto:
            self.lineEquivalents[lineNumber] = 'goto'
            return

        #chegou natural
        if lineNumber not in self.lineEquivalents or (self.lineEquivalents[lineNumber] == 'goto' and goto == False):
            self.lineEquivalents[lineNumber] = self.getCurrentline()
            return
        return

    def handleInput(self, line):
        self.checkLine(line[0].value)
        id = line[2].value
        self.setPlaceholder(id)
        comando = 'read '+f'{id}'
        self.codigo_intermediario.append(comando)

    def handlePrint(self,line):
        self.checkLine(line[0].value)
        id = line[2].value
        self.setPlaceholder(id)
        comando = 'write ' + f'{line[2].value}'
        self.codigo_intermediario.append(comando)

    def handleGoto(self,line):
        self.checkLine(line[0].value)
        id = line[2].value
        self.checkLine(id, goto=True)
        comando = 'branch ' + f'{line[2].value}'
        self.codigo_intermediario.append(comando)

    def handleEnd(self,line):
        self.checkLine(line[0].value)
        comando = 'halt'
        self.codigo_intermediario.append(comando)

    def handleLet(self,line):
        self.checkLine(line[0].value)
        operators = {
            '+': 'add',
            '-': 'subtract',
            '*': 'multiply',
            '/': 'divide',
            '%': 'module'
            }
        tam = len(line)
        if line[4].classe == 'numero'  and tam == 6:
            id_resultado = line[4].value
            id_valor = line[2].value
            self.setPlaceholder(id_resultado)
            self.setPlaceholder(id_valor)
            self.codigo_intermediario.append(f'load {id_resultado}')
            self.codigo_intermediario.append(f'store {id_valor}')
        elif line[4].classe == 'numero'  and tam != 6:
            id_resultado = line[2].value
            id_var1 = line[4].value
            id_var2 = line[6].value
            self.setPlaceholder(id_resultado)
            self.setPlaceholder(id_var1)
            self.setPlaceholder(id_var2)
            operation = operators[line[5].value]
            self.codigo_intermediario.append(f'load {id_var1}')
            self.codigo_intermediario.append(f'{operation} {id_var2}')
            self.codigo_intermediario.append(f'store {id_resultado}')


        if line[4].classe =='identificador' and tam == 6:
            id_resultado = line[4].value
            id_valor = line[2].value
            self.setPlaceholder(id_resultado)
            self.setPlaceholder(id_valor)
            self.codigo_intermediario.append(f'load {id_resultado}')
            self.codigo_intermediario.append(f'store {id_valor}')

        if line[4].classe == 'identificador' and line[5].classe == 'operador aritmetico':
            id_resultado = line[2].value
            id_var1 = line[4].value
            id_var2 = line[6].value
            self.setPlaceholder(id_resultado)
            self.setPlaceholder(id_var1)
            self.setPlaceholder(id_var2)
            operation = operators[line[5].value]
            self.codigo_intermediario.append(f'load {id_var1}')
            self.codigo_intermediario.append(f'{operation} {id_var2}')
            self.codigo_intermediario.append(f'store {id_resultado}')

    def handleIf(self,line):
        self.checkLine(line[0].value)
        operator = line[3].value
        id_base = line[2].value
        id_comparador = line[4].value
        id_destino = line[6].value
        self.setPlaceholder(id_base)
        self.setPlaceholder(id_comparador)
        self.checkLine(id_destino, goto=True)
        match operator:
            case  "==":
                self.codigo_intermediario.append(f'load {id_base}')
                self.codigo_intermediario.append(f'subtract {id_comparador}')
                self.codigo_intermediario.append(f'branchzero {id_destino}')
            case '!=':
                self.codigo_intermediario.append(f'load {id_base}')
                self.codigo_intermediario.append(f'subtract {id_comparador}')
                self.codigo_intermediario.append(f'branchzero flag',)
                self.codigo_intermediario.append(f'branch {id_destino}')

            case '>':
                self.codigo_intermediario.append(f'load {id_comparador}')
                self.codigo_intermediario.append(f'subtract {id_base}',)
                self.codigo_intermediario.append(f'branchneg {id_destino}')

            case '<':
                self.codigo_intermediario.append(f'load {id_base}')
                self.codigo_intermediario.append(f'subtract {id_comparador}')
                self.codigo_intermediario.append(f'branchneg {id_destino}')

            case '>=':
                self.codigo_intermediario.append(f'load {id_comparador}')
                self.codigo_intermediario.append(f'subtract {id_base}')
                self.codigo_intermediario.append(f'branchneg {id_destino}')
                self.codigo_intermediario.append(f'branchzero {id_destino}')
            case '<=':
                self.codigo_intermediario.append(f'load {id_base}')
                self.codigo_intermediario.append(f'subtract {id_comparador}')
                self.codigo_intermediario.append(f'branchneg {id_destino}')
                self.codigo_intermediario.append(f'branchzero {id_destino}')

    def getIntermediaryCode(self):
        return self.codigo_intermediario

    def getPlaceholders(self):
        return self.placeholders

    def getLineEquivalents(self):
        return self.lineEquivalents

    def getCurrentline(self):
        return len(self.codigo_intermediario)