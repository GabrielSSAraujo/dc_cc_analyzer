from pycparser import c_generator
from modules.code_instrumenter.function_inserter import FunctionCallInserter

# REQ-8 A Ferramenta deve criar um SUT Instrumentado (suti.c) a partir do SUT original, adicionando nele 
# chamadas de funções (probes) que registram os valores das entradas e saídas de cada função executada pelo SUT.
class CodeInstrumenter:
    def __init__(self, main_func="sut"):
        self._ast = None
        self._function_interface_list = None
        # Handle AST and insert data
        self.inserter = FunctionCallInserter(main_func)

    def _generate_c_code(self, my_ast):
        generator = c_generator.CGenerator()
        return generator.visit(my_ast)

    def insert_probes(self, parameters, func_name, insert_after=False):
        recorded_params = []
        for parameter in parameters:
            # fill parameters list
            recorded_params.append(parameter.current_name)

            # define the instrument function
            before_name = ""
            if not parameter.pointer_depth or parameter.pointer_depth == "&":
                before_name = "&"
            self.inserter.set_data_to_insert(
                func_name,
                "recorder_record",
                f'"{parameter.current_name}"',
                before_name + parameter.name,
                '"' + self.type_list[parameter.type] + '"',
                insert_after=insert_after,
            )
            self.inserter.visit(self._ast)
        return recorded_params

    def instrument_code(
        self, ast, function_interface_list, main_func: str, type_list: dict
    ):
        self._ast = ast
        self._function_interface_list = function_interface_list
        self.type_list = type_list

        # stores the parameters name
        recorder_param = []
        for function_interface in self._function_interface_list:

            func_name = function_interface.function_name
            recorder_param.extend(
                self.insert_probes(
                    function_interface.input_parameters,
                    func_name,
                    False,
                )
            )
            recorder_param.extend(
                self.insert_probes(
                    function_interface.output_parameters,
                    func_name,
                    True,
                )
            )

        recorder_param = list(set(recorder_param))
        
        # initializing coupling list in recorder
        self.inserter.set_data_to_insert(
            main_func,
            "recorder_setCouplings",
            len(recorder_param),
            ", ".join(f'"{item}"' for item in recorder_param),
        )
        self.inserter.visit(self._ast)

        # compares C code with preprocessed includes and returns difference
        code = self._generate_c_code(self._ast)
        return code
