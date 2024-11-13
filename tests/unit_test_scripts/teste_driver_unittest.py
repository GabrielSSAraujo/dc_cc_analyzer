import sys
import os
import unittest
from unittest.mock import patch, mock_open, MagicMock

# Adicione o caminho do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.test_driver.test_driver_generator import TestDriver
from models.parameter import Parameter

class TestTestDriverGenerator(unittest.TestCase):

    def setUp(self):
        self.test_driver = TestDriver()

    def test_typing_mapping(self):
        parameters = [
            Parameter(name='param1', type='kcg_int', is_input=1),
            Parameter(name='param2', type='kcg_real', is_input=0)
        ]
        type_mapping, formatter_spec = self.test_driver.typing_mapping(parameters)
        self.assertEqual(type_mapping[0].type, 'int')
        self.assertEqual(type_mapping[1].type, 'double')
        self.assertEqual(formatter_spec['int'], '%d')
        self.assertEqual(formatter_spec['double'], '%lf')

    # def test_sut_caller(self):
    #     parameters = [
    #         Parameter(name='param1', type='int', is_input=1),
    #         Parameter(name='param2', type='double', is_input=0)
    #     ]
    #     sut_call = self.test_driver.sut_caller(parameters, 'SUT')
    #     self.assertEqual(sut_call, 'SUT(param1, &param2);')

    # def test_write_results_formatter(self):
    #     parameters = [
    #         Parameter(name='param1', type='int', is_input=1),
    #         Parameter(name='param2', type='double', is_input=0)
    #     ]
    #     formatter_spec = {
    #         'int': '%d',
    #         'float': '%f',
    #         'double': '%lf'
    #     }
    #     format_string, variable_list = self.test_driver.write_results_formatter(parameters, formatter_spec)
    #     self.assertEqual(format_string, '%lf\\n')
    #     self.assertEqual(variable_list, 'param2')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    @patch('shutil.copy')
    @patch('shutil.copyfile')
    @patch('modules.test_driver.data_extractor.DataExtractor.extract_data')
    @patch('pandas.read_csv')
    def test_generate_test_driver(self, mock_read_csv, mock_extract_data, mock_copyfile, mock_copy, mock_exists, mock_open):
        # Configurar os mocks
        mock_exists.return_value = True
        mock_open.return_value = MagicMock()
        mock_read_csv.return_value = MagicMock()
        mock_extract_data.return_value = ('input_path', 'output_path', [
            Parameter(name='param1', type='int', is_input=1),
            Parameter(name='param2', type='double', is_input=0)
        ])

        mock_copyfile.side_effect = lambda src, dst: open(dst, 'w').write(open(src).read())
        file_path = "./tests/data/test_vectors/TestVec_VCP-500-VC-01.xlsx"
        result_file_path =  "./tests/data/results_unittest.csv"
        
        # Chamar a função que estamos testando
        self.test_driver.generate_test_driver(file_path, result_file_path)
        
        # Verificar se os arquivos de saída foram gerados corretamente
        mock_open.assert_any_call(result_file_path, 'w')
        mock_open.assert_any_call('./modules/test_driver/c_files/test_driver.c', 'w')
        mock_copy.assert_called()
        mock_copyfile.assert_called()
        self.assertTrue(mock_exists(result_file_path))

if __name__ == '__main__':
    unittest.main()