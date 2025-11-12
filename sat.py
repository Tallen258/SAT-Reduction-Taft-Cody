from pulp import LpVariable, LpProblem, LpMaximize, LpBinary

def verify_sat(func: list, solution: dict):
    for or_gate in func:
        inputs = or_gate.split(";")
        works = False
        for i in inputs:
            if len(i) == 2:
                if solution[i[1]] == False:
                    works = True
            else:
                if solution[i] == True:
                    works = True
        if not works:
            return False
    return True

def sat(func: list):
    problem = LpProblem("circuit_thing", LpMaximize)
    inputs = set()
    for or_gate in func:
        chars = or_gate.split(';')
        for c in chars:
            inputs.add(c[-1])

    nodeToVariable = {
        node: LpVariable(node, 0, 1)
        for node in inputs
    }
    notNodeToVariable = {
        node: LpVariable("not" + node, 0, 1)
        for node in inputs
    }
    def is_not_gate(input):
        return len(input) == 2
    
    gates = []
    for gate in func:
        or_gate = LpVariable(gate, 0, 1)
        gates.append(or_gate)
        current_inputs = gate.split(';')
        current_variables = []
        for input in current_inputs:
            if is_not_gate(input):
                current_variables.append(notNodeToVariable[input[-1]])
            else:
                current_variables.append(nodeToVariable[input])

        for variable in current_variables:
            problem += or_gate >= variable
        problem += or_gate <= sum(current_variables)

    f_variable = LpVariable("func", 0, 1)

    for gate in gates:
        problem += f_variable <= gate
    problem += f_variable >= sum(gates) - 1

    problem.solve()
    # See if the problem found a solution
    # If true, return that as a dictionary type
    # If not, return none

    # (the code below does not work)
    for i in inputs:
        print(nodeToVariable[i].value)




f = ['a;b;c', '-a;b;-c', '-d;-b', '-a;c', '-b;a']

print(sat(f))