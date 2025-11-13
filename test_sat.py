from sat import verify_sat, sat

def test_two_gates_1():
    f = ['a', 'b']
    d = {'a': True, 'b': True}
    assert verify_sat(f, d) == True

def test_two_gates_2():
    f = ['a', '-b']
    d = {'a': True, 'b': False}
    assert verify_sat(f, d) == True
    d = {'a': True, 'b': True}
    assert verify_sat(f, d) == False

def test_two_gates_3():
    f = ['a;c', 'b;-d']
    d = {'a': True, 'b': True, 'c': True, 'd': True}
    assert verify_sat(f, d) == True
    d = {'a': False, 'b': True, 'c': True, 'd': False}
    assert verify_sat(f, d) == True
    d = {'a': False, 'b': True, 'c': False, 'd': True}
    assert verify_sat(f, d) == False
    d = {'a': True, 'b': False, 'c': True, 'd': True}
    assert verify_sat(f, d) == False

def test_sat_1():
    f = ['a;b', 'a;-b']
    assert verify_sat(f, sat(f)) == True

def test_sat_2():
    f = ['a;b', 'a;-b', '-a;b']
    assert verify_sat(f, sat(f)) == True

def test_sat_3():
    f = ['a;b;c', '-a;b;-c', '-d;-b', '-a;c', '-b;a']
    assert verify_sat(f, sat(f)) == True

def test_sat_4():
    f = ['a;b', '-a;b', 'a;-b', '-a;-b']
    assert verify_sat(f, sat(f)) == False

