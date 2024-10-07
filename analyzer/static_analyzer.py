from pycparser import c_ast, parse_file, c_generator
from models.function_structure import FuncStructure
from models.parameter import Parameter
from models.coupling_list import CouplingList


# Visit functions definitions
class FuncDefVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.functions_list = {}
        self.current_name = None

    # get from each function definition (Fucntion structure) // usar recursão aqui faria mais sentido .type.type.type //testado apenas para inteiro e ponteiro para interiro, presciso verificar tipos diversos
    def visit_FuncDef(self, node):
        current_function = FuncStructure(
            type=node.decl.type.type.type.names[0], name=node.decl.name
        )
        self.current_name = node.decl.name

        # for each parameter, check name, type and whether it is input or output
        for param in node.decl.type.args.params:
            temp_parameter = Parameter()
            params_type = param.type.type

            if isinstance(params_type, c_ast.IdentifierType):
                # inputs
                temp_parameter.type = params_type.names[0]
                temp_parameter.is_input = True

            elif isinstance(params_type, c_ast.TypeDecl):
                # outputs
                temp_parameter.type = params_type.type.names[0]
                temp_parameter.is_input = False

            temp_parameter.name = param.name
            current_function.parameters.append(temp_parameter)

        self.functions_list[current_function.name] = current_function

        # visit the body of each definition to identify calls to others fucntions
        self.visit(node.body)

    def visit_FuncCall(self, node):
        name = node.name.name
        self.functions_list[self.current_name].calls.append(name)


# Analyze data coupling between functions
class FunctionAnalyzer:
    def __init__(self, functions):
        self.functions = functions

    def _identify_coupled_parameters(self, func_a_parameters, func_b_parameters):
        coupling_data = []
        output_params_func_a = [
            param for param in func_a_parameters if not param.is_input
        ]
        # Verificar se os parâmetros de entrada da segunda função estão nos parâmetros de saída da primeira
        coupling_data = [
            param
            for param in func_b_parameters
            if param.is_input and param in output_params_func_a
        ]
        return coupling_data

    def _analyze_parameter_coupling(
        self, main_function
    ):  # Vou fazer isso aqui apenas para esse problema (sem recursão) prescisa generalizar
        coupling_list = []
        call_list = self.functions[main_function].calls
        for i in range(0, len(call_list)):
            for j in range(i + 1, len(call_list)):
                coupling_data = CouplingList()
                # find_parameter_coupling
                func_a_parameters = self.functions[call_list[i]].parameters
                func_b_parameters = self.functions[call_list[j]].parameters

                coupling_data.coupled_parameters = self._identify_coupled_parameters(
                    func_a_parameters, func_b_parameters
                )

                if len(coupling_data.coupled_parameters) > 0:

                    funca = self.functions[call_list[i]].name
                    funcb = self.functions[call_list[j]].name

                    coupling_data.function_a = funca
                    coupling_data.function_b = funcb
                    coupling_list.append(coupling_data)
                    # ver melhor forma de retonar (acho que dicionario)

        return coupling_list

    # If there is a function that does not call and has not been called, it is not used
    def find_unused_functions(self):
        print("implement")


# interface de chamadas de funções para analise
class StaticAnalyzer:
    # def __init__(self):
    #     self._ast.show()

    def get_ast(self, file_path):
        return self._generate_ast(file_path)

    def _generate_ast(self, file_path):
        return parse_file(
            file_path,
            use_cpp=True,
            cpp_path="gcc",
            cpp_args=["-E", "-Iutils/fake_libc_include"],
        )

    def _extract_function_definitions(self, ast):
        definitions = FuncDefVisitor()
        definitions.visit(ast)

        return definitions.functions_list

    def generate_c_code_from_ast(self, ast):
        generator = c_generator.CGenerator()
        return generator.visit(ast)

    def get_coupled_data(self, ast):

        functions = self._extract_function_definitions(ast)  # _info?
        function_analyzer = FunctionAnalyzer(functions)

        # # show function definitions:
        # for func in functions.values():
        #     print(func.generate_func_signature())

        coupled_data = function_analyzer._analyze_parameter_coupling("SUT")
        return coupled_data
