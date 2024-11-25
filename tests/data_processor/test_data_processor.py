import unittest
import os
import sys
import pandas as pd

# Encontra o diretório raiz do projeto (dois níveis acima do arquivo atual)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)  # Insere o diretório raiz no início do sys.path
# Get full absolute path of data for the tests

from modules.data_processor.data_processor import DataProcessor
from models.function_interface import FunctionInterface
from modules.analyzer.static_analyzer import StaticAnalyzer



class TestDataProcessor(unittest.TestCase):
    def custom_setUp(self, data_path):
        static_analyzer = StaticAnalyzer()
        ast = static_analyzer.get_ast(data_path + "sut.c")

        self.function_interface_list = static_analyzer.get_coupled_data(ast)

        self.data_processor = DataProcessor(data_path)

        self.df_list = self.data_processor.analyze(self.function_interface_list)
    
    def test_req12_intermed_coverage_func(self):

        data_path = os.path.join(os.path.dirname(__file__),"data/")
        self.custom_setUp(data_path)
        # create ref dataframe
        expected_df_list = []
        # First DataFrame
        df1 = pd.DataFrame({"d_1": ["0.01-0.02", "0.02-0.03"]}, index=["a", "b"])
        expected_df_list.append(df1)
        # Second DataFrame
        df2 = pd.DataFrame({"d_2": ["0", "0.02-0.03"], "e_1": ["0.03-0.04", "0.02-0.03"]}, index=["c", "d_1"])
        expected_df_list.append(df2)

        for expected_df in expected_df_list:
            is_in_list = any(
                expected_df.equals(df_in_list) for df_in_list in self.df_list
            )
            self.assertTrue(is_in_list, f"The processed result is not as expected")

    def test_req12_intermed_coverage(self):

        # check dc coverage
        data_path = os.path.join(os.path.dirname(__file__), "data/")
        self.custom_setUp(data_path)

        dc_coverage = self.data_processor.get_coverage(self.df_list)
        self.assertTrue(
            abs(dc_coverage-83.33) < 0.00001,
            "[ERROR] The total coverage is different from the expected value.",
        )

    def test_req_20_pass_fail_intermed_coverage(self):
        # check pass/fail coverage rate
        data_path = os.path.join(os.path.dirname(__file__), "data/")
        self.custom_setUp(data_path)
        pass_fail_coverage, pass_fail_data = self.data_processor.get_pass_fail_coverage()
        self.assertEqual(
            pass_fail_coverage,
            100,
            "[ERROR] The pass/fail coverage does not match the expected value.",
        )

    def test_req12_zero_coverage_func(self):

        data_path = os.path.join(os.path.dirname(__file__),"data1/")
        self.custom_setUp(data_path)
        # create ref dataframe
        expected_df_list = []
        # First DataFrame
        df1 = pd.DataFrame({"a_1": ["0"]}, index=["i1"])
        expected_df_list.append(df1)
        # Second DataFrame
        df2 = pd.DataFrame({"o1_1": ["0"]}, index=["a_1"])
        expected_df_list.append(df2)

        for expected_df in expected_df_list:
            is_in_list = any(
                expected_df.equals(df_in_list) for df_in_list in self.df_list
            )
            self.assertTrue(is_in_list, f"The processed result is not as expected")

    def test_req12_zero_coverage(self):

        # check dc coverage
        data_path = os.path.join(os.path.dirname(__file__), "data1/")
        self.custom_setUp(data_path)

        dc_coverage = self.data_processor.get_coverage(self.df_list)
        self.assertTrue(
            abs(dc_coverage-0) < 0.00001,
            "[ERROR] The total coverage is different from the expected value.",
        )

    def test_req_20_pass_fail_zero_coverage(self):
        # check pass/fail coverage rate
        data_path = os.path.join(os.path.dirname(__file__), "data1/")
        self.custom_setUp(data_path)
        pass_fail_coverage, pass_fail_data = self.data_processor.get_pass_fail_coverage()
        self.assertEqual(
            pass_fail_coverage,
            100,
            "[ERROR] The pass/fail coverage does not match the expected value.",
        )

    def test_req12_full_coverage_func(self):

        data_path = os.path.join(os.path.dirname(__file__),"data2/")
        self.custom_setUp(data_path)
        # create ref dataframe
        expected_df_list = []
        # First DataFrame
        df1 = pd.DataFrame({"a_1": ["0.0-1.0"]}, index=["i1"])
        expected_df_list.append(df1)
        # Second DataFrame
        df2 = pd.DataFrame({"o1_1": ["0.0-1.0"]}, index=["a_1"])
        expected_df_list.append(df2)

        for expected_df in expected_df_list:
            is_in_list = any(
                expected_df.equals(df_in_list) for df_in_list in self.df_list
            )
            self.assertTrue(is_in_list, f"The processed result is not as expected")

    def test_req12_full_coverage(self):

        # check dc coverage
        data_path = os.path.join(os.path.dirname(__file__), "data2/")
        self.custom_setUp(data_path)

        dc_coverage = self.data_processor.get_coverage(self.df_list)
        self.assertTrue(
            abs(dc_coverage-100) < 0.00001,
            "[ERROR] The total coverage is different from the expected value.",
        )

    def test_req_20_pass_fail_full_coverage(self):
        # check pass/fail coverage rate
        data_path = os.path.join(os.path.dirname(__file__), "data2/")
        self.custom_setUp(data_path)
        pass_fail_coverage, pass_fail_data = self.data_processor.get_pass_fail_coverage()
        self.assertEqual(
            pass_fail_coverage,
            100,
            "[ERROR] The pass/fail coverage does not match the expected value.",
        )

    def test_req_20_pass_tolerance(self):
        # check pass/fail coverage rate
        data_path = os.path.join(os.path.dirname(__file__), "data3/")
        self.custom_setUp(data_path)
        pass_fail_coverage, pass_fail_data = self.data_processor.get_pass_fail_coverage()
        self.assertEqual(
            pass_fail_coverage,
            50,
            "[ERROR] The pass/fail coverage does not match the expected value.",
        )

