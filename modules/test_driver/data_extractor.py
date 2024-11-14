"""
 @file: data_extractor.py
 @brief [Descrição breve do arquivo]

 @date: 2024-11-12 17:29
 @author: Aline Andreotti Urna
 @e-mail: aline.urna@gmail.com
"""
import pandas as pd
import os
from models.parameter import Parameter
    
    
class DataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        

    def extract_data(self, parameters):
        # Verifica a extensão do arquivo e lê o arquivo
        file_extension = os.path.splitext(self.file_path)[1]
        if file_extension == ".xlsx" or file_extension == ".xls":
            # Lê o arquivo Excel 'dados.xlsx' na aba 'TestVec' com cabeçalho na segunda linha (índice 1)
            df = pd.read_excel(self.file_path, sheet_name="TestVec", header=1)
            # Lê a linha específica [1°linha] (skiprows é zero-indexado)
            # Lê as duas primeiras linhas do arquivo para identificar as colunas não vazias [na segunda linha consta os nomes das variáveis de interesse]
            df_head = pd.read_excel(self.file_path, sheet_name="TestVec", header=None, nrows=2)
        elif file_extension == ".csv":
            # Lê o arquivo CSV com cabeçalho na segunda linha (índice 1)
            df = pd.read_csv(self.file_path, header=1)
            # Lê a linha específica [1°linha] (skiprows é zero-indexado)
            # Lê as duas primeiras linhas do arquivo para identificar as colunas não vazias [na segunda linha consta os nomes das variáveis de interesse]
            df_head = pd.read_csv(self.file_path, header=None, nrows=2)
        #else:  #deixei aqui apenas enquanto não implementamos inputValidator
            #raise ValueError("Formato de arquivo não suportado. Use .csv ou .xlsx") #se não for .csv ou .xlsx, retorna erro

        # parameters = self.generate_parameters()        
        # Imprimir os parâmetros para verificar **DEBUG**
        # for param in parameters:
        #     print(f"Type: {param.type}, Name: {param.name}, Is Input: {param.is_input}")
        

        # Encontra os índices das colunas
        time_index = 0  #convencionado que a coluna de tempo é a primeira
        input_comments_index = df.columns.get_loc("INPUT_COMMENTS")
        
        # Calcula o número de colunas de input
        num_input = input_comments_index - (time_index + 1)
        input_df, output_df = self.verify_parameters(df, parameters)
        

        if (len(input_df.columns) != num_input):
            raise ValueError("Review your test vector and your SUT. The number of inputs in test vector must exactly match the number of inputs in SUT. Some parameters in test vector file are leftover.")

        if len(output_df) != len(input_df):
            raise ValueError("Review your test vector. The input and output must match in number of rows.")
        
        
        input_path = "./data/inputs.csv"
        input_df = pd.concat([df.iloc[:, time_index:time_index+1], input_df], axis=1)
        input_df.to_csv(input_path, index=False)  # TO DO:mudar o local onde salva os arquivos??

        
        output_path = "./data/outputs.csv"
        output_df = pd.concat([df.iloc[:, time_index:time_index+1], output_df], axis=1)
        output_df.to_csv(output_path, index=False)  # TO DO:mudar o local onde salva os arquivos??

        # Identifica as colunas não vazias na primeira linha (índice 0)
        non_empty_indices = df_head.iloc[0].dropna().index
        # Cria um novo DataFrame com as células correspondentes que estão imediatamente abaixo das colunas não vazias
        tolerance_data = df_head[non_empty_indices].T
        # Espelha o DataFrame (inverte a ordem das colunas)
        tolerance_data = tolerance_data.iloc[:, ::-1]
        #mudando o nome da primeira coluna para "Variable"
        tolerance_data.iat[0,0] = "Variable"
        tolerance_data.to_csv("./data/tolerances.csv", index=False, header=False)
        
        #lembrete: considerar a primeira linha do tolerance.csv como o "nome das colunas"
        #ou seja, a parte importante é a segunda linha em diante.
        #na primeira linha estão as labels da coluna, na segunda linha em diante estão os valores de tolerância.

        return input_path, output_path
    
    #generate_parameters está sendo usado para criar os dados sintéticos. posteriormente, será substituido pelo analisador estático
    def generate_parameters(self):
        # Definir as listas conforme especificado
        types = ["kcg_int", "kcg_int", "kcg_int", "kcg_int", "int", "int", "int", "int", "int", "int", "int", "int", "int"]
        names = ["SUTI1", "SUTI2", "SUTI3", "SUTI4", "SUTI5", "SUTI6", "SUTI7", "SUTO6", "SUTO5", "SUTO4", "SUTO3", "SUTO2", "SUTO1"]
        is_input = [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]

        # Criar a lista de objetos Parameter
        parameters = []
        for t, n, i in zip(types, names, is_input):
            param = Parameter(type=t, name=n, is_input=bool(i))
            parameters.append(param)
            
        #questionamento: essa lista de parâmetros conterá apenas as variáveis de assinatura da função desejada (SUT)?
        #caso não, haverá alguma identificação para separar as variáveis de assinatura da função SUT das demais funções/variáveis?
        return parameters
    
    #função que re-organiza o dataframe de input e output para corresponder com a ordem de chamada das variaveis na função SUT
    #para garantir que elas estejam na ordem certo da chamada
    #re-arrumamamos o arquivo que será lido pelo teste_driver.c
    #de acordo com a ordem de assinaura da função SUT
    def verify_parameters(self, df, parameters):
        # Inicializa os DataFrames vazios
        input_df = pd.DataFrame()
        output_df = pd.DataFrame()

        # Verificar e ordenar os DataFrames conforme parameters.name
        for param in parameters:
            if not param.pointer_depth:
                if param.name in df.columns:
                    input_df[param.name] = df[param.name]
                else:
                    raise ValueError(f"Parameter {param.name} not found as an input header.")
            else:
                if param.name in df.columns:
                    output_df[param.name] = df[param.name]
                else:
                    raise ValueError(f"Parameter {param.name} not found as an output header.")

        return input_df, output_df
    
    