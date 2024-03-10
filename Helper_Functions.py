# Line 1
# @author Nathan Ulmen

class StringIntPair:
    def __init__(self, name, associated_value, description):
        self.name = name
        self.associated_value = associated_value
        self.description = description


class Color:
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


PINNACLE = StringIntPair(Color.RED + "PINNACLE" + Color.END, 0, "")
SPECIAL = StringIntPair(Color.ORANGE + "SPECIAL" + Color.END, 1, '')
EXOTIC = StringIntPair(Color.YELLOW + "EXOTIC" + Color.END, 2, '')
PRESTIGE = StringIntPair(Color.CYAN + "PRESTIGE" + Color.END, 3, '')
EPIC = StringIntPair(Color.PURPLE + "EPIC" + Color.END, 4, '')
SUPER_RARE = StringIntPair(Color.DARKCYAN + "SUPER_RARE" + Color.END, 5, '')
RARE = StringIntPair(Color.BLUE + "RARE" + Color.END, 6, '')
UNCOMMON = StringIntPair(Color.GREEN + "UNCOMMON" + Color.END, 7, '')
COMMON = StringIntPair("COMMON", 8, '')

validTiers = [PINNACLE, SPECIAL, EXOTIC, PRESTIGE, EPIC, SUPER_RARE, RARE, UNCOMMON, COMMON]


def prompt_for_tier(item_type):
    print()
    while True:
        print()
        for tier in validTiers:
            print(tier.associated_value, '-', tier.name)
        user_input = prompt_for_int(
            "Enter the Number associated with the tier you want the " + item_type + " to posses. ")
        for tier in validTiers:
            if tier.associated_value == user_input:
                return remove_color(tier.name)  # Need to remove color before printing to Json
        print(user_input, " is not a valid input.")


def prompt_for_string(prompt):
    print()
    return input(Color.BOLD + prompt + Color.END)


def prompt_for_float(prompt):
    print()
    while True:
        user_input = input(Color.BOLD + prompt + Color.END)
        try:
            user_input = float(user_input)
            return user_input
        except ValueError:
            print("Invalid input.")


def prompt_for_int(prompt):
    print()
    while True:
        user_input = input(Color.BOLD + prompt + Color.END)
        try:
            user_input = int(user_input)
            return user_input
        except ValueError:
            print("Invalid input. Make sure you enter an integer.")


def prompt_for_boolean(prompt):
    print()
    while True:
        user_input = input(Color.BOLD + prompt + "\n Enter 't' for true, 'f' for false: " + Color.END)
        if user_input.lower() == 't':
            return True
        elif user_input.lower() == 'f':
            return False
        else:
            print("Invalid input")


def remove_color(string):
    # Attribute is name of Property, EX: PURPLE, RED.
    # value is value associated with attribute EX: '\033[95m' is associated with purple
    for attr, value in vars(Color).items():
        if isinstance(value, str):
            string = string.replace(value, '')
    return string


ORE_VALUE = StringIntPair("ORE_VALUE", 0, '')
TEMPERATURE = StringIntPair("TEMPERATURE", 1, '')
MULTIORE = StringIntPair("MULTIORE", 2, '')

vtm = [ORE_VALUE, TEMPERATURE, MULTIORE]


def prompt_for_vtm(upg_type):
    print()
    while True:
        for value in vtm:
            print(value.associated_value, '-', value.name)
        user_input = prompt_for_int(
            Color.BOLD + "Which of those values would you like " + upg_type + " to modify? " + Color.END)
        for value in vtm:
            if user_input == value.associated_value:
                return value.name
        print(user_input, " is not a valid input.")
