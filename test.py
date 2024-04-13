import queue, re
from queue import LifoQueue


def prompt_for_upgrade_function():
    #1st: We give them all the info they need to know for creating an upgradeFunction
    #2nd: prompt them for their String.
    #3rd: verify that the input is actually a valid upgradeFunction by "compiling" it. (aka just do what the java algorithm does and see if it works)
    print("((ORE_VALUE * 2) + 20)")
    user_input = input("Please enter your function, it should look similar to the function above: ")
    # user_input = re.sub("\\s", '', user_input) # Trim white space.
# operand_stack = queue.LifoQueue

    # operator_stack = queue.LifoQueue()
    operand_stack = LifoQueue
    operator_stack = LifoQueue
    pattern = re.compile("([a-zA-Z_]+|\\(|\\)|\\d+(\\.\\d+)?|\\+|-|\\*|/|=|%|^)")
    for token in re.finditer(pattern, user_input):
        print(token.group())
        if token == "(":
            print()
        elif token == ")":
            right_operand = operand_stack.get()
            left_operand = operand_stack.get()
            operator = operator_stack.get()
            function = (right_operand, operator, left_operand)
            operand_stack.put(function)
        elif token.group().isdigit() == "ORE_VALUE":
            operand_stack.put(token.group())
        elif token.group() == "*" or "+":
            operator_stack.put(token.group())
        elif token.group().isdigit():
            operand_stack.put((token.group()))

    return operand_stack.get()


func = prompt_for_upgrade_function()
print(func)