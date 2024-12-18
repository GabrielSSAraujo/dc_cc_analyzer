from pycparser import c_ast
from .ast_node_structure import ASTNodeStructure

class FunctionCallInserter(c_ast.NodeVisitor):
    def __init__(self, main_func):
        self.main_func = main_func
        self.func_name = None
        self.args = None
        self.func_name_to_insert = None
        self.probles = None
        self.type = None

    def set_data_to_insert(
        self,
        func_name,
        func_name_to_insert,
        args=None,
        func_param=None,
        type=None,
        insert_after=False,
    ):
        self.insert_after = insert_after
        self.func_name = func_name
        self.args = args if args is not None else []
        self.func_name_to_insert = func_name_to_insert
        self.param = func_param
        self.type = type

    def set_new_probes_to_insert(self, coupled_param=None):
        self.probes = coupled_param

    def generic_visit(self, node):
        # parent nodes are kept and the child nodes are updated
        for child_name, child in node.children():
            self.visit(child)

    def visit_FuncDef(self, node):
        # if the first time, add includes
        if node.decl.name == self.main_func:
            self.visit(node.body)

    def visit_Compound(self, node):
        ast_node_structure = ASTNodeStructure()

        # Create a new function call to print coupled data
        function_call = ast_node_structure.get_func_call_structure(
            self.func_name_to_insert, self.args, self.param, self.type
        )

        # if the function to be inserted is the main function, insert in the index 0
        ind = 0 if (self.func_name == self.main_func) else -1

        # find the block index to insert function
        if hasattr(node.block_items, "insert"):
            for index, block in enumerate(node.block_items):
                if isinstance(block, c_ast.FuncCall):
                    if block.name.name == self.func_name:
                        ind = index
                elif hasattr(block, "rvalue"):
                    if not isinstance(block.rvalue, c_ast.Constant):
                        if block.rvalue.name.name == self.func_name:
                            ind = index
        else:
            print("[Code Instrumenter][Error]: The main function has no body")
            exit(1)
        if ind >= 0:

            if self.insert_after:
                node.block_items.insert(ind + 1, function_call)
            else:
                node.block_items.insert(ind, function_call)
