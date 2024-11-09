import io
import unittest
from unittest.mock import patch

from InputValidator import InputValidator

class TestInputValidator(unittest.TestCase):
    def test_req5_valid_argv(self):
        iv = InputValidator(["test", "test_files/main.c", "test_files/TestVec_VCP-500-VC-01.xlsx"])
        self.assertTrue(iv.validate_argv())
        del iv

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_req5_less_than_3_args(self, mock_stdout):
        iv = InputValidator(["test", "test_files/TestVec_VCP-500-VC-01.xlsx"])
        self.assertFalse(iv.validate_argv())
        self.assertEqual(mock_stdout.getvalue(), "[ERROR] Missing one or more tool inputs\n")
        del iv

    def test_req6_files_exit(self):
        iv = InputValidator(["test", "test_files/main.c", "test_files/TestVec_VCP-500-VC-01.xlsx"])
        self.assertTrue(iv.validate_files())
        del iv

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_req6_file_dont_exist(self, mock_stdout):
        iv = InputValidator(["test", "test_files/main2.c", "test_files/TestVec_VCP-500-VC-01.xlsx"])
        self.assertFalse(iv.validate_files())
        self.assertEqual(mock_stdout.getvalue(), "[ERROR] Could not find SUT input file at path test_files/main2.c\n")
        del iv
    
    def test_req7_SUT_in_C(self):
        iv = InputValidator(["test", "test_files/main.c", "test_files/TestVec_VCP-500-VC-01.xlsx"])
        self.assertTrue(iv.validate_sut())
        del iv
    
    def test_req8_TestVec_CSV(self):
        iv = InputValidator(["test", "test_files/main.c", "test_files/TestVec_VCP-500-VC-01.csv"])
        self.assertTrue(iv.validate_test_vectors_file())
        del iv
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_req8_TestVec_TXT(self, mock_stdout):
        iv = InputValidator(["test", "test_files/main.c", "test_files/TestVec_VCP-500-VC-01.txt"])
        self.assertFalse(iv.validate_test_vectors_file())
        self.assertEqual(mock_stdout.getvalue(), "[ERROR] Only Test Vectors in .xlsx or .csv are accepted\n")
        del iv

    def test_req9_good_TestVec(self):
        iv = InputValidator(["test", "test_files/main.c", "test_files/TestVec_VCP-500-VC-01.csv"])
        self.assertTrue(iv.validate_test_vectors_format())
        del iv
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_req9_TestVec_without_tolerances(self, mock_stdout):
        iv = InputValidator(["test", "test_files/main.c", "test_files/TestVec_VCP-500-VC-01_without_tolerances.csv"])
        self.assertFalse(iv.validate_test_vectors_format())
        self.assertEqual(mock_stdout.getvalue(), "[ERROR] Bad Test Vector format\n")
        del iv

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_req9_TestVec_without_tolerances(self, mock_stdout):
        iv = InputValidator(["test", "test_files/main.c", "test_files/TestVec_VCP-500-VC-01_without_inputcomments.csv"])
        self.assertFalse(iv.validate_test_vectors_format())
        self.assertEqual(mock_stdout.getvalue(), "[ERROR] Bad Test Vector format\n")
        del iv

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_req9_TestVec_without_tolerances(self, mock_stdout):
        iv = InputValidator(["test", "test_files/main.c", "test_files/TestVec_VCP-500-VC-01_without_time.csv"])
        self.assertFalse(iv.validate_test_vectors_format())
        self.assertEqual(mock_stdout.getvalue(), "[ERROR] Bad Test Vector format\n")
        del iv

if __name__ == "__main__":
    unittest.main(verbosity=2)