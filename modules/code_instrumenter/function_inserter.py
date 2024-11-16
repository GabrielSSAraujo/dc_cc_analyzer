from pycparser import c_ast
from .ast_node_structure import ASTNodeStructure


class FunctionCallInserter(c_ast.NodeVisitor):
    def __init__(self, main_func):
        self.main_func = main_func
        self.func_name = None
        self.args = None
        self.func_name_to_insert = None
        self.coupled_parameter = None
        self.type = None

    def set_data_to_insert(
        self, func_name, func_name_to_insert, args=None, func_param=None, type=None
    ):
        self.func_name = func_name
        self.args = args if args is not None else []
        self.func_name_to_insert = func_name_to_insert
        self.param = func_param
        self.type = type

    def set_new_coupled_parameter_to_insert(self, coupled_param=None):
        self.coupled_parameter = coupled_param

    def generic_visit(self, node):
        # parent nodes are kept and the child nodes are updated
        for child_name, child in node.children():
            self.visit(child)

    def visit_FuncDef(self, node):
        # if the first time, add includes
        if node.decl.name == self.main_func:
            # print(node)
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
                    if block.rvalue.name.name == self.func_name:
                        ind = index
        else:
            print("[Code Instrumenter][Error]: The main function has no body\n")
        if ind >= 0:
            # insert function
            # insert parameter definition and value if old_name defined(duplicated coupling)
            if (
                hasattr(self.coupled_parameter, "old_name")
                and self.coupled_parameter.old_name != None
            ):
                if self.coupled_parameter.pointer_depth == "*":
                    decl_param = (
                        ast_node_structure.get_delc_init_pointer_parameter_structure(
                            self.coupled_parameter
                        )
                    )
                else:
                    decl_param = ast_node_structure.get_decl_init_parameter_structure(
                        self.coupled_parameter
                    )

                node.block_items.insert(ind, decl_param)
                node.block_items.insert(ind + 1, function_call)
            else:
                node.block_items.insert(ind, function_call)
