import networkx as nx
import matplotlib.pyplot as plt


class DataCouplingFlow:
    def __init__(self, couplings, functions, comp_name="sut"):
        self.couplings = couplings
        self.functions = functions
        self.comp_name = comp_name
        self.calls = None
        self.coupling_output_mapping = {}
        self.graph = nx.DiGraph()

    def remove_aux_suffix(self, value):
        # Check if string ends with 'aux' and remove
        while value.endswith("_aux"):
            value = value[:-4] if value.endswith("_aux") else value
        return value

    # Performs a recursive analysis starting from the output to identify which couplings influence its result.
    def find_coupling_to_output(self, output, comp_name):  # b, f4
        # find index of current function
        if comp_name in self.calls:
            start_index = self.calls.index(comp_name) - 1
        else:
            start_index = len(self.calls) - 1

        for call in self.calls[start_index::-1]:  # start for the end
            if output == self.functions[call].body.function_return:
                for coup in self.couplings:
                    if coup.function_b == call:
                        for param in coup.parameters:
                            self.graph.add_edge(param.name, output.name)
                            self.find_coupling_to_output(param, call)
                break
            for param in self.functions[call].parameters:
                if self.remove_aux_suffix(param.name) == output.name:
                    for coup in self.couplings:
                        if coup.function_b == call:
                            for param in coup.parameters:
                                self.graph.add_edge(param.name, output.name)
                                self.find_coupling_to_output(param, call)
                    break

    def analyze_data_flow(self):
        # get outputs from main function
        outputs = [
            out
            for out in self.functions[self.comp_name].parameters
            if out.pointer_depth
        ]
        outputs_name = [out.name for out in outputs]

        # get ordered function calls
        self.calls = self.functions[self.comp_name].body.calls

        # get the coupled parameters name
        cp_names = []
        for coup in self.couplings:
            for param in coup.parameters:
                cp_names.append(param.name)

        # create graph with couplings and outputs
        self.graph.add_nodes_from(outputs_name)
        self.graph.add_nodes_from(cp_names)

        # find couplings that affect each output
        for out in outputs:
            self.find_coupling_to_output(out, self.comp_name)
            # generate dictionary with couplings that affect each output
            outs = []
            for coup in self.couplings:
                for param in coup.parameters:
                    if nx.has_path(self.graph, param.name, out.name):
                        outs.append(param.name)
            self.coupling_output_mapping[out.name] = outs

    def get_coupling_to_output_mapping(self):
        return self.coupling_output_mapping

    def save_graph(self, path):
        # Draw graph
        plt.figure(figsize=(18, 12))
        pos = nx.spring_layout(self.graph)  # Define a posição dos nós

        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            node_size=3000,
            node_color="skyblue",
            font_size=20,
            font_weight="bold",
            edge_color="gray",
            arrows=True,
        )

        # Save png image
        plt.savefig(path + "dc_graph.png", format="png", dpi=300)
