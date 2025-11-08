from pulp import LpVariable, LpProblem, LpMaximize
# input: directed graph (nodes are labeled with gate type--and, or, not, input)
def CircuitSimulat(graph, target, inputs):
    #inputs is a dictionary from node to value
    reversed_graph = graph.reversed()
    problem = LpProblem("circuit_simulation", LpMaximize)
    nodeToVariable ={
        str(node): LpVariable(str(node), 0, 1)
        for node in graph.nodes()
    }
    def output(node):
        return nodeToVariable[str(node)]
    def first_input(node):
        return nodeToVariable[str(reversed_graph.first_child(node))]
    def second_input(node):
        return nodeToVariable[str(reversed_graph.second_child(node))]
    
    for node in graph.nodes():
        if node in inputs and type(inputs) == dict:
            problem += nodeToVariable[node] == inputs[node]
        if node.getType()== 'not':
            problem += output(node)==1 - first_input (node)
        if output.getType() == 'or':
            problem += output(node) >= first_input(node)
            problem += output(node) >= second_input(node)
            problem += output(node) <= first_input(node) + second_input (node)
        if output.getType() == 'and':
            problem += output(node) <= first_input(node)
            problem += output(node) <= second_input(node)
            problem += output (node) >= first_input (node) + second_input (node) - 1
        problem += nodeToVariable[target]
        problem.solve()
        return nodeToVariable[target].value, {input: nodeToVariable[(str(input))].value for input in inputs}