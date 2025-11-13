from pulp import LpVariable, LpProblem, LpMaximize, value, LpBinary

def verify_sat(func: list, solution: dict):
    if solution is None: 
        return False
    
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
        node: LpVariable(node, 0, 1, cat=LpBinary)
        for node in inputs
    }
    notNodeToVariable = {
        node: LpVariable("not" + node, 0, 1, cat=LpBinary)
        for node in inputs
    }

    for i in inputs:
        problem += nodeToVariable[i] + notNodeToVariable[i] == 1


    def is_not_gate(input):
        return len(input) == 2
    
    gates = []
    for gate in func:
        or_gate = LpVariable(gate.replace(';', ',').replace('-', 'not'), 0, 1, cat=LpBinary)
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

    f_variable = LpVariable("func", 0, 1, cat=LpBinary)

    for gate in gates:
        problem += f_variable <= gate
    problem += f_variable >= sum(gates) - (len(gates) - 1)

    problem += f_variable

    problem.solve()
    if value(f_variable) == 0:
        return None

    return {
        i: value(nodeToVariable[i])
        for i in inputs
    }

# current knowledge: 
# We know the objective function is being set to maximize our output variable
# EVERYTHING is being typed as 'Integer'
# Bounds are set by default between 0 and 1
# Intermediate steps are returning 0.5

# Console log below: 
# Result - Linear relaxation infeasible

# No feasible solution found
# (this is for the circuit ['a;b', '-a;b', 'a;-b'], which has an obvious solution)


f = ['a;b;c', '-a;b;-c', '-d;-b', '-a;c', '-b;a']
# f = ['a;b', '-a;b', 'a;-b', '-a;-b']

print(sat(f))