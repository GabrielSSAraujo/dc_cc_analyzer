import unittest
import os
import sys

# Configura o sys.path para incluir o diretório raiz do projeto
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Descobre e executa os testes
test_loader = unittest.TestLoader()
test_suite = test_loader.discover(start_dir="tests", pattern="test_*.py")
test_runner = unittest.TextTestRunner(verbosity=2)
test_runner.run(test_suite)
