import re

def instrument_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    # encontra as funções
    expression = r'([\w*]+ [\w*]+\(.*\))\s*\n*\s*\{'
    matches = re.finditer(expression, code)

    # para cada função adiciona um printf no inicio e um no final
    instrumented_code = code
    for match in matches:
        function_name =  match.group(1)
        print(function_name)
        init_code = f'\nprintf("init of function {function_name}");\n'
        end_code = f'printf("end of {function_name}");\n'
        
        # Adicionar informações no inicio e final do arquivo
        instrumented_code = re.sub(
            rf'({match.group(1)}+\(.*\)\s*\n*\s*\{{)',
            rf'\1{init_code}',
            instrumented_code
        )
    print(instrumented_code)

if __name__ == "__main__":
    file_path = 'teste.c'
    instrument_code(file_path)