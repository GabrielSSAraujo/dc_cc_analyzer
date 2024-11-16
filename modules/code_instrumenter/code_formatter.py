from modules.analyzer.static_analyzer import StaticAnalyzer
import re
import difflib
import os
import shutil


class CodeFormatter:

    def __init__(self, file_path, analyzer: StaticAnalyzer):
        self._analyzer = analyzer
        # sut path
        self._sut_file_path = file_path
        self._sut_file_directory = os.path.dirname(self._sut_file_path)
        # teporary path to store sut includes
        if not os.path.exists("./temp"):
            os.makedirs("./temp")
        self._temp_include_path = "./temp/temp_includes.c"
        # temporary path to store preprocessed includes
        self._temp_preporcessed_include_path = "./temp/temp_preprocessed_includes.c"

    # create c file with sut includes
    def create_c_file_sut_includes(self):
        with open(self._sut_file_path, "r") as file:
            code = file.read()

        # find includes and defines
        expression = r"#\s*(define|include)\s+.*"
        matches = re.finditer(expression, code)

        with open(self._temp_include_path, "w+") as file:
            for match in matches:
                file.write(match.group(0) + "\n")

    def copy_headers_to_temp(self):
        origem = self._sut_file_directory
        destino = "./temp/"
        for root, dirs, files in os.walk(origem):
            for file in files:
                if file.endswith(".h"):
                    caminho_origem = os.path.join(root, file)
                    caminho_destino = os.path.join(destino, file)

                    # copy .h file to temp folder
                    shutil.copy2(caminho_origem, caminho_destino)

    def generate_preprocess_includes(self):
        includes_ast = self._analyzer.get_ast(self._temp_include_path)
        c_code_includes = self._analyzer.generate_c_code_from_ast(includes_ast)

        with open(self._temp_preporcessed_include_path, "w+") as file:
            file.write(c_code_includes)

    # compare files and return the difference betweeen them
    def compare_files(self, file1, file2):
        with open(file1, "r") as f1, open(file2, "r") as f2:
            file1_lines = f1.readlines()
            file2_lines = f2.readlines()

        # uising difflib to generate diff
        diff = difflib.unified_diff(file1_lines, file2_lines, lineterm="")

        # get includes from backup
        includes = ""
        with open(self._temp_include_path, "r") as inc_path:
            includes = inc_path.read()
        output = includes

        # filter lines to exclude default difflib characteres
        for line in diff:
            if (
                line.startswith("---")
                or line.startswith("+++")
                or line.startswith("@@")
            ):
                continue

            if line.startswith("-") or line.startswith("+"):
                output = output + str(line[1:] + "\n")
        return output

    def remove_temp_files(self):
        for filename in os.listdir("./temp"):
            file_path = os.path.join("./temp", filename)
            # Verifica se é um arquivo e o remove
            if os.path.isfile(file_path):
                os.remove(file_path)

    def format_code(self, preprocessed_code):

        preprocessed_code_file_path = "./temp/temp_preprocessed_sut.c"

        self.create_c_file_sut_includes()
        self.copy_headers_to_temp()
        self.generate_preprocess_includes()

        with open(preprocessed_code_file_path, "w+") as file:
            file.write(preprocessed_code)

        formatted_code = self.compare_files(
            preprocessed_code_file_path, self._temp_preporcessed_include_path
        )
        self.remove_temp_files()

        return formatted_code
