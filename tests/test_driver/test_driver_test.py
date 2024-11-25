"""
 @file: test_driver_test.py
 @brief [Descrição breve do arquivo]
 
 REQ - The tool should create a Test Driver for the (test_driver_sut.c),
 whose function is to execute the SUT with the inputs present in the 
 Test Vectors and record the outputs produced for each input in a file called 
 "results_sut.csv".
 
 REQ - The tool should create a Test Driver for the Instrumented SUT (test_driver_suti.c),
 whose function is to execute the Instrumented SUT with the inputs present in the 
 Test Vectors and record the outputs produced for each input in a file called 
 "results_suti.csv".
"""

import unittest
import subprocess
import os
import platform
import sys
import pandas as pd

# Encontra o diretório raiz do projeto (dois níveis acima do arquivo atual)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)  # Insere o diretório raiz no início do sys.path
# Get full absolute path of data for the tests

from modules.test_driver.data_extractor import DataExtractor
from modules.test_driver.test_driver_generator import TestDriver
from models.parameter import Parameter


class TestTestDriverGenerator(unittest.TestCase):

    def setUp(self):

        self.test_driver = TestDriver()
        self.CType_parameters = [
            Parameter(type="int", name="i1", pointer_depth=0),
            Parameter(type="int", name="o1", pointer_depth=1),
        ]
        self.formatter_spec = {"int": "%d"}

        self.data_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "data")
        )
        self.path_sut = self.data_path + "/SUT/sut.c"
        data_extractor = DataExtractor(self.data_path + "/SUT/TestVec.csv")
        self.input_path = data_extractor.extract_data(self.CType_parameters)

    def test_generating_testDriver_c_files(self):
        # Generate test_driver_sut.c
        self.original_file_path_sut = "./modules/test_driver/c_files/test_driver_sut.c"
        self.result_file_path_sut = "./data/results_sut.csv"
        self.test_driver.test_driver_generator(
            self.input_path,
            self.data_path + "/SUT/sut.h",
            self.result_file_path_sut,
            self.original_file_path_sut,
            self.CType_parameters,
            self.formatter_spec,
        )
        # test if exists
        self.assertTrue(
            os.path.exists(self.original_file_path_sut),
            f"{self.original_file_path_sut} was not created",
        )

        # Generate test_driver_suti.c
        self.original_file_path_suti = (
            "./modules/test_driver/c_files/test_driver_suti.c"
        )
        self.result_file_path_suti = "./data/results_suti.csv"
        self.test_driver.test_driver_generator(
            self.input_path,
            self.data_path + "/SUT/sut.h",
            self.result_file_path_suti,
            self.original_file_path_suti,
            self.CType_parameters,
            self.formatter_spec,
        )
        # test if exists
        self.assertTrue(
            os.path.exists(self.original_file_path_suti),
            f"{self.original_file_path_suti} was not created",
        )

    def compile_and_run(self, executable_path):

        if platform.system() == "Windows":
            compilation = subprocess.run(
                [
                    "mingw32-make",
                    "all",
                    f"SRC_DIR={os.path.dirname(self.path_sut)}",
                    # f"SRC_TEST_DRIVER={project_root}/modules/test_driver/c_files",
                ],
                stdout=subprocess.DEVNULL,
            )
        else:

            compilation = subprocess.run(
                [
                    "make",
                    "all",
                    f"SRC_DIR={os.path.dirname(self.path_sut)}",
                    # f"SRC_TEST_DRIVER={project_root}/tests/test_driver/c_files",
                ],
                stdout=subprocess.DEVNULL,
            )
        # test if compilation was successful
        self.assertEqual(
            compilation.returncode,
            0,
            f"Compilation failed with return code {compilation.returncode}",
        )

        execution = subprocess.run(
            [f"{executable_path}"], capture_output=True, text=True
        )

        # test if execution was successful
        self.assertEqual(
            execution.returncode,
            0,
            f"Execution failed with return code {execution.returncode}",
        )

    def verify_csv_files(self, result_file_path):
        # test if result file was created
        self.assertTrue(os.path.exists(result_file_path))

        ref_result_df = pd.read_csv(self.data_path + "/result_ref.csv")
        result_df = pd.read_csv(project_root + "/data/results_suti.csv")

        self.assertTrue(ref_result_df.equals(result_df))

    def test_driver_suite(self):
        # tests suite
        self.test_generating_testDriver_c_files()
        self.compile_and_run("./testdriver_sut")
        self.compile_and_run("./testdriver_suti")
        self.verify_csv_files(self.result_file_path_sut)
        self.verify_csv_files(self.result_file_path_suti)
