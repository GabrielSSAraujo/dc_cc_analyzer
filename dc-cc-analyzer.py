from analyzer.static_analyzer import StaticAnalyzer
from instrumentation.instrument import Instrumentator
from utils.code_formatter import CodeFormatter
from test_driver.test_driver_generator import TestDriverGenerator
import subprocess

if __name__ == "__main__":
    """
    # python3 dc_cc.py /path-sut /path-testvec

    InputValidator.validate(path-sut, path-testvec)

    [class Parameter] = StaticAnalyzer.get_func_metadata(string func_name)

    DataExtractor(path-testvec) # cria inputs.csv, outputs.csv, tolerances.csv

    TestDriver.generate(inputs.csv, outputs.csv, [class Parameter]) # modifica o modelo test_driver.c

    ast = StaticAnalyzer.get_ast(path-sut)
    [CouplingData] = StaticAnalyzer.get_coupled_data(ast)

    Instrumentator.instrument_code(ast, [CouplingData]) # gera SUTI.c

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
