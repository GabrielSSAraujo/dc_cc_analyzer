"""
 @file: test_driver_generator.py
 @brief [Descrição breve do arquivo]

 @date: 2024-11-12 17:29
 @author: Aline Andreotti Urna
 @e-mail: aline.urna@gmail.com
"""

from modules.test_driver.data_extractor import DataExtractor
import shutil
import pandas as pd
from models.parameter import Parameter


class TestDriver:

    def create_variables(self,CType_parameters):
        # Cria uma lista de strings no formato "parameter.type parameter.name;"
        variable_strings = [
            f"\t{param.type} {param.name};"
            for param in CType_parameters
        ]

        # Junta todas as strings em uma única string, com cada uma em sua linha
        variable_strings = '\n'.join(variable_strings)
        return variable_strings
    
    def header_generator(self, CType_parameters):
        # Cria uma lista de strings no formato "parameter.name"
        header = [param.name for param in CType_parameters if param.pointer_depth]
        
        # Junta todas as strings em uma única string, com cada uma separada por vírgula
        header = ', '.join(header)
        return header
    
    def generate_formatting_code(self, params):
        
        atoi= ['int', 'short', 'unsigned int', 'unsigned short', 'bool', 'size_t','int8_t', 'int16_t', 'int32_t', 'uint8_t', 'uint16_t', 'uint32_t']
        atof= ['float', 'double', 'long double']
        atol= ['long', 'unsigned long']
        atoll= ['long long', 'int64_t', 'uint64_t']
        
        code_lines = []
        
        for param in params:
            if not param.pointer_depth:
                code_lines.append('\t\ttoken = strtok(NULL, ",");')
                conversion_type = ''
                if param.type in atoi:
                    conversion_type = 'atoi'
                elif param.type in atof:
                    conversion_type = 'atof'
                elif param.type in atol:
                    conversion_type = 'atol'
                elif param.type in atoll:
                    conversion_type = 'atoll'
                if conversion_type != '':
                    code_lines.append(f'\t\tif (token != NULL) {param.name} = {conversion_type}(token);')
                else:
                    code_lines.append(f'\t\tif (token != NULL) {param.name} = token[0];')
        return code_lines
    
    
    def sut_caller(self, CType_parameters, sut_name):   
        param_strings = []
        for param in CType_parameters:
            if param.pointer_depth:
                param_strings.append(f'&{param.name}')
            else:
                param_strings.append(param.name)
        sut_call = f'{sut_name}({", ".join(param_strings)});'
        return sut_call 
    
    def write_results_formatter(self, CType_parameters, formatter_spec):
        # Criar a string de formato e a lista de variáveis
        format_string = []
        variables_list = []

        for param in CType_parameters:
            if param.pointer_depth:
                format_spec = formatter_spec[param.type]
                if format_spec:
                    format_string.append(format_spec)
                    variables_list.append(param.name)

        format_string = ",".join(format_string)
        variables_list= ",".join(variables_list)

        return format_string + "\\n", variables_list
        
    
    def _test_driver_generator(self, input_path, path_sut, result_file_path, original_file_path, CType_parameters,formatter_spec):

        # Caminho do arquivo .c
        # original_file_path = "./modules/test_driver/c_files/test_driver.c"  # TO DO: automatizar a busca do arquivo teste_driver.c

        # Caminho do arquivo de backup
        backup_file = "./modules/test_driver/c_files/test_driver_model.c"
        # Caminho do arquivo original

        # Copiar o conteúdo do arquivo de backup para o arquivo test_driver.c
        shutil.copyfile(backup_file, original_file_path)

        # Ler o conteúdo do arquivo
        with open(original_file_path, "r") as arquivo:
            conteudo = arquivo.read()
        # print(conteudo)
        # Substituir os valores específicos
        conteudo = conteudo.replace(
            "// include SutFileName.h", f'#include "../../../{path_sut}"'
        )  # TO DO: automatizar a inclusão do arquivo sut de interesse
        
        input_filename = "input_file"

        result_filename = "results_file"
        #path dinâmico para os arquivos de input.csv e output.csv
        conteudo = conteudo.replace("// inputFile_path", f'FILE *{input_filename} = fopen("{input_path}", "r");')       
        conteudo = conteudo.replace("// resultFile_path", f'FILE *{result_filename} = fopen("{result_file_path}", "w");')
        # Gerar dinamicamente a declaração de variáveis
        var_declaration = self.create_variables(CType_parameters)

        # Substituir a declaração de variáveis out no conteúdo
        conteudo = conteudo.replace("// init_var", var_declaration)

        # Gerar dinamicamente o cabeçalho
        header = self.header_generator(CType_parameters)
        conteudo = conteudo.replace(
            "// HeaderPlaceholder",
            f'fprintf({result_filename}, "%s,%s\\n","Time","{header}");'
        )
        
        #Gerar dinamicamente a atribuição dos tokens de input.csv
        #as variáveis de entrada do teste_driver.c
        code_lines = self.generate_formatting_code(CType_parameters)
        conteudo = conteudo.replace("// TokenAssignment", '\n'.join(code_lines))

        # Gerar dinamicamente a chamada da função SUT
        #enviar o nome da função SUT de interesse como parâmetro
        # TO DO : automatizar a busca do nome da função SUT (static analyzer?)
        sut_name = "SUT"
        sut_call = self.sut_caller(CType_parameters, sut_name)
        conteudo = conteudo.replace("// SUT()", f"{sut_call}")
        format_string, variable_list = self.write_results_formatter(CType_parameters, formatter_spec)
        # # Gerar a string de formato
        # format_string = "%s," + ",".join(["%d"] *( output_shape[1]-1)) + "\\n"
        # # Gerar a lista de variáveis
        # variables = ["aux_output_line"] + [f"out{i}" for i in range(output_shape[1]-1)]
        # # Combinar a string de formato e a lista de variáveis
        fprintf_line = f'if (fprintf({result_filename}, "%f,{format_string}", time_id,{variable_list}) < 0) {{'
        conteudo = conteudo.replace("// RESULTS.CSV", fprintf_line)

        # Escrever o conteúdo atualizado de volta no arquivo
        with open(original_file_path, "w") as arquivo:
            arquivo.write(conteudo)

        #print(f"Valores substituídos no arquivo {original_file_path}")

        return

    def generate_test_driver(self, file_path, path_sut, result_file_path, original_file_path, parameters, CType_parameters, formatter_spec):
        data_extractor = DataExtractor(file_path)
        input_path, output_path = data_extractor.extract_data(parameters)

        # print(f"input.csv - Linhas: {input_shape[0]}, Colunas: {input_shape[1]-1}")
        # print(f"output.csv - Linhas: {output_shape[0]}, Colunas: {output_shape[1]}")

        self._test_driver_generator(input_path, path_sut, result_file_path, original_file_path, CType_parameters, formatter_spec)
        
        
        #pro generator, precisamos de dinamicamente criar o código para o teste_driver.c, que consiste em alterações
        #dinamicas de acordo com a quantidade de colunas de saída e entrada, e a quantidade de linhas de entrada.
        #na planilha de teste, pode vir mais colunas, mas o teste driver vai usar apenas as colunas de entrada e saída,
        #ignoarando o restante.
        #duvida?? como vamos fazer o mapeamento das entradas e saídas??
        #exemplo: no sut a entrada chama suti0,suti1,suti2, e a saída chama suto0,suto1
        #mas quando chamamos a função compA, ela tem como entrada a0,a1,a2, e como saída b0,b1?
        #como vamos fazer essa correspondencia??
        #precisamos fazer a correlação entre os nomes das variáveis de entrada e saída do sut e do teste_driver.c
        #pra isso vou usar as strings parameter do analisador estático, e comparar com os nomes das variáveis de entrada e saída
        #dos arquivos inputs e outputs, e provavelmente o tolerance (ainda não refleti sobre isso).
