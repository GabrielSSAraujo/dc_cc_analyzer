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
import platform

if __name__ == "__main__":
    # python3 dc_cc.py /path-sut /path-testvec
    
    # Validate inputs
    # input_validator = InputValidator(sys.argv)
    # if not InputValidator.validate():
    #     exit

    path_sut = sys.argv[1]
    path_testvector = sys.argv[2]
    dir_name = os.path.dirname(path_sut)

    # Get coupling data from SUT
    static_analyzer = StaticAnalyzer()
    ast = static_analyzer.get_ast(path_sut)
    coupled_data = static_analyzer.get_coupled_data(ast)

    # # Get SUT's typedefs primitive types
    types = TypeExtractor()
    typedef_to_primitive_type = types.get_types_from_ast(ast)

    # # Generate preprocessed Instrumented SUT from AST
    code_instrumenter = CodeInstrumenter()
    preprocessed_code = code_instrumenter.instrument_code(ast, coupled_data, "sut", typedef_to_primitive_type)  # gera suti.c

    # # Format Instrumented SUT (suti.c)
    code_formatter = CodeFormatter(path_sut, static_analyzer)
    code = code_formatter.format_code(preprocessed_code)
    include_abs_path_recorder = f'#include "{os.path.join(os.getcwd(), "modules", "coupling_recorder", "coupling_recorder.h")}"\n'

    code = include_abs_path_recorder + code

    # # # Create sut_inst.c file
    with open(dir_name + "/suti.c", "w+") as out_file:
        out_file.write(code)

    # #Execute Test Driver with Original SUT
    main_funtion = static_analyzer.get_func_metadata("sut")

    CType_parameters_sut = []
    formatter_spec_sut =  {}
    for param in main_funtion.parameters:
        format = types.get_format_from_type(str(param.type))
        param.type = types.type_list[param.type]
        CType_parameters_sut.append(param)
        formatter_spec_sut[param.type] = format

    # static_analyzer.
    td_generator = TestDriver()
    td_generator.generate_test_driver(path_testvector,dir_name+"/sut.h" , "./data/results_sut.csv", "./modules/test_driver/c_files/test_driver_sut.c", main_funtion.parameters, CType_parameters_sut, formatter_spec_sut)

    # Setup Test Driver
    td_generator = TestDriver()
    td_generator.generate_test_driver(path_testvector,dir_name+"/sut.h", "./data/results_suti.csv", "./modules/test_driver/c_files/test_driver_suti.c", main_funtion.parameters, CType_parameters_sut, formatter_spec_sut)

    # Compile Test Driver with Instrumented SUT and Original SUT
    if platform.system() == "Windows":
        compilation = subprocess.run(["mingw32-make", "all", f"SRC_DIR={dir_name}"])
    else:
        compilation = subprocess.run(["make", "all", f"SRC_DIR={dir_name}"])

    if compilation.returncode == 0:
        execution = subprocess.run(["./testdriver_sut"], capture_output=True, text=True)
        print(execution.stdout)

    # Execute Test Driver with Instrumented SUT
    if compilation.returncode == 0:
        # Executar o programa compilado
        execution = subprocess.run(["./testdriver_suti"], capture_output=True, text=True)
        print(execution.stdout) # debug
    
    # Analyze data produced by test driver execution
    # data_processor = DataProcessor("./data/")
    # data_processor.analyze()

    # TO-DO: CREATE GET FUNCTIONS TO PASS DATA TO PRINTER

    # printer = Printer()
    # printer.generate_report()