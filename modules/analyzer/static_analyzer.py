from pycparser import c_ast, parse_file, c_generator
from models.function_structure import FuncStructure
from models.parameter import Parameter
from models.coupling_state import CouplingState, StateOnDest
from models.coupling_list import Coupling
from models.function_body import Body
from models.function_interface import FunctionInterface
import pycparser_fake_libc


class VariableAssignmentVisitor(c_ast.NodeVisitor):
    def __init__(self, func_name):
        self.initialized = []
        self.function_name = func_name

    def visit_FuncDef(self, node):
        if node.decl.name == self.function_name:
            # Traverse the function body
            self.visit(node.body)

    def visit_Assignment(self, node):
        if isinstance(node.rvalue, c_ast.Constant):
            if hasattr(node.rvalue, "value"):
                if node.rvalue.value:
                    if isinstance(node.lvalue, c_ast.UnaryOp):
                        self.initialized.append(node.lvalue.expr.name)
                    if isinstance(node.lvalue, c_ast.ID):
                        self.initialized.append(node.lvalue.name)


class VariableDeclarationVisitor(c_ast.NodeVisitor):
    def __init__(self, function_name):
        self.function_name = function_name
        self.variable_declarations = []
        self.initialized = []

    def visit_FuncDef(self, node):
        if node.decl.name == self.function_name:
            # Traverse the function body
            self.visit(node.body)

    def visit_Decl(self, node):
        parameter = Parameter()

        if isinstance(node.type, c_ast.TypeDecl):
            parameter.name = node.name
            parameter.type = " ".join(node.type.type.names)
            parameter.pointer_depth = ""
        if isinstance(node.type, c_ast.PtrDecl):
            parameter.name = node.name
            parameter.type = " ".join(node.type.type.type.names)
            parameter.pointer_depth = "*"
        if parameter.name:
            self.variable_declarations.append(parameter)

        if hasattr(node, "init"):
            if node.init:
                self.initialized.append(parameter.name)


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
                    temp_parameter.pointer_depth = ""
                elif isinstance(params_type, c_ast.PtrDecl):
                    # output - tratar esse caso quando acoplado
                    temp_parameter.type = " ".join(params_type.type.type.names)
                    temp_parameter.pointer_depth = "**"
                elif isinstance(params_type, c_ast.TypeDecl):
                    # outputs
                    temp_parameter.type = " ".join(params_type.type.names)
                    temp_parameter.pointer_depth = "*"

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
            current_function.body.assigned_to = func_ret

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
                    if arg.op == "&":
                        params[index].pointer_depth = "&"
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
        pd_asgn = ""
        if isinstance(node.lvalue, c_ast.ID):
            name = node.lvalue.name
        elif isinstance(node.lvalue, c_ast.UnaryOp):
            if isinstance(node.lvalue.expr, c_ast.ID):
                name = node.lvalue.expr.name
                pd_asgn = "*"
        if isinstance(node.rvalue, c_ast.FuncCall):
            self.functions_list[node.rvalue.name.name].body.function_return.name = name
            self.functions_list[node.rvalue.name.name].body.assigned_to.name = name
            self.functions_list[
                node.rvalue.name.name
            ].body.assigned_to.pointer_depth = pd_asgn


# Analyze data coupling between functions
class FunctionAnalyzer:
    def __init__(self, functions, initialized_param_list):
        self.functions = functions
        self.written_coupling = []
        self.record_name = {}
        self.initialized_param_list = initialized_param_list

    def remove_aux_suffix(self, value):
        # Check if string ends with 'aux' and remove
        while value.endswith("_aux"):
            value = value[:-4] if value.endswith("_aux") else value
        return value

    def get_function_outputs(self, function_metadata):
        function_parameters = function_metadata.parameters
        function_return = function_metadata.body.assigned_to

        output = [param for param in function_parameters if param.pointer_depth]
        if function_return.name:
            output.append(function_return)
        return output

    def _analyze_parameter_coupling(self, main_function):
        # se o parametro nao estiver na lista ela é so saida
        function_interface_list = []
        call_list = self.functions[main_function].body.calls

        for i in range(0, len(call_list)):
            func = self.functions[call_list[i]]
            function_interface = FunctionInterface()
            function_interface.function_name = func.name
            ret = func.body.function_return

            if ret.name:
                if ret.name not in self.record_name:
                    self.record_name[ret.name] = 0
                else:
                    self.record_name[ret.name] += 1

                if self.record_name[ret.name] != 0:
                    ret.current_name = ret.name + "_" + str(self.record_name[ret.name])
                else:
                    ret.current_name = ret.name

                self.initialized_param_list.append(ret.name)
                function_interface.output_parameters.append(ret)

            for parameter in func.parameters:
                if parameter.name not in self.record_name:
                    self.record_name[parameter.name] = 0

                parameter_copy = parameter.clone()
                if self.record_name[parameter.name] != 0:
                    parameter.current_name = (
                        parameter.name + "_" + str(self.record_name[parameter.name])
                    )
                else:
                    parameter.current_name = parameter.name

                if not parameter.pointer_depth:
                    function_interface.input_parameters.append(parameter)
                else:
                    if parameter.name in self.initialized_param_list:
                        function_interface.input_parameters.append(parameter)
                    self.initialized_param_list.append(parameter.name)

                    self.record_name[parameter_copy.name] += 1

                    parameter_copy.current_name = (
                        parameter_copy.name
                        + "_"
                        + str(self.record_name[parameter_copy.name])
                    )
                    function_interface.output_parameters.append(parameter_copy)

            function_interface_list.append(function_interface)

        return function_interface_list

    # If there is a function that does not call and has not been called, it is not used
    def find_unused_functions(self):
        print("implement")


# interface de chamadas de funções para analise
class StaticAnalyzer:
    def __init__(self):
        self.functions_metadata = None
        self.initialized = []

    def get_ast(self, file_path):
        return self._generate_ast(file_path)

    def _generate_ast(self, file_path):
        fake_libc_arg = "-I" + pycparser_fake_libc.directory
        return parse_file(file_path, use_cpp=True, cpp_args=["-E", fake_libc_arg])

    def get_func_metadata(self, functions_name=None):
        if not functions_name:
            return self.functions_metadata
        else:
            return self.functions_metadata[functions_name]

    def _extract_function_definitions(self, ast):
        # get definitions and parameters
        variables_def = VariableDeclarationVisitor("sut")
        variables_def.visit(ast)

        self.initialized = variables_def.initialized

        var_attr = VariableAssignmentVisitor("sut")
        var_attr.visit(ast)

        self.initialized.extend(var_attr.initialized)

        self.initialized = list(set(self.initialized))

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

        function_analyzer = FunctionAnalyzer(self.functions_metadata, self.initialized)
        coupled_data = function_analyzer._analyze_parameter_coupling("sut")
        return coupled_data
