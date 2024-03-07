# @author Nathan Ulmen

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ORANGE = '\x1b[38;5;208m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Tier:
    def __init__(self, name, associated_value):
        self.name = name
        self.associated_value = associated_value


PINNACLE = Tier(color.RED + "PINNACLE" + color.END, 0)
SPECIAL = Tier(color.ORANGE + "SPECIAL" + color.END, 1)
EXOTIC = Tier(color.YELLOW + "EXOTIC" + color.END, 2)
PRESTIGE = Tier(color.CYAN + "PRESTIGE" + color.END, 3)
EPIC = Tier(color.PURPLE + "EPIC" + color.END, 4)
SUPER_RARE = Tier(color.DARKCYAN + "SUPER_RARE" + color.END, 5)
RARE = Tier(color.BLUE + "RARE" + color.END, 6)
UNCOMMON = Tier(color.GREEN + "UNCOMMON" + color.END, 7)
COMMON = Tier("COMMON", 8)

validTiers = []
validTiers.append(PINNACLE)
validTiers.append(SPECIAL)
validTiers.append(EXOTIC)
validTiers.append(PRESTIGE)
validTiers.append(EPIC)
validTiers.append(SUPER_RARE)
validTiers.append(RARE)
validTiers.append(UNCOMMON)
validTiers.append(COMMON)


def prompt_for_tier(item_type):
    while True:
        print()
        for tier in validTiers:
            print(tier.associated_value, '-', tier.name)
        user_input = prompt_for_int(
            "Enter the Number associated with the tier you want the " + item_type + " to posses. ")
        for tier in validTiers:
            if tier.associated_value == user_input:
                return remove_color(tier.name)  # Need to remove color before printing to Json
        print(user_input,  " is not a valid input.")


def prompt_for_string(prompt):
    return input(prompt)


def prompt_for_float(prompt):
    while True:
        user_input = input(prompt)
        try:
            user_input = float(user_input)
            return user_input
        except ValueError:
            print("Invalid input.")


def prompt_for_int(prompt):
    while True:
        user_input = input(prompt)
        try:
            user_input = int(user_input)
            return user_input
        except ValueError:
            print("Invalid input. Make sure you enter an integer.")


def prompt_for_boolean(prompt):
    while True:
        user_input = input(prompt + "\n Enter 't' for true, 'f' for false: ")
        if user_input.lower() == 't':
            return True
        elif user_input.lower() == 'f':
            return False
        else:
            print("Invalid input")


def remove_color(string):
    # Attribute is name of Property, EX: PURPLE, RED.
    # value is value associated with attribute EX: '\033[95m' is associated with purple
    for attr, value in vars(color).items():
        if isinstance(value, str):
            string = string.replace(value, '')
    return string

class ValueToModify:
    def __init__(self, name, associated_value):
        self.name = name
        self.associated_value = associated_value

ORE_VALUE = ValueToModify("ORE_VALUE", 0)
TEMPERATURE = ValueToModify("TEMPERATURE", 1)
MULTIORE = ValueToModify("MULTIORE", 2)

vtm = [ORE_VALUE, TEMPERATURE, MULTIORE]

def prompt_for_vtm():
    while True:
        for value in vtm:
            print(value.associated_value, value.name)
        user_input = prompt_for_int("Which of those values would you like this effect to modify?")
        for value in vtm:
            if user_input == value.associated_value:
                return value.name
        print(user_input, " is not a valid input.")
