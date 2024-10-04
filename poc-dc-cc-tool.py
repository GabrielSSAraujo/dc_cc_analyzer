from analyzer.static_analyzer import StaticAnalyzer
from instrumentation.instrument import Instrumentator

if __name__ == "__main__":
    path = "./SUT/"
    file_path = path + "sut.c"
    analyzer = StaticAnalyzer(file_path)

    ast = analyzer.get_ast()
    coupled_data = analyzer.get_coupled_data()

    intrumentator = Instrumentator(ast, coupled_data, file_path)
    intrumentator.instrument_code()
