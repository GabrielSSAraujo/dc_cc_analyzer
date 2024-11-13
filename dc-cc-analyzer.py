from modules.analyzer.static_analyzer import StaticAnalyzer
from modules.analyzer.type_extractor import TypeExtractor
from modules.code_instrumenter.code_formatter import CodeFormatter
from modules.code_instrumenter.code_instrumenter import CodeInstrumenter
from modules.data_processor.data_processor import DataProcessor
from modules.input_validator.input_validator import InputValidator
# from modules.printer.printer import Printer
from modules.test_driver.test_driver_generator import TestDriver

import sys
import os
import subprocess

if __name__ == "__main__":
    # python3 dc_cc.py /path-sut /path-testvec
    
    # Validate inputs
    # input_validator = InputValidator(sys.argv)
    # if not InputValidator.validate():
    #     exit

    path_sut = sys.argv[1]
    path_testvector = sys.argv[2]

    # Get coupling data from SUT
    static_analyzer = StaticAnalyzer()
    ast = static_analyzer.get_ast(path_sut)
    coupled_data = static_analyzer.get_coupled_data(ast)

    # # Get SUT's typedefs primitive types
    types = TypeExtractor()
    typedef_to_primitive_type = types.get_types_from_ast(ast)

    # # Generate preprocessed Instrumented SUT from AST
    code_instrumenter = CodeInstrumenter()
    preprocessed_code = code_instrumenter.instrument_code(ast, coupled_data, "SUT", typedef_to_primitive_type)  # gera SUTI.c

    # # Format Instrumented SUT (sut_inst.c)
    code_formatter = CodeFormatter(path_sut, static_analyzer)
    code = code_formatter.format_code(preprocessed_code)

    # # Create sut_inst.c file
    with open(os.path.dirname(path_sut) + "/sut_inst.c", "w+") as out_file:
        out_file.write(code)

    # # Compile Test Driver with Instrumented SUT and Original SUT
    dir_name = os.path.dirname(path_sut)
    compilation = subprocess.run(["make", "all", f"pd={dir_name}"])

    # #Execute Test Driver with Original SUT
    main_funtion = static_analyzer.get_func_metadata("SUT")
    td_generator = TestDriver()
    td_generator.generate_test_driver(path_testvector, "./data/results_sut.csv", main_funtion.parameters)

    # if compilation.returncode == 0:
    #     execution = subprocess.run(["./testdriver_sut"], capture_output=True, text=True)
    #     print(execution.stdout)

    # # Setup Test Driver
    # td_generator = TestDriver()
    # td_generator.generate_test_driver(path_testvector, "./data/results_suti.csv")

    # # Execute Test Driver with Instrumented SUT
    # if compilation.returncode == 0:
    #     # Executar o programa compilado
    #     execution = subprocess.run(["./testdriver_suti"], capture_output=True, text=True)
    #     print(execution.stdout) # debug
    
    # # Analyze data produced by test driver execution
    # data_processor = DataProcessor("./data/")
    # data_processor.analyze()

    # TO-DO: CREATE GET FUNCTIONS TO PASS DATA TO PRINTER

    # printer = Printer()
    # printer.generate_report()