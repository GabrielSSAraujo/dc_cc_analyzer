# PARA PENSAR:
# 1)VAMOS ESPECIFICAR/OU DEIXAR DINÂMICO A PASTA PARA SALVAR OS ARQUIVOS GERADOS?? atualmente está na raiz
# 2)VAMOS DEIXAR DINAMICO O NOME DOS ARQUIVOS GERADOS?? (ESSES ARQUIVOS INTERMEDIARIOS PENSO QUE NÃO)
# SE DEIXAR UM NOME FIXO FICA MAIS FÁCIL DE LIDAR, E NÃO IMPACTA NA EXPERIENCIA DO USUÁRIO, VISTO QUE
# O IMPORTANTE PARA ELE É O ARQUIVO FINAL GERADO (relatório)
# vamos apagar os arquivos intermediários?? (input.csv e output.csv) e disponibilizar apenas o relatório final??

import pandas as pd


class DataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_data_from_excel(self):
        # Lê o arquivo Excel 'dados.xlsx' na aba 'TestVec' com cabeçalho na segunda linha (índice 1)
        df = pd.read_excel(self.file_path, sheet_name="TestVec", header=1)

        # Encontra os índices das colunas
        time_index = df.columns.get_loc("Time")
        input_comments_index = df.columns.get_loc("INPUT_COMMENTS")
        output_comments_index = df.columns.get_loc("OUTPUT_COMMENTS")

        # Seleciona as colunas entre 'Time' (exclusivo) e 'INPUT_COMMENTS' (exclusivo) para 'input.csv'
        input_columns = df.iloc[:, time_index + 1 : input_comments_index]
        input_shape = input_columns.shape
        input_columns.to_csv(
            "./test_vector/input.csv", index=False
        )  # TO DO:mudar o local onde salva os arquivos??

        # Seleciona as colunas entre 'INPUT_COMMENTS' (exclusivo) e 'OUTPUT_COMMENTS' (exclusivo) para 'output.csv'
        output_columns = df.iloc[:, input_comments_index + 1 : output_comments_index]
        output_shape = output_columns.shape
        output_columns.to_csv(
            "./test_vector/output.csv", index=False
        )  # TO DO:mudar o local onde salva os arquivos??

        print("Arquivos 'input.csv' e 'output.csv' foram gerados com sucesso.")

        # Retorna as formas(linha e coluna) dos DataFrames
        return input_shape, output_shape
