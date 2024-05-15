import queue
from queue import LifoQueue
import re

from Helper_Functions import is_numeric, Color

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


def is_negative(string):
    digit = re.search(r'(-?\d*\.?\d+(?:[eE]-?\d+)?)', string)
    return digit is not None and digit.group() is not None


def is_operand(string):
    return string in numeric_ore_fields or string in other_fields or is_numeric(string) or string == ")"


def has_numeric_char(string):
    for char in string:
        if char.isdigit():
            return True
    return False


# Returns an error message(String) if it fails to validate the function otherwise it returns the LifoQueue that holds the validated function.
def validate_function(function_string):
    trimmed_function = function_string.replace(r"(\d+)([-+])(\\d+)", "$1 $2 $3")
    open_paren = trimmed_function.count("(")
    close_paren = trimmed_function.count(")")
    if open_paren != close_paren:
        return "Expression: " + trimmed_function + " has unbalanced parenthesis."
    if open_paren == 0 or close_paren == 0:
        return "Expression: " + trimmed_function + " is missing required parenthesis."
    pattern = re.compile(r"([a-zA-Z_]+)|(-?\d*\.?\d+(?:[eE]-?\d+)?)|\(|\)|\+|-|\*|/|=|%|\^")
    operand_stack = LifoQueue()
    operator_stack = LifoQueue()
    # TODO: Implement Internal state machine for what token type to expect next to allow for better error messages.

    tokens = []
    for token in re.finditer(pattern, trimmed_function):
        tokens.append(token.group())

    operand_count = 0
    for i in range(0, len(tokens)):
        previous_token = tokens[i - 1] if i > 0 else None
        current_token = tokens[i]
        next_token = tokens[i + 1] if i < len(tokens) - 1 else None

        # if has_numeric_char(current_token):
        #     current_token.replace(r",", "")

        # Correct function so that we don't mistake a subtraction for a negative.
        if previous_token is not None and next_token is not None:
            if is_operand(previous_token) and next_token == ")" and is_negative(current_token):
                operator_stack.put("- ")
                operand_stack.put(current_token.replace("-", ""))
                operand_count += 1
                continue
        if current_token == "(":
            pass
        elif current_token == ")":
            try:
                right_operand = operand_stack.get_nowait()
                left_operand = operand_stack.get_nowait()
                operand_count -= 2
                operator = operator_stack.get_nowait()
                function_string = "(" + left_operand + operator + right_operand + ")"
                operand_stack.put(function_string)
                operand_count += 1
            except queue.Empty:
                # TODO expand to give more descriptive errors here.
                return "Invalid Expression: " + trimmed_function
        elif current_token in numeric_ore_fields or current_token in other_fields or is_numeric(current_token):
            operand_stack.put(current_token)
            operand_count += 1
        elif current_token in numeric_operators:
            operator_stack.put(current_token)
        else:
            return "Invalid token " + current_token + " in" + trimmed_function
    if not operator_stack.empty():
        # Need to improve.
        return "Invalid Expression: " + trimmed_function + " operators remaining without operands."
    elif operand_count != 1:
        return "Too many operands"
    return operand_stack


function_test_strings = [
    "(2 + 3)",
    "(-2 - -3)",
    "(-8300 --1.0)",
    "(4 * (5 - 2))",
    "((8 / 2) ^ 2)",
    "(6 % 4)",
    "(ORE_VALUE + TEMPERATURE)",
    "(MULTIORE / SPEED)",
    "(UPGRADE_COUNT = 10)",
    #
    "((ORE_VALUE * 5) + (TEMPERATURE / 2))",
    "(MULTIORE - (SPEED * 2))",
    "(ORE_VALUE -1)",
    "((UPGRADE_COUNT % 3) = 1)",
    # Negative Number Tests
    "(-3 + 7)",
    "(4 * -2)",
    "((8 / -2) ^ 2)",
    "(-6 % -4)",
    "(-4 --3)",
    # Invalid Strings
    "(2 + * 3)",
    "(4 * (5 - ))",
    "(8 / 2) ^ 2)",
    "(6 %)",
    #Other
    "ORE_VALUE * 2) + 20) + ORE_VALUE * 2)) ((((",
]


def test_functions():
    for test_string in function_test_strings:
        result = validate_function(test_string)
        if isinstance(result, LifoQueue):
            result = Color.GREEN + "Successfully Verified Function: " + result.get_nowait() + Color.END
            print(f"{test_string}: {result}")
        else:
            print(f"{test_string}: {Color.RED + result + Color.END}")


# TODO: Implement boolean Condition Validation
def validate_condition(condition_string):
    pass


test_functions()
