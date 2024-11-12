import io
import unittest
from unittest.mock import patch

# Add InputValidator module to the path and import it
import sys
import os
module_path = os.path.join(os.path.dirname(__file__), "..", "..", "modules", "input_validator")
sys.path.insert(0, module_path)

from input_validator import InputValidator

# Get full absolute path of data for the tests
data_path = os.path.join(os.path.dirname(__file__), "..", "data")

class TestInputValidator(unittest.TestCase):

    def test_req5_valid_argv(self):
        iv = InputValidator(["dc_cc_analyzer", f"{data_path}/SUT/SUT.c", f"{data_path}/test_vectors/TestVec_VCP-500-VC-01.xlsx"])
        self.assertTrue(iv.validate_argv())
        del iv

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_req5_less_than_3_args(self, mock_stdout):
        iv = InputValidator(["dc_cc_analyzer", f"{data_path}/test_vectors/TestVec_VCP-500-VC-01.xlsx"])
        self.assertFalse(iv.validate_argv())
        self.assertEqual(mock_stdout.getvalue(), "[ERROR] Missing one or more tool inputs\n")
        del iv

    def test_req6_files_exist(self):
        iv = InputValidator(["dc_cc_analyzer", f"{data_path}/SUT/SUT.c", f"{data_path}/test_vectors/TestVec_VCP-500-VC-01.xlsx"])
        self.assertTrue(iv.validate_files())
        del iv

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_req6_file_doesnot_exist(self, mock_stdout):
        iv = InputValidator(["dc_cc_analyzer", f"{data_path}/main2.c", f"{data_path}/test_vectors/TestVec_VCP-500-VC-01.xlsx"])
        self.assertFalse(iv.validate_files())
        self.assertEqual(mock_stdout.getvalue(), f"[ERROR] Could not find SUT input file at path {data_path}/main2.c\n")
        del iv
    
    def test_req7_SUT_in_C(self):
        iv = InputValidator(["dc_cc_analyzer", f"{data_path}/SUT/SUT.c", f"{data_path}/test_vectors/TestVec_VCP-500-VC-01.xlsx"])
        self.assertTrue(iv.validate_sut())
        del iv
    
    def test_req8_TestVec_CSV(self):
        iv = InputValidator(["dc_cc_analyzer", f"{data_path}/SUT/SUT.c", f"{data_path}/test_vectors/TestVec_VCP-500-VC-01.csv"])
        self.assertTrue(iv.validate_test_vectors_file())
        del iv
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_req8_TestVec_TXT(self, mock_stdout):
        iv = InputValidator(["dc_cc_analyzer", f"{data_path}/SUT/SUT.c", f"{data_path}/test_vectors/TestVec_VCP-500-VC-01.txt"])
        self.assertFalse(iv.validate_test_vectors_file())
        self.assertEqual(mock_stdout.getvalue(), "[ERROR] Only Test Vectors in .xlsx or .csv are accepted\n")
        del iv

    def test_req9_good_TestVec(self):
        iv = InputValidator(["dc_cc_analyzer", f"{data_path}/SUT/SUT.c", f"{data_path}/test_vectors/TestVec_VCP-500-VC-01.csv"])
        self.assertTrue(iv.validate_test_vectors_format())
        del iv
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_req9_TestVec_without_tolerances(self, mock_stdout):
        iv = InputValidator(["dc_cc_analyzer", f"{data_path}/SUT/SUT.c", f"{data_path}/test_vectors/TestVec_VCP-500-VC-01_without_tolerances.csv"])
        self.assertFalse(iv.validate_test_vectors_format())
        self.assertEqual(mock_stdout.getvalue(), "[ERROR] Bad Test Vector format\n")
        del iv

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_req9_TestVec_without_inputcomments(self, mock_stdout):
        iv = InputValidator(["dc_cc_analyzer", f"{data_path}/SUT/SUT.c", f"{data_path}/test_vectors/TestVec_VCP-500-VC-01_without_inputcomments.csv"])
        self.assertFalse(iv.validate_test_vectors_format())
        self.assertEqual(mock_stdout.getvalue(), "[ERROR] Bad Test Vector format\n")
        del iv

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_req9_TestVec_without_time(self, mock_stdout):
        iv = InputValidator(["dc_cc_analyzer", f"{data_path}/SUT/SUT.c", f"{data_path}/test_vectors/TestVec_VCP-500-VC-01_without_time.csv"])
        self.assertFalse(iv.validate_test_vectors_format())
        self.assertEqual(mock_stdout.getvalue(), "[ERROR] Bad Test Vector format\n")
        del iv

if __name__ == "__main__":
    unittest.main(verbosity=2)