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
    op = Opcode("+1234")
    assert str(op) == "+1234"

def test_init_with_minus():
    op = Opcode("-1234")
    assert str(op) == "-1234"

def test_init_with_no_sign():
    op = Opcode("1234")
    assert str(op) == "+1234"

def test_init_with_too_long():
    with pytest.raises(ValueError):
        Opcode("12345")

def test_init_with_too_short():
    with pytest.raises(ValueError):
        Opcode("123")

def test_init_with_non_num():
    with pytest.raises(ValueError):
        Opcode("12a4")

def test_init_with_empty():
    with pytest.raises(ValueError):
        Opcode("")

def test_init_with_too_large():
    with pytest.raises(ValueError):
        Opcode("+12345")

def test_init_with_too_small():
    with pytest.raises(ValueError):
        Opcode("+123")

#########
# Name: #
#########

def test_name():
    op = Opcode("+1034")
    assert op.name == "READ"

def test_noop():
    op = Opcode("+9999")
    assert op.name == "NOOP"

#########
# Sign: #
#########

def test_plus():
    op = Opcode("+1234")
    assert op.sign == "+"

def test_minus():
    op = Opcode("-1234")
    assert op.sign == "-"

############
# Operand: #
############

def test_operand():
    op = Opcode("+1234")
    assert op.operand == "34"

##########################
# String Representation: #
##########################

def test_str_from_minus():
    op = Opcode("-1234")
    assert str(op) == "-1234"

def test_str_from_plus():
    op = Opcode("+1234")
    assert str(op) == "+1234"

def test_str_from_no_sign():
    op = Opcode("1234")
    assert str(op) == "+1234"

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
    with pytest.raises(OverflowError):
        result = op1 + op2

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
    with pytest.raises(OverflowError):
        result = op1 - op2

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


#############
# Overflow: #
#############

def test_overflow():
    op1 = Opcode("+9999")
    op2 = Opcode("+0002")

    result = op1 + op2

    assert result == Opcode("+0001")

def test_underflow():
    op1 = Opcode("-9999")
    op2 = Opcode("+0002")

    result = op1 - op2

    assert result == Opcode("-0001")

    
