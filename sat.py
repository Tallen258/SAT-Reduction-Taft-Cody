
def sat(func: list):
    pass

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





f = ['a;b;c', '-a;b;-c', '-d;-b', '-a;c', '-b;a']