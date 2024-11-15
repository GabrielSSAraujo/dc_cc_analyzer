from pycparser import c_ast
from models.parameter import Parameter

class ASTNodeStructure:
    def get_delc_init_pointer_parameter_structure(self, parameter: Parameter):
        return c_ast.Decl(
            name=str(parameter.name),
            type= c_ast.PtrDecl(
                quals=[],
                type=c_ast.TypeDecl(
                    declname=str(parameter.name),
                    quals=[],
                    align=None,
                    type=c_ast.IdentifierType(names=[str(parameter.type)]),
                ),
            ),
            init=c_ast.ID(str(parameter.old_name)),
            quals=[],
            storage=[],
            funcspec=[],
            align=[],
            bitsize=None,
        )
    
    def get_decl_init_parameter_structure(self, parameter: Parameter):
        return c_ast.Decl(
            name=str(parameter.name),
            type=c_ast.TypeDecl(
                declname=str(parameter.name),
                quals=[],
                align=None,
                type=c_ast.IdentifierType(names=[str(parameter.type)]),
            ),
            init=c_ast.ID(str(parameter.old_name)),
            quals=[],
            storage=[],
            funcspec=[],
            align=[],
            bitsize=None,
        )

    def get_func_call_structure(self, func_name, args, param, type):
        arguments, params, n_type = None, None, None
        if args:
            arguments = c_ast.ID(name=f"{args}")
        if param:
            params = c_ast.ID(name=f"{param}")
        if type:
            n_type = c_ast.ID(name=f"{type}")

        aux_exprs = [arguments, params, n_type]
        exprs = [item for item in aux_exprs if item is not None]

        return c_ast.FuncCall(
            name=c_ast.ID(name=f"{func_name}"),
            args=c_ast.ExprList(exprs),
        )