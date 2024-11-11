from pycparser import c_ast, c_generator
from models.coupling_list import Coupling


class CodeInstrumenter:
    def __init__(self):
        self._ast = None
        self._coupled_data = None

    def _generate_c_code(self, my_ast):
        generator = c_generator.CGenerator()
        return generator.visit(my_ast)

    def instrument_code(self, ast, coupled_data: Coupling):
        self._ast = ast
        self._coupled_data = coupled_data
        # Handle AST and insert data
        inserter = FunctionCallInserter()

        # for each coupled function get which parameter is coupled and instrument the funtion
        for coupled_data in self._coupled_data:
            func_name = coupled_data.function_b
            for parameter in coupled_data.coupled_parameters:
                # define the instrument function
                inserter.set_data_to_insert(
                    func_name,
                    "printf",
                    f"o valor de {parameter.name}: %d \\n",
                    parameter.name,
                )
                # visit ast and insert function
                inserter.visit(self._ast)

        # compara codigo c com os includes pre-processados e retorna diferença
        code = self._generate_c_code(self._ast)
        return code


class FunctionCallInserter(c_ast.NodeVisitor):
    def __init__(self):
        self.func_name = None
        self.args = None
        self.func_name_to_insert = None
        self.param = None

    def set_data_to_insert(self, func_name, func_name_to_insert, args=None, param=None):
        self.func_name = func_name
        self.args = args if args is not None else []
        self.func_name_to_insert = func_name_to_insert
        self.param = param

    def generic_visit(self, node):
        # parent nodes are kept and the child nodes are updated
        for child_name, child in node.children():
            self.visit(child)

    def visit_FuncDef(self, node):
        # if the first time, add includes
        if node.decl.name == self.func_name:
            self.visit(node.body)

    def visit_Compound(self, node):

        # Create a new function call to print coupled data
        function_call = c_ast.FuncCall(
            name=c_ast.ID(name=f"{self.func_name_to_insert}"),
            args=c_ast.ExprList(
                exprs=[
                    c_ast.Constant(type="string", value=f'"{self.args}"'),
                    c_ast.ID(name=f"{self.param}"),
                ]
            ),
        )
        node.block_items.insert(0, function_call)
