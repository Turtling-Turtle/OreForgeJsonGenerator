#!/usr/bin/env python3
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


# PINNACLE = StringIntPair(Color.RED + "PINNACLE" + Color.END, 0, "")
# SPECIAL = StringIntPair(Color.ORANGE + "SPECIAL" + Color.END, 1, '')
# EXOTIC = StringIntPair(Color.YELLOW + "EXOTIC" + Color.END, 2, '')
# PRESTIGE = StringIntPair(Color.CYAN + "PRESTIGE" + Color.END, 3, '')
# EPIC = StringIntPair(Color.PURPLE + "EPIC" + Color.END, 4, '')
# SUPER_RARE = StringIntPair(Color.DARKCYAN + "SUPER_RARE" + Color.END, 5, '')
# RARE = StringIntPair(Color.BLUE + "RARE" + Color.END, 6, '')
# UNCOMMON = StringIntPair(Color.GREEN + "UNCOMMON" + Color.END, 7, '')
COMMON = StringIntPair("COMMON", 8, '')


def list_prompt(values_to_prompt_from, prompt, can_take_zero):
    while True:
        for element in values_to_prompt_from:
            # [0] - AssociatedValue, [1]-Simple Name, [2] - Description, [3] - Real Name.
            print(element[0], "-", element[1], "-", element[2])
        user_input = prompt_for_int(prompt)
        if can_take_zero and user_input == 0:
            return user_input
        for element in values_to_prompt_from:
            if user_input == element[0]:
                return element
        print(user_input, " is an invalid input!")

# [0] - AssociatedValue, [1]-Simple Name, [2] - Description, [3] - Real Name.
pinnacle = (1, Color.RED + "Pinnacle" + Color.END, "TEMP DESCRIPTION- THE RAREST", "PINNACLE")
special = (2, Color.ORANGE + "Special" + Color.END, "TEMP DESCRIPTION- 2nd RAREST", "SPECIAL")
exotic = (3,Color.YELLOW + "Exotic" + Color.END, "TEMP DESCRIPTION - 3rd RAREST", "EXOTIC")
prestige = (4, Color.CYAN + "Prestige" + Color.END, "TEMP DESCRIPTION -4 RAREST", "PRESTIGE")
epic = (5, Color.PURPLE + "Epic" + Color.END, "TEMP DESCRIPTION -5th RAREST", "EPIC")
super_rare = (6, Color.DARKCYAN + "Super Rare" + Color.END, "TEMP DESCRIPTION -6th RAREST", "SUPER_RARE")
rare = (7, Color.BLUE + "Rare" + Color.END, "TEMP DESCRIPTION - 7th RAREST", "RARE")
uncommon = (8, Color.GREEN + "Uncommon" + Color.END, "TEMP DESCRIPTION - 8th RAREST", "UNCOMMON")
common = (9, "Common", "TEMP DESCRIPTION - 9th RAREST", "COMMON")
valid_tiers = [pinnacle, special, exotic, prestige, epic, super_rare, rare, uncommon, common]

def prompt_for_tier(item_type):
    while True:
        tier = list_prompt(valid_tiers, "Which tier would you like your " + item_type + " to have?", False)
        return tier[3]
    # while True:
    #     print()
    #     for tier in valid_tiers:
    #         print(tier.associated_value, '-', tier.name)
    #     user_input = prompt_for_int(
    #         "Enter the Number associated with the tier you want the " + item_type + " to posses. ")
    #     for tier in valid_tiers:
    #         if tier.associated_value == user_input:
    #             return remove_color(tier.name)  # Need to remove color before printing to Json
    #     print(user_input, " is not a valid input.")


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
        user_input = input(Color.BOLD + prompt + "\n Enter 'y' for yes, 'n' for no: " + Color.END)
        if user_input.lower() == 'y':
            return True
        elif user_input.lower() == 'n':
            return False
        else:
            print("Invalid input")

ore_value = (1, "Ore Value", "The ores value.", "ORE_VALUE")
temperature = (2, "Temperature", "The ores temperature.", "TEMPERATURE")
multiore = (3, "Multiore", "The ores multiore.", "MULTIORE")
speed = (4, "Speed", "The ores speed scalar.", "SPEED")
value_to_modify = [ore_value, temperature, multiore, speed]


def prompt_for_vtm(upg_type):
    while True:
        vtm = list_prompt(value_to_modify, "Which value would you like " + upg_type + " to modify? ", False)
        return vtm[3]
