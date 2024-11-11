from pycparser import c_ast, parse_file, c_generator
from models.function_structure import FuncStructure
from models.parameter import Parameter
from models.coupling_list import Coupling
from models.function_body import Body


class FuncDeclVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.functions_list = {}
        self.current_name = None

    def get_function_parameters(self, node_args):
        parameter_list = []
        if hasattr(node_args, "params"):
            for param in node_args.params:
                temp_parameter = Parameter()
                params_type = param.type.type

                if isinstance(params_type, c_ast.IdentifierType):
                    # inputs
                    temp_parameter.type = " ".join(params_type.names)
                    temp_parameter.pointer_depth = "*"
                elif isinstance(params_type, c_ast.PtrDecl):
                    # output - tratar esse caso quando acoplado
                    temp_parameter.type = " ".join(params_type.type.type.names)
                    temp_parameter.pointer_depth = "**"
                elif isinstance(params_type, c_ast.TypeDecl):
                    # outputs
                    temp_parameter.type = " ".join(params_type.type.names)
                    temp_parameter.pointer_depth = ""

                temp_parameter.name = param.name
                parameter_list.append(temp_parameter)
        # else: empty function
        return parameter_list

    def visit_FuncDecl(self, node):
        pointer, node_type = "", ""

        # find function info path
        if isinstance(node.type, c_ast.PtrDecl):
            if isinstance(node.type.type, c_ast.PtrDecl):
                node_type = node.type.type.type
                pointer = "**"
            else:
                node_type = node.type.type
                pointer = "*"
        else:
            node_type = node.type

        # save the current funtion
        self.current_name = node_type.declname
        if self.current_name not in self.functions_list:
            current_function = FuncStructure(
                type=" ".join(node_type.type.names),
                name=self.current_name,
                pointer_depth=pointer,
            )
            # get parameter from node.args
            current_function.parameters = self.get_function_parameters(node.args)

            # create body function
            func_ret = Parameter()
            func_ret.pointer_depth = pointer
            func_ret.type = current_function.type
            current_function.body = Body()
            current_function.body.function_return = func_ret

            # append element to function list
            self.functions_list[self.current_name] = current_function

            self.visit(node)

    def visit_FuncCall(self, node):
        # Align function parameter names with caller function for clarity
        name = node.name.name
        self.functions_list[self.current_name].body.calls.append(name)

        # parameters to be renamed
        params = self.functions_list[name].parameters
        if hasattr(node.args, "exprs"):
            for index, arg in enumerate(node.args.exprs):

                if isinstance(arg, c_ast.ID):
                    params[index].name = arg.name

                elif isinstance(arg, c_ast.UnaryOp):
                    if isinstance(arg.expr, c_ast.ID):
                        params[index].name = arg.expr.name


# Visit functions definitions
class FuncDefVisitor(c_ast.NodeVisitor):
    def __init__(self, functions):
        self.functions_list = functions
        self.current_name = None
        self.function_return = None

    def visit_FuncDef(self, node):
        self.visit(node.body)

    def visit_Assignment(self, node):
        name = ""
        if isinstance(node.lvalue, c_ast.ID):
            name = node.lvalue.name
        elif isinstance(node.lvalue, c_ast.UnaryOp):
            if isinstance(node.lvalue.expr, c_ast.ID):
                name = node.lvalue.expr.name
        if isinstance(node.rvalue, c_ast.FuncCall):
            self.functions_list[node.rvalue.name.name].body.function_return.name = name


# Analyze data coupling between functions
class FunctionAnalyzer:
    def __init__(self, functions):
        self.functions = functions

    def _identify_coupled_parameters(
        self, func_a_parameters, func_b_parameters, function_a_return
    ):
        coord_a = []
        coord_b = []
        parameters = []
        output_params_func_a = [
            (i, param)
            for i, param in enumerate(func_a_parameters)
            if not param.pointer_depth
        ]

        for index, param in enumerate(func_b_parameters):
            if param.pointer_depth == "*":
                # check coupling between function return and parameters
                if function_a_return == param:
                    coord_a.append(-1)
                    coord_b.append(index)
                    parameters.append(param)

                # check coupling between parameters
                for a_param in output_params_func_a:
                    if param == a_param[1]:
                        coord_b.append(index)
                        coord_a.append(a_param[0])
                        parameters.append(param)
        return coord_a, coord_b, parameters

    def _analyze_parameter_coupling(self, main_function):
        coupling_list = []
        call_list = self.functions[main_function].body.calls
        for i in range(0, len(call_list)):
            for j in range(i + 1, len(call_list)):
                coupling_data = Coupling()
                # find_parameter_coupling
                func_a_parameters = self.functions[call_list[i]].parameters
                function_a_return = self.functions[call_list[i]].body.function_return
                func_b_parameters = self.functions[call_list[j]].parameters
                (
                    coupling_data.coord_a,
                    coupling_data.coord_b,
                    coupling_data.parameters,
                ) = self._identify_coupled_parameters(
                    func_a_parameters, func_b_parameters, function_a_return
                )
                if len(coupling_data.coord_a) > 0 and len(coupling_data.coord_b) > 0:

                    funca = self.functions[call_list[i]].name
                    funcb = self.functions[call_list[j]].name

                    coupling_data.function_a = funca
                    coupling_data.function_b = funcb

                    coupling_list.append(coupling_data)

        return coupling_list

    # If there is a function that does not call and has not been called, it is not used
    def find_unused_functions(self):
        print("implement")


# interface de chamadas de funções para analise
class StaticAnalyzer:
    def __init__(self):
        self.functions_metadata = None

    def get_ast(self, file_path):
        return self._generate_ast(file_path)

    def _generate_ast(self, file_path):
        return parse_file(
            file_path,
            use_cpp=True,
            cpp_path="gcc",
            cpp_args=["-E", "-I ../utils/fake_libc_include"],
        )

    def get_func_metadata(self, functions_name=None):
        if not functions_name:
            return self.functions_metadata
        else:
            return self.functions_metadata[functions_name]

    def _extract_function_definitions(self, ast):
        # get definitions and parameters
        definitions = FuncDeclVisitor()
        definitions.visit(ast)

        # get return and rename the parameters to allow analyzis
        aux_def = FuncDefVisitor(definitions.functions_list)
        aux_def.visit(ast)

        # print(definitions.functions_list)
        self.functions_metadata = (
            definitions.functions_list
        )  # remover o retorno e usar o metadata global

    def generate_c_code_from_ast(self, ast):
        generator = c_generator.CGenerator()
        return generator.visit(ast)

    def get_coupled_data(self, ast):
        self._extract_function_definitions(ast)

        function_analyzer = FunctionAnalyzer(self.functions_metadata)
        coupled_data = function_analyzer._analyze_parameter_coupling("SUT")

        return coupled_data
