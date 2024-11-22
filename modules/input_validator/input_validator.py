import os.path
import pandas as pd


class InputValidator:
    def __init__(self, argv):
        self.__argv = argv

    def validate(self) -> bool:
        try:
            return (
                self.validate_argv()
                and self.validate_files()
                and self.validate_sut()
                and self.validate_test_vectors_file()
                and self.validate_test_vectors_format()
            )
        except:
            print("[ERROR] Something went wrong while trying to validate inputs")
            return False

    # REQ-3: Caso a Ferramenta não receba um de seus parâmetros de entrada, ela deve produzir uma mensagem de erro no terminal informando "[ERROR] Missing one or more tool inputs".
    def validate_argv(self) -> bool:
        if len(self.__argv) != 3:
            print("[ERROR] Missing one or more tool inputs")
            return False
        return True

    # REQ-4: Caso um dos arquivos de entrada não exista, a Ferramenta deve produzir uma mensagem de erro informando "[ERROR] Could not find {input} input file at path {path}", onde {input} deve ser substituído por "SUT" ou "TestVector" conforme o caso e {path} deve ser substituído pelo caminho passado pelo usuário para o referido arquivo.
    def validate_files(self) -> bool:
        if not (os.path.isfile(self.__argv[1])):
            print(f"[ERROR] Could not find SUT input file at path {self.__argv[1]}")
            return False
        if not (os.path.isfile(self.__argv[2])):
            print(
                f"[ERROR] Could not find TestVector input file at path {self.__argv[2]}"
            )
            return False
        return True

    # REQ-5: Caso a Ferramenta receba como entrada um SUT que não esteja em linguagem C, ela deve produzir uma mensagem de erro no terminal informando "[ERROR] Only SUT in C are accepted".
    def validate_sut(self) -> bool:
        _, file_extension = os.path.splitext(self.__argv[1])
        if file_extension != ".c":
            print("[ERROR] Only SUT in C are accepted")
            return False
        return True

    # REQ-6: Caso a Ferramenta receba como entrada um arquivo de Test Vectors que não esteja no formato Excel (.xlsx ou .xls) ou CSV, a Ferramenta deve produzir uma mensagem de erro informando "[ERROR] Only Test Vectors in .xlsx, .xls or .csv are accepted".
    def validate_test_vectors_file(self) -> bool:
        _, file_extension = os.path.splitext(self.__argv[2])
        if (
            file_extension != ".csv"
            and file_extension != ".xlsx"
            and file_extension != ".xls"
        ):
            print("[ERROR] Only Test Vectors in .xlsx, .xls or .csv are accepted")
            return False
        return True

    # REQ-7: A Ferramenta deve verificar se a planilha de Test Vectors segue o formato indicado na aba TestVec e, caso possua alguma divergência, deve produzir a mensagem "[ERROR] Bad Test Vector format".
    # Premissa: o separador do arquivo csv é a virgula e o separador decimal é o ponto.
    def validate_test_vectors_format(self) -> bool:
        _, file_extension = os.path.splitext(self.__argv[2])
        tolerances_row = []
        header_row = []

        # Load desired rows depending on file extension
        if file_extension == ".xlsx" or file_extension == ".xls":
            tolerances_row = pd.read_excel(self.__argv[2], nrows=0).columns
            header_row = pd.read_excel(self.__argv[2], skiprows=1, nrows=0).columns

        elif file_extension == ".csv":
            tolerances_row = pd.read_csv(self.__argv[2], nrows=0).columns
            header_row = pd.read_csv(self.__argv[2], skiprows=1, nrows=0).columns

        # Verifiy if tolerances row is present
        if tolerances_row[0] != "Tolerances":
            print("[ERROR] Bad Test Vector format")
            return False

        # Check if header structure follows the pattern "Time Inputs INPUT_COMMENTS Outputs OUTPUT_COMMENTS"
        if (
            ("Time" in header_row)
            and ("INPUT_COMMENTS" in header_row)
            and ("OUTPUT_COMMENTS" in header_row)
        ):
            time_index = header_row.get_loc("Time")
            input_comments_index = header_row.get_loc("INPUT_COMMENTS")
            output_comments_index = header_row.get_loc("OUTPUT_COMMENTS")

            if (
                time_index < input_comments_index
                and input_comments_index < output_comments_index
            ):
                # OK, do nothing
                pass
            else:
                print("[ERROR] Bad Test Vector format")
                return False
        else:
            print("[ERROR] Bad Test Vector format")
            return False

        return True
