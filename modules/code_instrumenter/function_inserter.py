from pycparser import c_ast


class FunctionCallInserter(c_ast.NodeVisitor):
    def __init__(self, main_func):
        self.main_func = main_func
        self.func_name = None
        self.args = None
        self.func_name_to_insert = None
        self.param = None
        self.type = None

    def set_data_to_insert(
        self, func_name, func_name_to_insert, args=None, param=None, type=None
    ):
        self.func_name = func_name
        self.args = args if args is not None else []
        self.func_name_to_insert = func_name_to_insert
        self.param = param
        self.type = type

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
        # Create a new function call to print coupled data
        arguments, params, type = None, None, None
        if self.args:
            arguments = c_ast.ID(name=f"{self.args}")
        if self.param:
            params = c_ast.ID(name=f"{self.param}")
        if self.type:
            type = c_ast.ID(name=f"{self.type}")

        aux_exprs = [arguments, params, type]
        exprs = [item for item in aux_exprs if item is not None]

        function_call = c_ast.FuncCall(
            name=c_ast.ID(name=f"{self.func_name_to_insert}"),
            args=c_ast.ExprList(exprs),
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
            node.block_items.insert(ind, function_call)
