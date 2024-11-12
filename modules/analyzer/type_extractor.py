from pycparser import c_ast


class TypeDefVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.type_list = {}

    def visit_Typedef(self, node):
        node_type = node
        while hasattr(node_type, "type"):
            node_type = node_type.type
        self.type_list[node.name] = " ".join(node_type.names)


class TypeExtractor:
    def __init__(self, ast):
        self.ast = ast

    def get_types_from_ast(self):
        types = TypeDefVisitor()
        types.visit(self.ast)
        return types.type_list

    # def get_format_from_type:
