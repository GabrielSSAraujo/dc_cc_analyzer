from modules.analyzer.static_analyzer import StaticAnalyzer
from modules.analyzer.type_extractor import TypeExtractor
from modules.code_instrumenter.code_formatter import CodeFormatter
from modules.code_instrumenter.code_instrumenter import CodeInstrumenter
from modules.data_processor.data_processor import DataProcessor
from modules.input_validator.input_validator import InputValidator
from modules.test_driver.data_extractor import DataExtractor
from modules.printer.printer import Printer
from modules.test_driver.test_driver_generator import TestDriver
import sys
import os
import subprocess
import platform

if __name__ == "__main__":
    # Validate inputs
    print(">> Validating inputs...")

    input_validator = InputValidator(sys.argv)
    if not input_validator.validate():
        exit(1)

    # REQ-2: A Ferramenta deve ser executada por meio de linha de comando seguindo a estrutura 
    # "python3 dc-cc-analyzer.py <sut> <test-vector>", onde "<sut>" é o caminho para o arquivo 
    # "sut.c" e "<test-vector>" é o caminho para a planilha de Test Vectors no computador do usuário.
    path_sut = sys.argv[1]
    path_testvector = sys.argv[2]
    dir_name = os.path.dirname(path_sut)

    # Get coupling data from SUT
    print(">> Identifying couplings...")
    static_analyzer = StaticAnalyzer()
    ast = static_analyzer.get_ast(path_sut)
    function_interface_list = static_analyzer.get_coupled_data(ast)

    # Get SUT's typedefs primitive types
    types = TypeExtractor()
    typedef_to_primitive_type = types.get_types_from_ast(ast)

    # # Generate preprocessed Instrumented SUT from AST
    print(">> Generating instrumented code...")
    code_instrumenter = CodeInstrumenter()
    preprocessed_code = code_instrumenter.instrument_code(
        ast, function_interface_list, "sut", typedef_to_primitive_type
    )  # gera SUTI.c

    # # Format Instrumented SUT (suti.c)
    code_formatter = CodeFormatter(path_sut, static_analyzer)
    code = code_formatter.format_code(preprocessed_code)
    include_abs_path_recorder = f'#include "{os.path.join(os.getcwd(), "modules", "coupling_recorder", "coupling_recorder.h")}"\n'

    code = include_abs_path_recorder + code

    # Create sut_inst.c file
    with open(dir_name + "/suti.c", "w+") as out_file:
        out_file.write(code)
    out_file.close()

    # Execute Test Driver with Original SUT
    main_funtion = static_analyzer.get_func_metadata("sut")

    CType_parameters_sut = []
    formatter_spec_sut = {}
    for param in main_funtion.parameters:
        format = types.get_format_from_type(str(param.type))
        param.type = types.type_list[param.type]
        CType_parameters_sut.append(param)
        formatter_spec_sut[param.type] = format

    # Data extractor
    data_extractor = DataExtractor(path_testvector)
    input_path = data_extractor.extract_data(main_funtion.parameters)

    # Test driver generator sut]
    print(">> Generating test drivers...")
    td_generator = TestDriver()
    td_generator.test_driver_generator(
        input_path,
        dir_name + "/sut.h",
        "./data/results_sut.csv",
        "./modules/test_driver/c_files/test_driver_sut.c",
        CType_parameters_sut,
        formatter_spec_sut,
    )
    # Setup Test Driver
    td_generator.test_driver_generator(
        input_path,
        dir_name + "/sut.h",
        "./data/results_suti.csv",
        "./modules/test_driver/c_files/test_driver_suti.c",
        CType_parameters_sut,
        formatter_spec_sut,
    )

    # REQ-1: A Ferramenta deve executar em sistemas operacionais Windows e distribuições Linux.
    # Compile Test Driver with Instrumented SUT and Original SUT
    print(">> Compiling codes...")
    if platform.system() == "Windows":
        compilation = subprocess.run(
            ["mingw32-make", "all", f"SRC_DIR={dir_name}"], stdout=subprocess.DEVNULL
        )
    else:
        compilation = subprocess.run(
            ["make", "all", f"SRC_DIR={dir_name}"], stdout=subprocess.DEVNULL
        )

    # Execute Test Driver with SUT
    print(">> Executing test drivers...")
    if compilation.returncode == 0:
        execution = subprocess.run(["./testdriver_sut"], capture_output=True, text=True)
        # print(execution.stdout)

    # Execute Test Driver with Instrumented SUT
    if compilation.returncode == 0:
        # Executar o programa compilado
        execution = subprocess.run(
            ["./testdriver_suti"], capture_output=True, text=True
        )
        # print(execution.stdout)  # debug

    # Analyze data produced by test driver execution
    print(">> Processing data...")
    data_processor = DataProcessor("./data/")
    df_list = data_processor.analyze(function_interface_list)
    dc_coverage = data_processor.get_coverage(df_list)
    pass_fail_coverage, pass_fail_data = data_processor.get_pass_fail_coverage()

    # REQ-13: A Ferramenta deve produzir como saída um relatório de cobertura DC/CC, em formato PDF, 
    # do SUT considerando como casos de teste os Test Vectors presentes na planilha de entrada.
    print(">> Generating report...")
    testvector_abs_path = os.path.abspath(path_testvector)
    sut_abs_path = os.path.abspath(path_sut)

    printer = Printer("./data/", sut_abs_path, testvector_abs_path, df_list, dc_coverage, pass_fail_coverage, pass_fail_data)
    printer.generate_report()
    
    print(">> DONE!")

    # REQ-14: Ao término da geração do relatório de cobertura, a Ferramenta deve informar ao usuário 
    # no terminal: "Check the report.pdf file in <path> directory.", onde "<path>" indica o local onde 
    # o relatório foi armazenado no computador do usuário.
    print(f">> Check the report.pdf file in {os.path.dirname(os.path.abspath(__file__))} directory.")
