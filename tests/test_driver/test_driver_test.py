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
from unittest.mock import patch
import subprocess
import os

from modules.test_driver.data_extractor import DataExtractor
from modules.test_driver.test_driver_generator import TestDriver
from models.parameter import Parameter

class TestTestDriverGenerator(unittest.TestCase):

    def setUp(self):
        self.test_driver = TestDriver()
        self.path_sut = "./tests/test_driver/SUT/sut.c"
        self.CType_parameters = [
            Parameter(type="int", name="SUTI1", pointer_depth=0),
            Parameter(type="int", name="SUTI2", pointer_depth=0),
            Parameter(type="float", name="SUTI3", pointer_depth=0),
            Parameter(type="int", name="SUTI4", pointer_depth=0),
            Parameter(type="int", name="SUTI5", pointer_depth=0),
            Parameter(type="int", name="SUTI6", pointer_depth=0),
            Parameter(type="int", name="SUTI7", pointer_depth=0),
            Parameter(type="int", name="SUTO2", pointer_depth=1),
            Parameter(type="float", name="SUTO1", pointer_depth=1)
        ]
        self.formatter_spec = {
            "int": "%d",
            "float": "%f"
        }
        
        data_extractor = DataExtractor("./tests/data/test_vectors/TestVec_VCP-500-VC-01.csv")
        self.input_path = data_extractor.extract_data(self.CType_parameters)
    
    def compile_and_run(self, original_file_path, executable_path):
        include_dirs = "-I ./modules/coupling_recorder -I ./tests/test_driver/SUT -I ./modules/list"
        compile_command = f"gcc {include_dirs} ./modules/coupling_recorder/coupling_recorder.c ./modules/coupling_recorder/list.c {original_file_path} -o {executable_path}"
        
        try:
            subprocess.run(compile_command, shell=True, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            self.fail(f"Compilation failed: {e.stderr}")
        
        result = subprocess.run(executable_path, shell=True, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Execution failed with return code {result.returncode}")

    def test_test_driver_sut(self):
        result_file_path = "./tests/test_driver/results_sut.csv"
        original_file_path = "./tests/test_driver/test_driver_sut.c"
        executable_path = ".\\tests\\test_driver\\test_driver_sut"
        
        self.test_driver.test_driver_generator(
            self.input_path,
            self.path_sut,
            result_file_path,
            original_file_path,
            self.CType_parameters,
            self.formatter_spec
        )
        
        self.assertTrue(os.path.exists(original_file_path), f'{original_file_path} was not created')
        self.compile_and_run(original_file_path, executable_path)
        self.assertTrue(os.path.exists(result_file_path), f'{result_file_path} was not created')

    def test_test_driver_suti(self):
        result_file_path = "./tests/test_driver/results_suti.csv"
        original_file_path = "./tests/test_driver/test_driver_suti.c"
        executable_path = ".\\tests\\test_driver\\test_driver_suti"
        
        self.test_driver.test_driver_generator(
            self.input_path,
            self.path_sut,
            result_file_path,
            original_file_path,
            self.CType_parameters,
            self.formatter_spec
        )
        
        self.assertTrue(os.path.exists(original_file_path), f'{original_file_path} was not created')
        self.compile_and_run(original_file_path, executable_path)
        self.assertTrue(os.path.exists(result_file_path), f'{result_file_path} was not created')

if __name__ == "__main__":
    unittest.main()