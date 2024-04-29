import queue
from queue import LifoQueue
import re

from Helper_Functions import is_numeric

"""
Reserved Words:

    Numeric Ore Fields: ORE_VALUE, TEMPERATURE, MULTIORE, SPEED, UPGRADE_COUNT
    String Ore Fields: NAME, ID, "TYPE"

    Others: ACTIVE_ORE, PLACED_ITEMS, SPECIAL_POINTS, WALLET, PRESTIGE_LEVEL

    Logical Operators: NOT, XOR, AND, OR

"""

numeric_ore_fields = ["ORE_VALUE", "TEMPERATURE", "MULTIORE", "SPEED", "UPGRADE_COUNT"]
string_ore_fields = ["NAME", "ID", "TYPE"]
other_fields = ["ACTIVE_ORE", "PLACED_ITEMS", "SPECIAL_POINTS", "WALLET", "PRESTIGE_LEVEL", "PRESTIGE_LEVEL"]
logical_operators = ["NOT", "XOR", "AND", "OR"]
numeric_operators = ["+", "-", "*", "/", "=", "%", "^"]


def validate_function(function_string):
    operand_stack = LifoQueue()
    operator_stack = LifoQueue()
    trimmed_string = function_string.replace(r"(\d+)([-+])(\\d+)", "$1 $2 $3")
    open_paren = trimmed_string.count("(")
    close_paren = trimmed_string.count(")")
    if open_paren != close_paren:
        # print("FAILED")
        return False
    pattern = re.compile(r"([a-zA-Z_]+)|([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)|\(|\)|\+|-|\*|/|=|%|\^")
    # TODO: Implement Internal state machine for what token type to expect next to allow for better error messages.
    operand_count = 0
    for token in re.finditer(pattern, trimmed_string):
        token_string = token.group()
        if token_string == "(":
            pass
        elif token_string == ")":
            try:
                right_operand = operand_stack.get_nowait()
                left_operand = operand_stack.get_nowait()
                operand_count -= 2
                operator = operator_stack.get_nowait()
                function_string = "(" + left_operand + operator + right_operand + ")"
                operand_stack.put(function_string)
                operand_count += 1
            except queue.Empty:
                return False
        elif is_numeric(token_string) or token_string in numeric_ore_fields or token_string in other_fields:
            operand_stack.put(token_string)
            operand_count += 1
        elif token_string in numeric_operators:
            operator_stack.put(token_string)
        else:
            return False
    return operator_stack.empty() and operand_count == 1


function_test_strings = [
    "(ORE_VALUE + -TEMPERATURE)",  # Invalid
    "(-2.56E10 / ACTIVE_ORE)",  # Valid
    "(ORE_VALUE * -0.1)",  # Valid
    "(SPEED*-2)",  # Valid
    "((ORE_VALUE + TEMPERATURE) + 20)",  # Valid
    "((SPEED + 2.5) * TEMPERATURE)",  # Valid
    "(UPGRADE_COUNT - 20) +20",  # Invalid
    "(INVALID_FIELD * 2)",  # Invalid
    "(UPGRADE_COUNT / 0)",  # Valid
    "((ORE_VALUE + TEMPERATURE) *)",  # Invalid
    "(ID = '123' AND WALLET + 1000)"  # Invalid
]


def test_functions():
    for test_string in function_test_strings:
        print(f"{test_string}: {validate_function(test_string)}")


# TODO: Implement boolean Condition Validation
def validate_condition(condition_string):
    pass


test_functions()
