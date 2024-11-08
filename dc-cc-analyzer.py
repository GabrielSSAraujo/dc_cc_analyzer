from analyzer.static_analyzer import StaticAnalyzer
from instrumentation.instrument import Instrumentator
from utils.code_formatter import CodeFormatter
from test_driver.test_driver_generator import TestDriverGenerator
import subprocess

if __name__ == "__main__":
    path = "./SUT/"
    file_path = path + "sut.c"

    output_inst_sut = "SUT/sut_inst.c"
    # file_path_inst_sut_header = "temp/sut_inst.h"

    # create static analyzer
    analyzer = StaticAnalyzer()

    # get ast com file_path
    ast = analyzer.get_ast(file_path)

    # get coupled data
    coupled_data = analyzer.get_coupled_data(ast)

    # create instrumentator
    intrumentator = Instrumentator()

    # instrument code to show coupled data value
    preprocessed_c_code = intrumentator.instrument_code(
        ast, coupled_data
    )  # possivel problema: carregando todo o codigo

    # convert preprocessed C code to readable code
    code_formatter = CodeFormatter(file_path, analyzer)
    code_formatter.format_code(preprocessed_c_code, output_inst_sut)

    # chama test driver para rodar sut instrumentado
    # pegar automaticamente arquivo dentro da pasta test_vector, por enquanto:
    test_vector_path = "./test_vector/TestVec_VCP-500-VC-01.xlsx"
    td_generator = TestDriverGenerator()
    td_generator.generate_test_driver(test_vector_path)

    # podemos ter um makefile aqui
    compilation = subprocess.run(
        ["gcc", "./SUT/test_driver.c", "./SUT/sut_inst.c", "-o", "./SUT/test_driver"]
    )
    if compilation.returncode == 0:
        # Executar o programa compilado
        execution = subprocess.run(
            ["./SUT/test_driver"], capture_output=True, text=True
        )
        print(execution.stdout)
