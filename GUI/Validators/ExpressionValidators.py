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
special_functions = ["log(", "sqrt(", "ln("]


def is_negative(string):
    digit = re.search(r'(-?\d*\.?\d+(?:[eE]-?\d+)?)', string)
    return digit is not None and digit.group() is not None


def is_operand(string):
    return string is not None and string in numeric_ore_fields or string in other_fields or is_numeric(string)


def has_numeric_char(string):
    for char in string:
        if char.isdigit():
            return True
    return False


def isSpecialFunction(string: str) -> bool:
    return string and any(special_function in string for special_function in special_functions)


def getSpecialFunction(string: str) -> str:
    for special_function in special_functions:
        if special_function in string and string[1] == special_function[1]:
            return special_function


def create_Function(operandStack: LifoQueue, operatorStack: LifoQueue, wrapInParen: bool = None) -> str:
    try:
        right = operandStack.get_nowait()
        left = operandStack.get_nowait()
        operator = operatorStack.get_nowait()
        # operandStack.put(f"{left} {operator} {right}")
        return f"{left} {operator} {right}"
    except queue.Empty:
        raise ValueError("Operator stack is empty")


# TODO: Update to match the parser in Ore Forge.
# Returns an error message(String) if it fails to validate the function otherwise it returns the LifoQueue that holds the validated function.
def validate_function(function_string):
    trimmed_function = function_string.replace(r"(\d+)([-+])(\d+)", "$1 $2 $3")

    open_paren = trimmed_function.count("(")
    close_paren = trimmed_function.count(")")

    if open_paren > close_paren:
        return "Expression: " + trimmed_function + " has more opening parentheses than closing."
    elif close_paren > open_paren:
        return "Expression: " + trimmed_function + " has more closing parentheses than opening."

    # if open_paren == 0 or close_paren == 0:
    #     return "Expression: " + trimmed_function + " is missing required parenthesis."

    # pattern = re.compile(r"([a-zA-Z_]+)|(-?\d*\.?\d+(?:[eE]-?\d+)?)|\(|\)|\+|-|\*|/|=|%|\^")
    pattern = re.compile(
        "(log\\(|sqrt\\(|ln\\()((?:[^)(]|\\((?:[^)(]|\\((?:[^)(]|\\([^)(]*\\))*\\))*\\))*)|([a-zA-Z_]+)|(-?\\d*\\.?\\d+(?:[eE][-+]?\\d+)?)|\\(|\\)|([+\\-*/^=%])");

    operand_stack = LifoQueue()
    operator_stack = LifoQueue()

    tokens = []
    for token in re.finditer(pattern, trimmed_function):
        tokens.append(token)

    skip = False
    operand_count = 0
    for i in range(0, len(tokens)):
        if skip:
            skip = False
            continue
        print(i)
        previous_token = tokens[i - 1] if i > 0 else None
        current_Token = tokens[i]
        next_token = tokens[i + 1] if i < len(tokens) - 1 else None
        tokenString = tokens[i].group()

        # Correct function so that we don't mistake a subtraction for a negative.
        # if previous_token is not None and next_token is not None:
        if (previous_token is not None and is_operand(
                previous_token.group()) or previous_token and previous_token.group() == ")") and (
                next_token and next_token.group() == ")") and is_negative(tokenString):
            operator_stack.put("- ")
            operand_stack.put(tokenString.replace("-", ""))
            operand_count += 1
            continue

        # Check for implied multiplication
        elif tokenString == ")" and (
                next_token and next_token.group() == "("):  # Scenario: (30+32)(23+2) -> (30+32) * (23+2)
            while operator_stack.queue[-1] != "(":
                try:
                    operand_stack.put(create_Function(operand_stack, operator_stack))
                except ValueError as error:
                    return str(error)
                operand_count -= 1
            result = operand_stack.get_nowait()
            result = "(" + result + ")"
            operand_stack.put(result)
            operator_stack.get_nowait()  # Remove "(" character
            operator_stack.put("*")
            continue
        elif is_operand(tokenString) and (
                next_token and next_token.group() == "("):  # Scenario: 30(30+42) -> 30 * (30+42)
            operand_stack.put(tokenString)
            operator_stack.put("*")
            operand_count += 1
            continue
        elif (previous_token and previous_token.group() == ")") and is_operand(
                tokenString):  # Scenario: (30+42)30 -> (30+42) * 30
            operand_stack.put(tokenString)
            operator_stack.put("*")
            try:
                operand_stack.put(create_Function(operand_stack, operator_stack))
            except ValueError as error:
                return str(error)
            continue

        if tokenString == "(":
            operator_stack.put("(")
        elif tokenString == ")":
            while operator_stack.queue[-1] != "(":
                try:
                    operand_stack.put(create_Function(operand_stack, operator_stack))
                except ValueError as error:
                    return str(error)
                operand_count -= 1
            result = operand_stack.get_nowait()
            result = "(" + result + ")"
            operand_stack.put(result)
            operator_stack.get_nowait()  # Remove the "(" character
        elif is_operand(tokenString):
            operand_stack.put(tokenString)
            operand_count += 1
        elif tokenString in numeric_operators:
            operator_stack.put(tokenString)
        elif isSpecialFunction(tokenString):
            specialFunction = getSpecialFunction(tokenString)
            result = validate_function(current_Token.group(2))
            if isinstance(result, LifoQueue):
                operand_stack.put(specialFunction + result.get_nowait() + ")")
                print("After increment" + str(i))
                skip = True
            else:
                return result
        else:
            return "Invalid token " + tokenString + " in" + trimmed_function

    while not operator_stack.empty():
        try:
            operand_stack.put(create_Function(operand_stack, operator_stack))
        except ValueError as error:
            return str(error)
        operand_count -= 1
    if not operator_stack.empty():
        # Need to improve.
        return "Invalid Expression: " + trimmed_function + " operators remaining without operands."
    # elif operand_count != 1:
    #     return "Too many operands"
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
    # #
    "((ORE_VALUE * 5) + (TEMPERATURE / 2))",
    "(MULTIORE - (SPEED * 2))",
    "(ORE_VALUE -1)",
    "((UPGRADE_COUNT % 3) = 1)",
    # # Negative Number Tests
    "(-3 + 7)",
    "(4 * -2)",
    "((8 / -2) ^ 2)",
    "(-6 % -4)",
    "(-4 --3)",
    # # Invalid Strings
    # "(2 + * 3)",
    # "(4 * (5 - ))",
    # "(8 / 2) ^ 2)",
    # "(6 %)",
    # Other
    # "ORE_VALUE * 2) + 20) + ORE_VALUE * 2)) ((((",
    "32 + (47 * 900) / 90 + 20E90",
    "(20+2+3)(90+30+30)",
    "38 + ln(90+42+32(32)+42)",
    "ORE_VALUE(32+2)",
    "ORE_VALUE(sqrt(ORE_VALUE))",
]


def test_functions():
    for test_string in function_test_strings:
        # result = validate_function(test_string)
        result = validate_function(test_string)
        if isinstance(result, LifoQueue):
            result = Color.GREEN + "Successfully Verified Function: " + result.get_nowait() + Color.END
            print(f"{test_string}: {result}")
        else:
            print(f"{test_string}: {Color.RED + result + Color.END}")


# TODO: Implement boolean Condition Validation
def validate_condition(condition_string: str):
    pass


test_functions()
