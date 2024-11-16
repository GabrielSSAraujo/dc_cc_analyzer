from pycparser import c_generator
from models.coupling_list import Coupling
from modules.code_instrumenter.function_inserter import FunctionCallInserter


class CodeInstrumenter:
    def __init__(self):
        self._ast = None
        self._coupled_data = None

    def _generate_c_code(self, my_ast):
        generator = c_generator.CGenerator()
        return generator.visit(my_ast)

    def instrument_code(
        self, ast, coupled_data: Coupling, main_func: str, type_list: dict
    ):
        self._ast = ast
        self._coupled_data = coupled_data
        self.type_list = type_list

        # Handle AST and insert data
        inserter = FunctionCallInserter(main_func)

        # stores the parameters name
        recorder_param = []

        # for each coupled function get which parameter is coupled and instrument the funtion
        for coupled_data in self._coupled_data:
            func_name = coupled_data.function_b
            for parameter in coupled_data.parameters:
                
                # fill parameters list
                recorder_param.append(parameter.name)

                # define the instrument function
                before_name = ""
                if not parameter.pointer_depth or parameter.pointer_depth=="&":
                    before_name = "&"
                inserter.set_data_to_insert(
                    func_name,
                    "recorder_record",
                    f'"{parameter.name}"',
                    before_name + parameter.name,
                    '"'+self.type_list[parameter.type]+'"',   
                )

                # define the parameter to be inserted into the code
                inserter.set_new_coupled_parameter_to_insert(parameter) #if the old_name is defined it means that this coupling has already been defined

                # visit ast and insert function
                inserter.visit(self._ast)
              
        # initializing coupling list in recorder module
        inserter.set_data_to_insert(
            main_func,
            "recorder_setCouplings",
            len(recorder_param),
            ", ".join(f'"{item}"' for item in recorder_param),
        )
        inserter.visit(self._ast)

        # compara codigo c com os includes pre-processados e retorna diferença
        code = self._generate_c_code(self._ast)
        return code
