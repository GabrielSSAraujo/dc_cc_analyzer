from modules.analyzer.static_analyzer import StaticAnalyzer
from modules.instrumentation.instrument import Instrumentator
from utils.code_formatter import CodeFormatter
from modules.test_driver.test_driver_generator import TestDriver
import subprocess

if __name__ == "__main__":
    path = "./tests/data/SUT/"
    file_path = path + "sut.c"

    output_inst_sut = "tests/data/SUT/sut_inst.c"
    #file_path_inst_sut_header = "./tests/data/sut_inst.h"

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
    test_vector_path = "./tests/data/test_vectors/TestVec_VCP-500-VC-01.xlsx"


    #SUT INSTRUMENTADO
    td_generator = TestDriver()
    td_generator.generate_test_driver(test_vector_path, "./tests/data/results_suti.csv")

    # podemos ter um makefile aqui
    compilation = subprocess.run(
        ["gcc", "./modules/test_driver/c_files/test_driver.c", "./tests/data/SUT/sut_inst.c", "-o", "./modules/test_driver/c_files/test_driver"]
    )
    if compilation.returncode == 0:
        # Executar o programa compilado
        execution = subprocess.run(
            ["./modules/test_driver/c_files/test_driver"], capture_output=True, text=True
        )
        print(execution.stdout)
    
    #SUT ORIGINAL
    td_generator = TestDriver()
    td_generator.generate_test_driver(test_vector_path, "./tests/data/results_sut.csv")
    compilation = subprocess.run(
        ["gcc", "./modules/test_driver/c_files/test_driver.c", "./tests/data/SUT/sut.c", "-o", "./modules/test_driver/c_files/test_driver"]
    )
    if compilation.returncode == 0:
        # Executar o programa compilado
        execution = subprocess.run(
            ["./modules/test_driver/c_files/test_driver"], capture_output=True, text=True
        )
        print(execution.stdout)
