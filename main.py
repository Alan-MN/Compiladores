from Analise_lexica import analiseLexica
from Parser import Parser
from Semantico import Semantico


def main():
    tabela_tokens = analiseLexica()
    parser = Parser(tabela_tokens)
    semantico = Semantico(tabela_tokens)
    semantico.verificaSemantico()
    for linha in tabela_tokens:
        parser.validalinha(linha)


    if len(parser.erros) > 0:
        for error in parser.erros:
            print(error)
    elif len(semantico.errors) > 0:
        for error in semantico.errors:
            print(error)
    else:
        print('input correto')

if __name__ =="__main__":
    main()