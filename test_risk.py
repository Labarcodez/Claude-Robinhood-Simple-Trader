from risk import evaluate_new_position

def test_valid():
    assert evaluate_new_position(1000,0,50,0,0,0,50).allowed

def test_order_size():
    assert not evaluate_new_position(1000,0,101,0,0,0,101).allowed

def test_kill():
    assert not evaluate_new_position(1000,0,50,0,0,0,50,True).allowed

def test_daily_loss():
    assert not evaluate_new_position(1000,0,50,0,-0.03,0,50).allowed

def test_symbol_cap():
    assert not evaluate_new_position(1000,0,50,0,0,0,101).allowed
