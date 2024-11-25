import unittest
import os
import sys
import pandas as pd

# Encontra o diretório raiz do projeto (dois níveis acima do arquivo atual)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)  # Insere o diretório raiz no início do sys.path
# Get full absolute path of data for the tests
data_path = os.path.join(os.path.dirname(__file__), "data")

from modules.data_processor.data_processor import DataProcessor
from models.function_interface import FunctionInterface
from models.parameter import Parameter


class TestDataProcessor(unittest.TestCase):
    def setUp(self):

        # create data process object
        path = data_path + "/"
        self.data_processor = DataProcessor(path)

        # create components
        CA_in_param_1 = Parameter("int", "a", "a", "")
        CA_in_param_2 = Parameter("int", "b", "b", "")
        CA_out_param_3 = Parameter("int", "c", "c_1", "*")
        compA = FunctionInterface(
            "compA", [CA_in_param_1, CA_in_param_2], [CA_out_param_3]
        )

        CB_in_param_1 = Parameter("int", "d", "d", "")
        CB_out_param_2 = Parameter("int", "e", "e_1", "*")
        compB = FunctionInterface(
            "compB", [CA_out_param_3, CB_in_param_1], [CB_out_param_2]
        )
        # add components
        self.function_list = [compA, compB]

        # create ref dataframe
        self.expected_df_list = []
        # First DataFrame
        df1 = pd.DataFrame({"c_1": ["0.01-0.02", "0.02-0.03"]}, index=["a", "b"])
        self.expected_df_list.append(df1)
        # Second DataFrame
        df2 = pd.DataFrame({"e_1": ["0.02-0.03", "0.03-0.04"]}, index=["c_1", "d"])
        self.expected_df_list.append(df2)

        # get analysis
        self.result_df_list = self.data_processor.analyze(self.function_list)

    def test_req12_coverage_criteria(self):
        for expected_df in self.expected_df_list:
            is_in_list = any(
                expected_df.equals(df_in_list) for df_in_list in self.result_df_list
            )
            self.assertTrue(is_in_list, f"The processed result is not as expected")

    def test_req12_check_toal_coverage(self):
        total_coverage = self.data_processor.get_coverage(self.result_df_list)
        self.assertEqual(
            total_coverage,
            100,
            "[ERROR] The total coverage is different from the expected value.",
        )

    def test_req20_check_pass_fail_rate(self):
        pass_fail_rate, _ = self.data_processor.get_pass_fail_coverage()
        self.assertEqual(
            pass_fail_rate,
            80,
            "[ERROR] The pass/fail coverage does not match the expected value.",
        )
