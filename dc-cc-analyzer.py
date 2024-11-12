from modules.analyzer.static_analyzer import StaticAnalyzer
from modules.code_instrumenter.code_instrumenter import CodeInstrumenter
from modules.analyzer.type_extractor import TypeExtractor
from utils.code_formatter import CodeFormatter
from modules.test_driver.test_driver_generator import TestDriverGenerator
import subprocess
import os

if __name__ == "__main__":
    path_sut = "../SUT/sut.c"
    """
    # python3 dc_cc.py /path-sut /path-testvec

    InputValidator.validate(path-sut, path-testvec)
    """
    static_analyzer = StaticAnalyzer()

    # generate AST from SUT source
    ast = static_analyzer.get_ast(path_sut)

    # get coupled data from SUT components
    coupled_data = static_analyzer.get_coupled_data(ast)

    # get function metadata from function SUT(test: any function)
    function_list = static_analyzer.get_func_metadata()

    # get dictionary with typedef mapping to primitive types
    types = TypeExtractor(ast)
    type_list = types.get_types_from_ast()

    # instrument code using handling AST
    code_instrumenter = CodeInstrumenter()
    main_function = "SUT"
    preprocessed_code = code_instrumenter.instrument_code(
        ast, coupled_data, main_function, type_list
    )  # gera SUTI.c

    # format code and create sut_isnt.c
    code_formatter = CodeFormatter(path_sut, static_analyzer)
    code = code_formatter.format_code(preprocessed_code)

    with open(os.path.dirname(path_sut) + "/sut_inst.c", "w+") as out_file:
        out_file.write(code)

    """
    DataExtractor(path-testvec) # cria inputs.csv, outputs.csv, tolerances.csv

    TestDriver.generate(inputs.csv, outputs.csv, [class Parameter]) # modifica o modelo test_driver.c

    TestDriver.compile() # compila test_driver.c, logger.c, sut.c, suti.c, etc
    TestDriver.run() # run test_driver.c (com sut e suti) | results.csv (gerado pelo testdriver), coupling.csv (gerado pelo suti)

    DataProcessor.analyze(inputs.csv, outputs.csv, tolerances.csv, results.csv, coupling.csv) => analise = {
        "pass/fail": float, # porcentagem total
        "cobertura": float, # porcentagem total
        "instrumentacao_ok": bool,
        "passou": [bool],
        "observacoes": [str]
    }

    ReportGenerator.generate_report(analise, inputs.csv, outputs.csv, results.csv, coupling.csv) => report.pdf, complete_report.csv
    """
    pass
