# author: aline
# comando:  python3 ./scripts/data_management.py ./testes/TestVec_VCP-500-VC-01.xlsx

# COMECE POR AQUI:
# 1)O PRIMEIRO código a ser excecutado: data_management.py, usando o comando: python3 ./scripts/data_management.py ./testes/TestVec_VCP-500-VC-01.xlsx
# válido para quando abre o terminal no dc_cc_analyzer
# 2)SOMENTE APÓS A EXECUÇÃO DO data_management.py, O CÓDIGO teste_driver.c SERÁ GERADO, E O CÓDIGO teste_driver.c SERÁ EXECUTADO
# utilizando o comando: gcc SUT/teste_driver.c SUT/SUT.c -o teste_driver
# válido para quando o terminal estiver na pasta dc_cc_analyzer

# DESCRIÇÃO RÁPIDA:
# 1)data_management.py fará a inclusão do método extract_data_from_csv() na classe DataExtractor do arquivo data_extractor.py.
# 2)a partir dai, faremos a geração de texto para criar acrescentar código no arquivo teste_driver.c (usando o script_generator) do arquivo data_management.py
# 2.1)incluiremos: o arquivo input.csv para ser lido linha a linha pelo programa no teste_driver.c e o arquivo output.csv para ser comparado com a saída do programa
# e então um novo arquivo armazenando os resultados esperados e o resultado real.


# futuro:
# 1)incluir a análise estática no código
# 2)usar o subprocess, para automatizar a execução do teste_driver.c
# 3)levantamento dos possíveis erros causados pela inconsistencia de path dos arquivos

from test_driver.data_extractor import DataExtractor
import shutil


class TestDriverGenerator:

    def _generate_header(self, out_cols):
        header = "out0"
        for i in range(out_cols - 1):
            header += f",out{i+1}"
        return header

    def _test_driver_generator(self, input_shape, output_shape):
        # Caminho do arquivo .c
        original_file_path = "./SUT/test_driver.c"  # TO DO: automatizar a busca do arquivo teste_driver.c

        # Caminho do arquivo de backup
        backup_file = "./test_driver/c_files/test_driver_model.c"
        # Caminho do arquivo original

        # Copiar o conteúdo do arquivo de backup para o arquivo test_driver.c
        shutil.copyfile(backup_file, original_file_path)

        # Ler o conteúdo do arquivo
        with open(original_file_path, "r") as arquivo:
            conteudo = arquivo.read()
        # print(conteudo)
        # Substituir os valores específicos
        conteudo = conteudo.replace(
            "// include SutFileName.h", f'#include "SUT.h"'
        )  # TO DO: automatizar a inclusão do arquivo sut de interesse
        conteudo = conteudo.replace("// define ROWS", f"#define ROWS {input_shape[0]}")
        conteudo = conteudo.replace("// define COLS", f"#define COLS {input_shape[1]}")
        conteudo = conteudo.replace(
            "// define OUT_COLS", f"#define OUT_COLS {output_shape[1]}"
        )

        # Gerar dinamicamente a declaração de variáveis out
        out_declaration = (
            "int " + ", ".join([f"out{i}" for i in range(output_shape[1])]) + ";"
        )  # esse int no inicio deixa fixo que todas as variáveis são inteiras
        # mas isso deve ser modificado quando tiver o resultado da análise estática

        # Substituir a declaração de variáveis out no conteúdo
        conteudo = conteudo.replace("// int outx", out_declaration)

        # Gerar dinamicamente o cabeçalho
        header = self._generate_header(
            output_shape[1]
        )  # output_shape[1] é o número de colunas de saída
        conteudo = conteudo.replace(
            "// HeaderPlaceholder",
            f'fprintf(results_file, "%s,%s\\n",output_line,"{header}");',
        )

        # Gerar dinamicamente a chamada da função SUT
        sut_call = (
            "SUT("
            + ", ".join([f"input_data[{i}]" for i in range(input_shape[1])])
            + ", "
            + ", ".join([f"&out{i}" for i in range(output_shape[1])])
            + ");"
        )
        # Substituir a chamada da função SUT no conteúdo
        conteudo = conteudo.replace("// SUT()", f"{sut_call}")

        # Gerar a lista de comparações
        comparisons = [f"out{i} == output_data[{i}]" for i in range(output_shape[1])]
        # Combinar as comparações em uma única expressão lógica
        comparison_expression = " && ".join(comparisons)
        # Criar a linha de código final
        test_result_line = f"int test_result = ({comparison_expression}) ? 1 : 0;"
        conteudo = conteudo.replace(
            "// PassFailComparison", test_result_line
        )  # TO DO: aceitar todos tipos de variavel, não apenas o inteiro (talvez uma struct?)

        # Gerar a string de formato
        format_string = "%s," + ",".join(["%d"] * output_shape[1]) + "\\n"
        # Gerar a lista de variáveis
        variables = ["aux_output_line"] + [f"out{i}" for i in range(output_shape[1])]
        # Combinar a string de formato e a lista de variáveis
        fprintf_line = f'if (fprintf(results_file, "{format_string}", {", ".join(variables)}) < 0) {{'
        conteudo = conteudo.replace("// LineConcat", fprintf_line)

        # Escrever o conteúdo atualizado de volta no arquivo
        with open(original_file_path, "w") as arquivo:
            arquivo.write(conteudo)

        # print(f"Valores substituídos no arquivo {original_file_path}")

        return

    def generate_test_driver(self, file_path):
        data_extractor = DataExtractor(file_path)
        input_shape, output_shape = data_extractor.extract_data_from_excel()

        # print(f"input.csv - Linhas: {input_shape[0]}, Colunas: {input_shape[1]}")
        # print(f"output.csv - Linhas: {output_shape[0]}, Colunas: {output_shape[1]}")

        self._test_driver_generator(input_shape, output_shape)
