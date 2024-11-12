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
    def __init__(self):
        self.type_list = None

    def get_types_from_ast(self, ast):
        types = TypeDefVisitor()
        types.visit(ast)
        self.type_list = types.type_list
        return self.type_list

    def get_format_from_type(self, type):
        type_to_format = {
            "int": "%d",
            "char": "%c",
            "float": "%f",
            "double": "%lf",
            "long": "%ld",
            "short": "%hd",
            "unsigned int": "%u",
            "unsigned char": "%c",
            "unsigned long": "%lu",
            "unsigned short": "%hu",
            "long long": "%lld",
            "long double": "%Lf",
            "size_t": "%zu",  # print as unsigned decimal
            "int8_t": "%d",
            "int16_t": "%d",
            "int32_t": "%d",
            "int64_t": "%d",
            "uint8_t": "%d",
            "uint16_t": "%d",
            "uint32_t": "%d",
            "uint64_t": "%d",
        }
        if type not in self.type_list:
            return "ERRO"
        tydef_to_type = self.type_list[type]
        return type_to_format[tydef_to_type]
