#no caso do sut de teste ficaria -     main
#                                       |
#                                      SUT
#                              _________|__________
#                             |       |     |      |          |
#                           compa  compb  compc  compd      compE
# 
# Parse file and get the ast - DONE
# Extract the main signature - DONE - considerada sempre SUT(ou main add)
# Generate the graph with relationships ()
# Identify data coupling between components
# Instrument the code to alert when a coupling is ativated (mybe in other file)

from pycparser import c_ast, parse_file

# Visita funções e extrai dados referentes a sua definição no codigo
class FuncDefVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.functions_list = {}
        self.current_name = None
    # get the function definitions // usar recursão aqui faria mais sentido .type.type.type //testado apenas para inteiro e ponteiro para interiro, presciso verificar tipos diversos
    def visit_FuncDef(self, node):
        current_function = FuncStructure()
        self.current_name =  node.decl.name
        current_function.type = node.decl.type.type.type.names[0]
        current_function.name = node.decl.name

        for param in node.decl.type.args.params:
            temp_parameter = {"type": None, "is_input": None, "name": None}
            params_type = param.type.type

            if isinstance(params_type, c_ast.IdentifierType):
                #inputs
                temp_parameter['type'] = params_type.names[0]
                temp_parameter["is_input"] = True

            elif isinstance(params_type, c_ast.TypeDecl):
                # outputs
                temp_parameter['type'] = params_type.type.names[0]+'*'
                temp_parameter["is_input"] = False

            temp_parameter["name"] = param.name
            current_function.parameter.append(temp_parameter)
    
        self.functions_list[node.decl.name] = current_function
        self.visit(node.body)

    def visit_FuncCall(self, node):
        name = node.name.name
        self.functions_list[self.current_name].call.append(name)

# Estrutura de armazenamento de dados de uma função
class FuncStructure:
    def __init__(self):
        self.type = None
        self.name = None
        self.parameter = []
        self.call = []
        # self.body = None do tipo c_ast.Compound ??
        # self.ret = None
        # self.is_called = []
    
    def generate_func_signature(self):
        params = ''
        for i, param in enumerate(self.parameter):
            params = params + param['type'] +' '+ param['name']
            if(i < len(self.parameter)-1):
                params = params+', '
        signature = self.type +' '+ self.name +'('+ params +')'
        return signature

# realiza a analise de acoplamento entre funções
class FunctionAnalyzer:
    def __init__(self, functions):
        self.functions = functions
    
    def _identify_coupled_parameters(self, func_a_parameters, func_b_parameters):

        output_params_func_a = {
            param['name']: param for param in func_a_parameters 
            if '*' in param['type'] and not param['is_input']
        }

        coupling_info = []

        # Verificar se os parâmetros de entrada da segunda função estão nos parâmetros de saída da primeira
        for param in func_b_parameters:
            if param['is_input'] and param['name'] in output_params_func_a:
                # Adiciona os detalhes do acoplamento encontrado
                coupling_info.append(param['name'])

        return coupling_info


    def analyze_parameter_coupling(self, main_function): # Vou fazer isso aqui apenas para esse problema (sem recursão) prescisa generalizar
        call_list = self.functions[main_function].call

        for i in range(0,len(call_list)):
            for j in range(i+1, len(call_list)):
                #find_parameter_coupling
                func_a_parameters = self.functions[call_list[i]].parameter
                func_b_parameters = self.functions[call_list[j]].parameter
                
                coupling_data = self._identify_coupled_parameters(func_a_parameters, func_b_parameters)
                
                if(len(coupling_data) >0):
                    print(self.functions[call_list[i]].name,self.functions[call_list[j]].name) 
                    print(coupling_data)

                    # ver melhor forma de retonar (acho que dicionario)

        #return structure



    #If there is a function that does not call and has not been called, it is not used
    def find_unused_functions(self):
        print('implement')

# interface de chamadas de funções para analise
class StaticAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.ast = None
        self._generate_ast()
        # self.ast.show()

    def _generate_ast(self):
        self.ast = parse_file(self.file_path, use_cpp=True,
        cpp_path='gcc',
        cpp_args=['-E', '-Iutils/fake_libc_include'])
    
    def _extract_function_signatures(self):
        definitions = FuncDefVisitor()
        definitions.visit(self.ast)

        return definitions.functions_list
    
    def start_analysis(self):
        functions = self._extract_function_signatures() #_info?
        function_analyzer = FunctionAnalyzer(functions)

        #aqui estão os acoplamento que devem ser instrumentados no formato:
        # {'out':'compA', 'in':'compD', 'param_type': 'int' 'param_name':'AO1'}
        function_analyzer.analyze_parameter_coupling('SUT') 