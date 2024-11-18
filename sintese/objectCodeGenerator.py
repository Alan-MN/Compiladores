class ObjectCodeGenerator:
    def __init__(self):
        self.objectCode = []

    def generate(self,intermediary_code,lineEquivalents,placeholders):
        operation_code={
            'read':'+10',
            'write':'+11',
            'load':'+20',
            'store':'+21',
            'add':'+30',
            'subtract':'+31',
            'divide':'+32',
            'multiply':'+33',
            'module':'+34',
            'branch':'+40',
            'branchneg':'+41',
            'branchzero':'+42',
            'halt':'+43'
        }
        for line in intermediary_code:
            #print(line)
            command = line.split(' ')
            adress_user = ['branch','branchneg','branchzero']
            line_command = command[0]
            if line_command == 'halt':
                self.objectCode.append('+4300')
            else:
                value = command[1]
                if line_command in adress_user:
                    if value != 'flag':
                        self.objectCode.append(f'{operation_code[line_command]}{lineEquivalents[value]:02d}')
                    else:
                        line_value = len(self.objectCode)+2
                        self.objectCode.append(f'{operation_code[line_command]}{line_value:02d}')
                else:
                    self.objectCode.append(f'{operation_code[line_command]}{placeholders[value]:02d}')
        # print(len(self.objectCode)+1)
        # print(placeholders)
        # print(lineEquivalents)
        for key in placeholders.keys():
            if key.isalpha():
                self.objectCode.append(f'+0000')
            else:
                valor = int(key)
                if valor >= 0:
                    self.objectCode.append(f'+{valor:04d}')
                else:
                    self.objectCode.append(f'{valor:05d}')

        with open('./binary.txt', 'w') as output:
            for line in self.objectCode:
                output.writelines(line+"\n")


