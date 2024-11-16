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
        # Get the file extension
        file_extension = os.path.splitext(self.file_path)[1]
        
        # Read the file based on its extension
        if file_extension == ".xlsx" or file_extension == ".xls":
            df = pd.read_excel(self.file_path, sheet_name="TestVec", header=1)
            df_head = pd.read_excel(self.file_path, sheet_name="TestVec", header=None, nrows=2)
        elif file_extension == ".csv":
            df = pd.read_csv(self.file_path, header=1)
            df_head = pd.read_csv(self.file_path, header=None, nrows=2)

        # Determine the index for time and input comments
        time_index = 0
        input_comments_index = df.columns.get_loc("INPUT_COMMENTS")
        num_input = input_comments_index - (time_index + 1)

        # Verify and separate input and output parameters
        input_df, output_df = self.verify_parameters(df, parameters)

        # Check if the number of input columns matches the expected number
        if (len(input_df.columns) != num_input):
            raise ValueError("Review your test vector and your SUT. The number of inputs in test vector must exactly match the number of inputs in SUT. Some parameters in test vector file are leftover.")

        # Check if the number of rows in input and output DataFrames match
        if len(output_df) != len(input_df):
            raise ValueError("Review your test vector. The input and output must match in number of rows.")

        # Save the input DataFrame to a CSV file
        input_path = "./data/inputs.csv"
        input_df = pd.concat([df.iloc[:, time_index:time_index+1], input_df], axis=1)
        input_df.to_csv(input_path, index=False)

        # Save the output DataFrame to a CSV file
        output_path = "./data/outputs.csv"
        output_df = pd.concat([df.iloc[:, time_index:time_index+1], output_df], axis=1)
        output_df.to_csv(output_path, index=False)

        # Identify non-empty columns in the first row
        non_empty_indices = df_head.iloc[0].dropna().index
        # Create a new DataFrame with cells below the non-empty columns
        tolerance_data = df_head[non_empty_indices].T.iloc[:, ::-1]
        # Rename the first column to "Variable"
        tolerance_data.iat[0,0] = "Variable"
        # Save the tolerance DataFrame to a CSV file
        tolerance_data.to_csv("./data/tolerances.csv", index=False, header=False)

        return input_path
    

    def verify_parameters(self, df, parameters):
        input_df = pd.DataFrame()
        output_df = pd.DataFrame()

        # Verify and order pd as parameters.name order
        for param in parameters:
            if not param.pointer_depth: # If the parameter is not a pointer (input)
                if param.name in df.columns:
                    input_df[param.name] = df[param.name]  # Add the parameter to the input DataFrame
                else:
                    raise ValueError(f"Parameter {param.name} not found as an input header.")
            else: # If the parameter is a pointer (output)
                if param.name in df.columns:
                    output_df[param.name] = df[param.name] # Add the parameter to the output DataFrame
                else:
                    raise ValueError(f"Parameter {param.name} not found as an output header.")

        return input_df, output_df # Return the input and output DataFrames
    
    