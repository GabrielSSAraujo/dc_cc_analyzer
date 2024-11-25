import shutil

class TestDriver:

    def create_variables(self, CType_parameters):
        # Create a list of strings in the format "parameter.type parameter.name;"
        variable_strings = [
            f"\t{param.type} {param.name};" for param in CType_parameters
        ]
    
        # Join all the strings into a single string, each on its own line
        variable_strings = "\n".join(variable_strings)
        
        return variable_strings  # Return the generated variable declarations

    def header_generator(self, CType_parameters):
        # Create a list of parameter names for parameters that are pointers (outputs)
        header = [param.name for param in CType_parameters if param.pointer_depth]
    
        # Join all the parameter names into a single string, separated by commas
        header = ",".join(header)
        
        return header  # Return the generated header string

    def generate_formatting_code(self, params):
        # Define lists of types for different conversion functions
        atoi = [
            "int", "short", "unsigned int", "unsigned short", "bool", "size_t",
            "int8_t", "int16_t", "int32_t", "uint8_t", "uint16_t", "uint32_t"
        ]
        atof = ["float", "double", "long double"]
        atol = ["long", "unsigned long"]
        atoll = ["long long", "int64_t", "uint64_t"]
    
        # Initialize a list to hold the generated code lines
        code_lines = []
    
        # Iterate over the parameters
        for param in params:
            if not param.pointer_depth:  # Check if the parameter is not a pointer
                code_lines.append('\t\ttoken = strtok(NULL, ",");')  # Add code to get the next token
                conversion_type = ""
                if param.type in atoi:
                    conversion_type = "atoi"  # Use atoi for integer types
                elif param.type in atof:
                    conversion_type = "atof"  # Use atof for floating-point types
                elif param.type in atol:
                    conversion_type = "atol"  # Use atol for long types
                elif param.type in atoll:
                    conversion_type = "atoll"  # Use atoll for long long types
                if conversion_type != "":
                    code_lines.append(
                        f"\t\tif (token != NULL) {param.name} = {conversion_type}(token);"
                    )  # Add code to convert the token to the appropriate type
                else:
                    code_lines.append(
                        f"\t\tif (token != NULL) {param.name} = token[0];"
                    )  # Add code to assign the token directly if no conversion is needed
        return code_lines  # Return the list of generated code lines

    def sut_caller(self, CType_parameters, sut_name):
        # Create a list to hold the parameter strings
        param_strings = []
        
        # Iterate over the CType parameters
        for param in CType_parameters:
            if param.pointer_depth:  # Check if the parameter is a pointer
                param_strings.append(f"&{param.name}")  # Add the parameter name with an address-of operator
            else:
                param_strings.append(param.name)  # Add the parameter name directly
        
        # Create the SUT function call string
        sut_call = f'{sut_name}({", ".join(param_strings)});'
        
        # Return the SUT function call string
        return sut_call

    def write_results_formatter(self, CType_parameters, formatter_spec):
        # Create the format string and the list of variables
        format_string = []
        variables_list = []
    
        for param in CType_parameters:
            if param.pointer_depth:  # Check if the parameter is a pointer (output)
                format_spec = formatter_spec.get(param.type)  # Get the format specifier for the parameter type
                if format_spec:
                    format_string.append(format_spec)  # Add the format specifier to the format string
                    variables_list.append(param.name)  # Add the parameter name to the variables list
    
        # Join the format specifiers and variable names with commas
        format_string = ",".join(format_string)
        variables_list = ",".join(variables_list)
    
        # Return the format string with a newline character and the variables list
        return format_string + "\\n", variables_list

    def test_driver_generator(
            self,
            input_path,
            path_sut,
            result_file_path,
            original_file_path,
            CType_parameters,
            formatter_spec,
        ):

        # Path to the backup file
        backup_file = "./modules/test_driver/c_files/test_driver_model.c"

        # Copy the content of the backup file to the original file
        shutil.copyfile(backup_file, original_file_path)

        # Read the content of the original file
        with open(original_file_path, "r") as arquivo:
            conteudo = arquivo.read()

        # Replace specific values in the content
        conteudo = conteudo.replace(
            "// include SutFileName.h", f'#include "../../../{path_sut}"'
        )

        input_filename = "input_file"
        result_filename = "results_file"

        # Replace the dynamic paths for input.csv and output.csv files
        conteudo = conteudo.replace(
            "// inputFile_path", f'FILE *{input_filename} = fopen("{input_path}", "r");'
        )
        conteudo = conteudo.replace(
            "// resultFile_path",
            f'FILE *{result_filename} = fopen("{result_file_path}", "w");',
        )

        # Generate the variable declarations dynamically
        var_declaration = self.create_variables(CType_parameters)
        conteudo = conteudo.replace("// init_var", var_declaration)

        # Generate the header dynamically
        header = self.header_generator(CType_parameters)
        conteudo = conteudo.replace(
            "// HeaderPlaceholder",
            f'fprintf({result_filename}, "%s,%s\\n","Time","{header}");',
        )

        # Generate the token assignments dynamically
        code_lines = self.generate_formatting_code(CType_parameters)
        conteudo = conteudo.replace("// TokenAssignment", "\n".join(code_lines))

        # Generate the SUT function call dynamically
        sut_name = "sut"
        sut_call = self.sut_caller(CType_parameters, sut_name)
        conteudo = conteudo.replace("// sut()", f"{sut_call}")

        # Generate the format string and variable list for results
        format_string, variable_list = self.write_results_formatter(
            CType_parameters, formatter_spec
        )
        fprintf_line = f'if (fprintf({result_filename}, "%f,{format_string}", time_id,{variable_list}) < 0) {{'
        conteudo = conteudo.replace("// RESULTS.CSV", fprintf_line)

        # Write the updated content back to the original file
        with open(original_file_path, "w") as arquivo:
            arquivo.write(conteudo)

        return
