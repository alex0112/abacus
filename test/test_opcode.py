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

def test_init_with_plus_4digit():
    op = Opcode("+1234")
    assert str(op) == "+001234"

def test_init_with_minus_4digit():
    op = Opcode("-1234")
    assert str(op) == "-001234"

def test_init_with_no_sign_4digit():
    op = Opcode("1234")
    assert str(op) == "+001234"

def test_init_with_too_long():
    with pytest.raises(ValueError):
        Opcode("12345678")

def test_init_with_too_short():
    with pytest.raises(ValueError):
        Opcode("123")

def test_init_with_non_num():
    with pytest.raises(ValueError):
        Opcode("12a456")

def test_init_with_empty():
    with pytest.raises(ValueError):
        Opcode("")

def test_init_with_too_large():
    with pytest.raises(ValueError):
        Opcode("+12345678")

def test_init_with_too_small():
    with pytest.raises(ValueError):
        Opcode("+123")

#########
# Name: #
#########

def test_name_4digit():
    op = Opcode("+1034")
    assert op.name == "READ"

def test_noop_4digit():
    op = Opcode("+9999")
    assert op.name == "NOOP"

#########
# Sign: #
#########

def test_plus_4digit():
    op = Opcode("+1234")
    assert op.sign == "+"

def test_minus_4digit():
    op = Opcode("-1234")
    assert op.sign == "-"

############
# Operand: #
############

def test_operand_4digit():
    op = Opcode("+1088") ## operand to READ
    assert op.operand == "088"

def test_operand_6digit():
    op = Opcode("+010042")
    assert op.operand == "042"

##########################
# String Representation: #
##########################

def test_str_from_minus_4digit():
    op = Opcode("-7777")
    assert str(op) == "-007777"

def test_str_from_plus_4digit():
    op = Opcode("+7777")
    assert str(op) == "+007777"

def test_str_from_no_sign_4digit():
    op = Opcode("7777")
    assert str(op) == "+007777"

#############
# Equality: #
#############

def test_basic_equality_4digit():
    op1 = Opcode("+0000")
    op2 = Opcode("+0000")
    assert op1 == op2

def test_basic_inequality_4digit():
    op1 = Opcode("+1000")
    op2 = Opcode("+0001")
    assert op1 != op2

#############
# Addition: #
#############

def test_basic_add_4digit():
    op1 = Opcode("+0000")
    op2 = Opcode("+1000")
    result = op1 + op2
    assert result == Opcode("+1000")

def test_add_negative_and_positive_4digit():
    op1 = Opcode("+0000")
    op2 = Opcode("-1000")
    result = op1 + op2
    assert result == Opcode("-1000")

def test_add_negative_and_negative_4digit():
    op1 = Opcode("-1000")
    op2 = Opcode("-1000")
    result = op1 + op2
    assert result == Opcode("-2000")

################
# Subtraction: #
################

def test_basic_subtraction_4digit():
    op1 = Opcode("+0000")
    op2 = Opcode("+1000")
    result = op1 - op2
    assert result == Opcode("-1000")

def test_subtract_a_negative_4digit():
    op1 = Opcode("+0000")
    op2 = Opcode("-1000")
    result = op1 - op2
    assert result == Opcode("+1000")

###################
# Multiplication: #
###################

def test_mul_4digit():
    op1 = Opcode("+0000")
    op2 = Opcode("+0001")
    result = op1 * op2
    assert result == Opcode("+0000")

def test_mul_neg_4digit():
    op1 = Opcode("+0001")
    op2 = Opcode("-0001")
    result = op1 * op2
    assert result == Opcode("-0001")

#############
# Division: #
#############

def test_integer_div_4digit():
    op = Opcode("+0004")
    result = op / 2
    assert result == Opcode("+0002")

def test_opcode_div_4digit():
    op1 = Opcode("+0004")
    op2 = Opcode("+0002")
    result = op1 / op2
    assert result == Opcode("+0002")

def test_opcode_div_with_remainder_4digit():
    op1 = Opcode("+0005")
    op2 = Opcode("+0002")
    result = op1 / op2
    assert result == Opcode("+0002")

#############
# Overflow: #
#############

def test_overflow_addition():
    op1 = Opcode("+999999")
    op2 = Opcode("+000002")

    result = op1 + op2

    assert result == Opcode("+000001")

def test_underflow_subtraction():
    op1 = Opcode("-999999")
    op2 = Opcode("+000002")

    result = op1 - op2

    print(f"result: {result}")
    assert result == Opcode("-000001")

def test_overflow_product_4digit():
    op1 = Opcode("+999999")
    op2 = Opcode("+000010")

    result = op1 * op2

    print(f"{op1} * {op2} == {result.numeric}")
    assert result == Opcode("+999990")

def test_underflow_product_4digit():
    op1 = Opcode("-999999")
    op2 = Opcode("+000002")

    result = op1 * op2
    print(f"{op1} * {op2} == {result.numeric}")

    assert result == Opcode("-999998")

##################
# Human Readable #
##################

def test_named_opcode_4digit():
    write_op = Opcode("+1101")
    read_op = Opcode("+1002")

    assert write_op.human_friendly == "WRITE 001"
    assert read_op.human_friendly == "READ 002"

def test_unamed_opcode_4digit():
    op1 = Opcode("-0001")
    op2 = Opcode("+7700")

    assert op1.human_friendly == "NOOP"
    assert op2.human_friendly == "NOOP"

#################################
# New Six Digit Opcode Behavior #
#################################

def test_unnamed_opcode_NOOP():
    op4 = Opcode("+7777")
    op6 = Opcode("+777777")

    assert op4.raw == "+007777"
    assert op6.raw == "+777777"

def test_named_opcode_READ():
    op4 = Opcode("+1010")
    op6 = Opcode("+010010")

    assert op4.raw == "+010010"
    assert op6.raw == "+010010"

# def test_named_opcode_WRITE():
#     op4 = Opcode("+1110")
#     op6 = Opcode("+012010")

#     assert str(op4) == "WRITE 010"
#     assert str(op6) == "WRITE 010"

# def test_named_opcode_WRITE():
#     op4 = Opcode("+1110")
#     op6 = Opcode("+012010")

#     assert str(op4) == "WRITE 010"
#     assert str(op6) == "WRITE 010"

# def test_named_opcode_LOAD():
#     op4 = Opcode("+1110")
#     op6 = Opcode("+012010")

#     assert str(op4) == "LOAD 010"
#     assert str(op6) == "LOAD 010"

# def test_named_opcode_STORE:
#     pass
