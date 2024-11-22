from pycparser import c_ast, parse_file, c_generator
from models.function_structure import FuncStructure
from models.parameter import Parameter
from models.coupling_state import CouplingState, StateOnDest
from models.coupling_list import Coupling
from models.function_body import Body
import pycparser_fake_libc


class VariableDeclarationVisitor(c_ast.NodeVisitor):
    def __init__(self, function_name):
        self.function_name = function_name
        self.variable_declarations = []

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
    def __init__(self, functions):
        self.functions = functions
        self.written_coupling = []

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

    def _analyze_parameter_coupling(self, main_function, variable_decl):
        outputs_couplings = {}
        call_list = self.functions[main_function].body.calls
        for i in range(0, len(call_list)):
            func_a = self.functions[call_list[i]]
            output_params_func_a = self.get_function_outputs(func_a)

            for a_param in output_params_func_a:
                coupling_list = []

                if a_param.name in outputs_couplings.keys():
                    continue

                for j in range(i + 1, len(call_list)):
                    func_b = self.functions[call_list[j]]
                    func_b_parameters = func_b.parameters

                    for b_param in func_b_parameters:
                        if a_param == b_param:
                            coupling_state = CouplingState()
                            coupling_state.origin = func_a.name
                            coupling_state.destination = func_b.name
                            if func_a.body.assigned_to.name == a_param.name:
                                coupling_state.parameter = func_a.body.assigned_to
                            else:
                                coupling_state.parameter = b_param

                            if b_param.pointer_depth:
                                coupling_state.state_on_dest = StateOnDest.M
                            else:
                                coupling_state.state_on_dest = StateOnDest.R

                            coupling_list.append(coupling_state)

                outputs_couplings[a_param.name] = coupling_list

        coupling_data = []
        for output_name in outputs_couplings:
            last_state = StateOnDest.R
            i = 0
            parameter = Parameter()
            parameter.name = output_name

            for state in outputs_couplings[output_name]:
                if last_state == StateOnDest.M:
                    i += 1
                    name = parameter.name
                    parameter = Parameter()
                    parameter.name = name + "_aux" * i
                    parameter.old_name = name

                for var_decl in variable_decl:
                    if parameter.name.replace("_aux", "") == var_decl.name:
                        parameter.type = var_decl.type
                        parameter.pointer_depth = var_decl.pointer_depth
                for var_decl in self.functions[main_function].parameters:
                    if parameter.name.replace("_aux", "") == var_decl.name:
                        parameter.type = var_decl.type
                        parameter.pointer_depth = var_decl.pointer_depth

                cd = Coupling()
                cd.function_a = state.origin
                cd.function_b = state.destination
                cd.parameters.append(parameter)

                if cd not in coupling_data:
                    coupling_data.append(cd)
                else:
                    coupling_data[coupling_data.index(cd)].parameters.extend(
                        cd.parameters
                    )
                last_state = state.state_on_dest

        return coupling_data

    # If there is a function that does not call and has not been called, it is not used
    def find_unused_functions(self):
        print("implement")


# interface de chamadas de funções para analise
class StaticAnalyzer:
    def __init__(self):
        self.functions_metadata = None
        self.variables_def = []

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
        self.variables_def = VariableDeclarationVisitor("sut")
        self.variables_def.visit(ast)

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
        coupled_data = function_analyzer._analyze_parameter_coupling(
            "sut", self.variables_def.variable_declarations
        )
        return coupled_data
