import unittest
import os
import sys


# Encontra o diretório raiz do projeto (dois níveis acima do arquivo atual)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)  # Insere o diretório raiz no início do sys.path
# Get full absolute path of data for the tests
data_path = os.path.join(os.path.dirname(__file__), "..", "data")

from modules.analyzer.static_analyzer import StaticAnalyzer
from modules.data_couplings_flow.data_couplings_flow import DataCouplingFlow
from models.parameter import Parameter


class TestDataCouplingsFlow(unittest.TestCase):
    def setUp(self):
        static_analyzer = StaticAnalyzer()
        ast = static_analyzer.get_ast(data_path + "/SUT_nested_params/sut.c")
        self.coupled_data = static_analyzer.get_coupled_data(ast)
        self.functions = static_analyzer.get_func_metadata()

    # def test_req16_output_to_couplings_map(self):

    #     reference_mapping = {
    #         "suto1": ["a1", "a2", "a2_aux", "a3", "a4"],
    #         "suto2": ["a1", "a3"],
    #     }

    #     df = DataCouplingFlow(self.coupled_data, self.functions)
    #     df.analyze_data_flow()
    #     output_mapping = df.get_coupling_to_output_mapping()

    #     for ref_key, _ in reference_mapping.items():
    #         self.assertIn(ref_key, output_mapping)
