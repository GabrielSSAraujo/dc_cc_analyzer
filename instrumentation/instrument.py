from pycparser import c_ast, c_parser, parse_file, c_generator
from models.coupling_list import CouplingList
from typing import List


class Instrumentator:
    def __init__(self, ast, coupled_data: CouplingList, path):
        self._ast = ast
        self._coupled_data = coupled_data
        self.path = path

    def generate_c_code(self, my_ast):
        generator = c_generator.CGenerator()
        return generator.visit(my_ast)

    def instrument_code(self):

        inserter = FunctionCallInserter()

        for coupled_data in self._coupled_data:
            # pegando apenas o primeiro, alterar
            param1 = coupled_data.coupled_parameters[0]
            function_c_n = coupled_data.function_b
            # create a visitor to choose the type before use
            inserter.set_data_to_insert(
                function_c_n, "printf", f"o valor de {param1.name}: %d", param1.name
            )
            inserter.visit(self._ast)

        with open("./SUT/sut_inst.c", "w") as file:
            file.write(self.generate_c_code(self._ast))


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
        for child_name, child in node.children():
            # Armazena o nó pai e o atributo que aponta para o filho
            self.attr = child_name
            self.visit(child)

    def visit_FuncDef(self, node):
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
