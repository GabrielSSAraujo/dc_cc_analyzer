import unittest
import os
import sys
import re
import subprocess

# Encontra o diretório raiz do projeto (dois níveis acima do arquivo atual)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)  # Insere o diretório raiz no início do sys.path
# Get full absolute path of data for the tests
data_path = os.path.join(os.path.dirname(__file__), "..", "data")

from modules.code_instrumenter.code_instrumenter import CodeInstrumenter
from modules.analyzer.static_analyzer import StaticAnalyzer
from modules.analyzer.type_extractor import TypeExtractor
from modules.code_instrumenter.code_formatter import CodeFormatter


class TestCodeInstrumenter(unittest.TestCase):
    def setUp(self):
        static_analyzer = StaticAnalyzer()
        types = TypeExtractor()
        code_instrumenter = CodeInstrumenter()
        # generate ast
        ast = static_analyzer.get_ast(data_path + "/SUT/sut.c")
        # get coupled data
        self.function_interface_list = static_analyzer.get_coupled_data(ast)
        # get primitive types
        typedef_to_primitive_type = types.get_types_from_ast(ast)
        # instrument code
        preprocessed_code = code_instrumenter.instrument_code(
            ast, self.function_interface_list, "sut", typedef_to_primitive_type
        )
        # format code
        code_formatter = CodeFormatter(data_path + "/SUT/sut.c", static_analyzer)
        code = code_formatter.format_code(preprocessed_code)
        include_abs_path_recorder = f'#include "{os.path.join(os.getcwd(), "modules", "coupling_recorder", "coupling_recorder.h")}"\n'

        self.code = include_abs_path_recorder + code

    def test_req8_verify_suti_coupled_params(self):
        # check whether all coupled parameters habe been inserted into the instrumented sut
        already_verified = []
        for function_interface in self.function_interface_list:
            for param in function_interface.input_parameters:
                if param.name not in already_verified:
                    pattern = rf'recorder_record\(".*?",\s*&?{re.escape(param.name)},\s*"{re.escape(param.type)}"\);'
                    already_verified.append(param.current_name)
                    self.assertTrue(
                        re.search(pattern, self.code),
                        f"[ERRO] Parameter: {param}, has not been inserted!",
                    )

    def test_req8_verify_code_compilation(self):
        # write code to file
        with open(data_path + "/SUT/suti/suti.c", "w+") as fp:
            fp.write(str(self.code))
        # check if the code has an error
        main_path = data_path + "/SUT/suti/main.c"
        sut_path = data_path + "/SUT/suti/suti.c"
        recorder_path = project_root + "/modules/coupling_recorder/coupling_recorder.c"
        list_path = project_root + "/modules/coupling_recorder/list.c"

        compilation = subprocess.run(
            [
                "gcc",
                main_path,
                sut_path,
                recorder_path,
                list_path,
                "-o",
                data_path + "/SUT/suti/suti",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            compilation.returncode, 0, f"Instrumented SUT compilation error"
        )
