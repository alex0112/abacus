import sys
import os
import pytest
from src.cpu import CPU
from src.memory import Memory
from src.io_device import IODevice
from src.opcodes import Opcode

# Ensure the src directory is in the Python path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture
def cpu():
    return CPU()

@pytest.fixture
def memory():
    return Memory()

@pytest.fixture
def io_device():
    return IODevice()


##################
# Instantiation: #
##################

def test_init_with_plus():
    pass

def test_init_with_minus():
    pass

def test_init_with_no_sign():
    pass

def test_init_with_too_long():
    pass

def test_init_with_too_short():
    pass

def test_init_with_non_num():
    pass

def test_init_with_empty():
    pass

def test_init_with_too_large():
    pass

def test_init_with_too_small():
    pass
   
#########
# Name: #
#########

def test_name():
    pass

def test_noop():
    pass

#########
# Sign: #
#########

def test_plus():
    pass

def test_minus():
    pass

############
# Operand: #
############

def test_operand():
    pass

##########################
# String Representation: #
##########################

def test_str_from_minus():
    op = Opcode("-1234")

    assert str(op) == "-1234"

def test_str_from_plus():
    pass

def test_str_from_no_sign():
    pass

#############
# Equality: #
#############

def test_basic_equality():
    op1 = Opcode("+0000")
    op2 = Opcode("+0000")

    assert op1 == op2

def test_basic_inequality():
    op1 = Opcode("+1000")
    op2 = Opcode("+0001")

    assert op1 != op2

#############
# Addition: #
#############

def test_basic_add():
    op1 = Opcode("+0000")
    op2 = Opcode("+1000")

    result = op1 + op2

    assert result == Opcode("+1000")

def test_add_negative_and_positive():
    op1 = Opcode("+0000")
    op2 = Opcode("-1000")

    result = op1 + op2

    assert result == Opcode("-1000")

def test_add_negative_and_negative():
    op1 = Opcode("-1000")
    op2 = Opcode("-1000")

    result = op1 + op2

    assert result == Opcode("-2000")


def test_overflow():
    op1 = Opcode("+9999")
    op2 = Opcode("+0001")

    result = op1 + op2

    ## TODO: Undefined behavior currently. Figure this out

## TODO: Write more tests here

################
# Subtraction: #
################

def test_basic_subtraction():
    op1 = Opcode("+0000")
    op2 = Opcode("+1000")

    result = op1 - op2

    assert result == Opcode("-1000")

def test_subtract_a_negative():
    op1 = Opcode("+0000")
    op2 = Opcode("-1000")

    result = op1 - op2

    assert result == Opcode("+1000")

def test_underflow():
    op1 = Opcode("-9999")
    op2 = Opcode("+0001")

    result = op1 - op2

    ## TODO: Undefined behavior currently. Figure this out

## TODO: Write more tests


###################
# Multiplication: #
###################

def test_mul():
    op1 = Opcode("+0000")
    op2 = Opcode("+0001")

    result = op1 * op2

    assert result == Opcode("+0000")

def test_mul_neg():
    op1 = Opcode("+0001")
    op2 = Opcode("-0001")

    result = op1 * op2

    assert result == Opcode("-0001")

## TODO: more tests

#############
# Division: #
#############

def test_integer_div():
    op = Opcode("+0004")

    result = op / 2

    assert result == Opcode("+0002")

def test_opcode_div():
    op1 = Opcode("+0004")
    op2 = Opcode("+0002")

    result = op1 / op2

    assert result == Opcode("+0002")

def test_opcode_div_with_remainder():
    op1 = Opcode("+0005")
    op2 = Opcode("+0002")

    result = op1 / op2

    assert result == Opcode("+0002")

## TODO: As always, more tests




    
