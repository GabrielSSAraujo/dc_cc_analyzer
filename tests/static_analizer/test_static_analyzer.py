import unittest
import os
import sys


# Encontra o diretório raiz do projeto (dois níveis acima do arquivo atual)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)  # Insere o diretório raiz no início do sys.path
# Get full absolute path of data for the tests
data_path = os.path.join(os.path.dirname(__file__), "..", "data")

from modules.analyzer.static_analyzer import StaticAnalyzer
from models.parameter import Parameter


class TestStaticAnalyzer(unittest.TestCase):
    def setUp(self):
        self.static_analyzer = StaticAnalyzer()

    def get_coupled_param_list(self, coupled_data):
        identified_coupled_params = []
        for coupled in coupled_data:
            for param in coupled.parameters:
                if param not in identified_coupled_params:
                    identified_coupled_params.append(param)
        return identified_coupled_params

    def test_req10_single_level_coupling(self):
        ast = self.static_analyzer.get_ast(data_path + "/SUT/sut.c")

        coupled_param_list = [
            Parameter("int", "suto1"),  # compA - compCeD  :SUTO1
            Parameter("int", "suto2"),  # compA - compC: SUTO2
            Parameter("int", "suto3"),  # compB - compC: SUTO3
            Parameter("int", "suto2_aux"),  # compC - compD: SUTO2_aux
            Parameter("int", "suto4"),  # compC - compD: SUTO4
        ]

        coupled_data = self.static_analyzer.get_coupled_data(ast)
        identified_coupled_params = self.get_coupled_param_list(coupled_data)

        self.assertTrue(
            all(elem in identified_coupled_params for elem in coupled_param_list)
        )

    def test_req10_nested_param_coupling(self):
        ast = self.static_analyzer.get_ast(data_path + "/SUT_nested_params/sut.c")

        coupled_param_list = [
            Parameter("int", "suto1"),  # compA - compC/D  :SUTO1
            Parameter("double", "suto2"),  # compA - compE: SUTO2
            Parameter("float", "suto3"),  # compB - compC: SUTO3
            Parameter("double", "suto2_aux"),  # compE - compC: SUT2_aux
            Parameter("double", "suto2_aux_aux"),  # compC - compD: SUTO2_aux_aux
            Parameter("double", "suto6"),  # compC - compD: SUTO6
        ]

        coupled_data = self.static_analyzer.get_coupled_data(ast)
        identified_coupled_params = self.get_coupled_param_list(coupled_data)

        self.assertTrue(
            all(elem in identified_coupled_params for elem in coupled_param_list)
        )

    def test_req10_duplicate_component_params(self, mock_out=None):
        ast = self.static_analyzer.get_ast(
            data_path + "/SUT_duplicated_components/sut.c"
        )

        coupled_param_list = [
            Parameter("int", "suto1"),  # compA - compA  :SUTO1
            Parameter("int", "suto1_aux"),  # compA - compC/D: SUTO1_aux
            Parameter("double", "suto2"),  # compA - compE: SUTO2
            Parameter("double", "suto2_aux"),  # compE - compA: SUTO2_aux
            Parameter("double", "suto2_aux_aux"),  # compA - compC: SUTO2_aux_aux
            Parameter(
                "double", "suto2_aux_aux_aux"
            ),  # compC - compD: SUTO2_aux_aux_aux
            Parameter("float", "suto3"),  # compB - compC: SUTO3
            Parameter("double", "result"),  # compC - compD: result
        ]

        coupled_data = self.static_analyzer.get_coupled_data(ast)
        identified_coupled_params = self.get_coupled_param_list(coupled_data)
        self.assertTrue(
            all(elem in identified_coupled_params for elem in coupled_param_list)
        )


# if __name__ == "__main__":
#     unittest.main(verbosity=2)
