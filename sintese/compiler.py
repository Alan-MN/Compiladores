from analise.Analise_lexica import  analiseLexica
from .instructionHandler import  instructionHandler
from .objectCodeGenerator import ObjectCodeGenerator


def compile():
    token_list = analiseLexica()
    object_code = ObjectCodeGenerator()
    instruction_handler = instructionHandler()
    for line in token_list:

        operation = line[1].codigo

        match operation:
            #checa se input
            case 62:
                instruction_handler.handleInput(line)

            #checa se let
            case 63:
                instruction_handler.handleLet(line)

            #checa se print
            case 64:
                instruction_handler.handlePrint(line)

            #checa se goto
            case 65:
                instruction_handler.handleGoto(line)

            #checa se if
            case 66:
                instruction_handler.handleIf(line)

            #checa se end
            case 67:
                instruction_handler.handleEnd(line)

    codigo_intermediario = instruction_handler.getIntermediaryCode()
    # count_linha = 0o0
    # for linha in codigo_intermediario:
    #     print(f'{count_linha:02d}: {linha}')
    #     count_linha +=1

    #precisa adicionar verificação de linha, ver se ja passou por ela e atribuir um endereço
    lineEquivalents = instruction_handler.getLineEquivalents()

    final_line = max(lineEquivalents.values()) + 1
    for key in instruction_handler.placeholders.keys():
        instruction_handler.placeholders[key] = final_line
        final_line+=1

    placeholders = instruction_handler.getPlaceholders()

    object_code.generate(intermediary_code= codigo_intermediario, lineEquivalents= lineEquivalents, placeholders= placeholders)
