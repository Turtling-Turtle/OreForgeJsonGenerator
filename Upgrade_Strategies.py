#!/usr/bin/env python3
# @author Nathan Ulmen
import queue

from Helper_Functions import prompt_for_vtm, prompt_for_float, prompt_for_boolean, \
    list_prompt, is_numeric, prompt_for_string
from Ore_Strategies import prompt_for_ore_strategy
from queue import LifoQueue
import re

basic_upgrade = (1, "Basic Upgrade",
                 "A basic upgrade modifies an ore property by either addition, subtraction, multiplication, division, or modulo",
                 "ore.forge.Strategies.UpgradeStrategies.BasicUpgrade")

bundled_upg = (2, "Bundled Upgrade",
               "Select to bundle up different types of upgrades. EX: you want an upgrader that multiplies ore value and substracts ore Temperature.",
               "ore.forge.Strategies.UpgradeStrategies.BundledUpgrade")

conditional_upg = (3, "Conditional Upgrade",
                   "A conditional upgrade. Will on type of upgrade if the condition is true and an else upgrade if condition is false.",
                   "ore.forge.Strategies.UpgradeStrategies.ConditionalUpgrade")

influenced_upg = (4, "Influenced Upgrade", "Modifier is influenced/determined by another factor.",
                  "ore.forge.Strategies.UpgradeStrategies.InfluencedUpgrade")

resetter_upg = (
    5, "Resetter Upgrade",
    "Resets the upgrade tags of ore. Make sure to tag or as resetter if you want it to be balanced!",
    "ore.forge.Strategies.UpgradeStrategies.ResetterUpgrade")

apply_effect_upg = (
    6, "Apply Effect", "Applies an effect to ore.", "ore.forge.Strategies.UpgradeStrategies.ApplyEffectUpgrade")

destruction_upg = (7, "Destroy Ore", "Destroys Ore.", "ore.forge.Strategies.UpgradeStrategies.DestructionUpgrade")

cooldown_upg = (8, "Cooldown Upgrade", "Held upgrade has a cooldown after being applied",
                "ore.forge.Strategies.UpgradeStrategies.CooldownUpgrade")

incremental_upg = (9, "Incremental Upgrade",
                   "The upgrades modifier is change if a condition is met, the modifier resets once it reaches a specific threshold.",
                   "ore.forge.Strategeis.UpgradStrategies.IncrementalUpgrade")

# These will require oreStrategy creation to be implemented:
# ApplyEffectUPG = StringIntPair('ApplyEffect', 8, "\tApplies an effect to the ore.")
# TargetedCleanser = StringIntPair('TargetedCleanser', 9, " \tRemoves an effect from the ore.")

upgrades = [basic_upgrade, bundled_upg, conditional_upg, influenced_upg, resetter_upg, apply_effect_upg,
            destruction_upg, cooldown_upg]


# [0] - AssociatedValue, [1]-Simple Name, [2] - Description, [3] - Real Name.

def prompt_for_upg_type(strat, can_return_zero):
    while True:
        upgrade = list_prompt(upgrades, "Which type of Upgrade would you like " + strat + " to be?", can_return_zero)
        if upgrade == 0 and can_return_zero:
            return "null"
        if upgrade is basic_upgrade:
            return create_basic_upg()
        elif upgrade is bundled_upg:
            return create_bundled_upg()
        elif upgrade is resetter_upg:
            bundle = {"upgradeName": resetter_upg[3]}
            return bundle
        elif upgrade is conditional_upg:
            return create_conditional_upg()
        elif upgrade is influenced_upg:
            return create_influenced_upg()
        elif upgrade is apply_effect_upg:
            return create_apply_effect()
        elif upgrade is destruction_upg:
            bundle = {"upgradeName": destruction_upg[3]}
            return bundle
        elif upgrade is cooldown_upg:
            return create_cooldown_upgrade()


add = (1, "Add", "Adds the modifier to the value to modify.", "ADD")
subtract = (2, "Subtract", "Subtracts the modifier from the value to modify.", "SUBTRACT")
multiply = (3, "Multiply", "Multiplies the value to modify by the modifier.", "MULTIPLY")
divide = (4, "Divide", "Divides the value to modify by the modifier.", "DIVIDE")
exponent = (5, "Exponent", "Raises the value to modify to the power of the modifier.", "EXPONENT")
assignment = (6, "Assignment", "Used to 'set' the value to modify to the value of the modifier.", "ASSIGNMENT")
modulo = (
    7, "Modulo", "Applies the modulo operator to two values.(Returns the remainder after two numbers are divided).",
    "MODULO")
operations = [add, subtract, multiply, divide, exponent, assignment, modulo]


def prompt_for_operator(prompt_string):
    operator = list_prompt(operations, prompt_string, False)
    return operator[3]


def create_basic_upg():
    data = {
        "upgradeName": basic_upgrade[3],
        "valueToModify": prompt_for_vtm(basic_upgrade[1]),
        "operation": prompt_for_operator("Which operation would you like this upgrade to utilize? "),
        "modifier": prompt_for_float("Enter the modifier for your " + basic_upgrade[1] + ": ")
    }
    return data


def create_bundled_upg():
    count = 1
    bundle = {
        "upgradeName": bundled_upg[3],
        "upgStrat" + str(count): prompt_for_upg_type("upgrade" + str(count), False)
    }

    while True:
        count += 1
        result = prompt_for_upg_type("What would you like upgrade" + str(count) + " to do? ", True)
        if result == "null":
            return bundle
        else:
            bundle["upgStrat" + str(count)] = result


value = (1, "Ore Value", "The ores value.", "ORE_VALUE")
upgrade_count = (2, "Upgrade Count", "The ores upgrade count.", "UPGRADE_COUNT")
temperature = (3, "Temperature", "The ores temperature.", "TEMPERATURE")
multiore = (4, "Multiore", "The ores multiore.", "MULTIORE")
comparison_fields = [value, upgrade_count, temperature, multiore]


# TODO: update to verify that entered expression is valid.
def prompt_for_condition():
    condition = list_prompt(comparison_fields, "Which condition do you want to evaluate? ", False)
    return condition[3]


# [0] - AssociatedValue, [1]-Simple Name, [2] - Description, [3] - Real Name.
greater_than = (
    1, "Greater Than", "Returns whether or not the specified value is greater than the threshold.", "GREATER_THAN")
greater_than_equal_to = (
    2, "Greater Than or Equal To",
    "Returns whether or not the specified value is greater than or equal to the threshold.",
    "GREATER_THAN_EQUAL_TO")
less_than = (3, "Less Than", "Returns whether or not a the specified value is less than the threshold.", "LESS_THAN")
less_than_equal_to = (
    4, "Less Than or Equal To", "Returns whether or not the specified value is less than or equal to the threshold.",
    "LESS_THAN_EQUAL_TO")
equal_to = (5, "Equal To", "Returns if a the specified value is equal to the threshold.", "EQUAL_TO")
comparison_types = [greater_than, greater_than_equal_to, less_than, less_than_equal_to, equal_to]


def prompt_for_comparison():
    boolean_operator = list_prompt(comparison_types, "Which Boolean operator would you like to apply? ", False)
    return boolean_operator[3]


def create_conditional_upg():
    bundle = {
        "upgradeName": conditional_upg[3],
        # "condition": prompt_for_condition(),
        "condition": prompt_for_string("Enter your condition: "),
        "trueBranch": prompt_for_upg_type("true upgrade", False),
        "falseBranch": prompt_for_upg_type("false upgrade", True)
    }
    return bundle


def create_resetter_upg():
    bundle = {
        "upgradeName": resetter_upg[3]
    }

    return bundle


active_ore = (5, "Active Ore", "Number of Ore currently active on the base.", "ACTIVE_ORE")
placed_items = (6, "Placed Items", "Number of Items currently on the base.", "PLACED_ITEMS")
special_points = (7, "Special Points", "The number of Special Points that the player has.", "SPECIAL_POINTS")
wallet = (8, "Wallet", "The amount of money that the player currently has.", "WALLET")
prestige_level = (9, "Prestige Level", "The players current prestige level.", "PRESTIGE_LEVEL")
values_of_influence = [value, upgrade_count, temperature, multiore, active_ore, placed_items, special_points, wallet,
                       prestige_level]


# prompt for value of influence
def prompt_for_voi():
    value_of_influence = list_prompt(values_of_influence, "Which of those values would you like to influence this upgrades modifier?", False)
    return value_of_influence[3]


def optional_float_prompt(prompt_string1, prompt_string2):
    if prompt_for_boolean(prompt_string1):
        return prompt_for_float(prompt_string2)
    else:
        return "null"


# TODO: Make this prompt easier to follow/understand.
def create_influenced_upg():
    data = {
        "upgradeName": influenced_upg[3],
        "upgradeFunction": prompt_for_upgrade_function(),
        "numericOperator": prompt_for_operator("How would you like this upgrade to be applied? "),
        "valueToModify": prompt_for_vtm(influenced_upg[1]),
        "minModifier": optional_float_prompt("Would you like to set a min modifier? ",
                                             "Enter the minimum for the modifier: "),
        "maxModifier": optional_float_prompt("Would you like to set a max modifier? ",
                                             "Enter the maximum for the modifier: "),
    }

    if data["minModifier"] == "null":
        del data["minModifier"]

    if data["maxModifier"] == "null":
        del data["maxModifier"]

    return data


# TODO: Add better error handling for parsing function and more informative feedback when there are errors in the inputs syntax
# Verify that each parenthesis has a "partner"
# Ideally we would be able to know exactly where the missing parenthesis is located and alert/notify the user.
def prompt_for_upgrade_function():
    operand_stack = LifoQueue()
    operator_stack = LifoQueue()
    while True:
        print("((ORE_VALUE * 2) + 20)")
        untrimmed_input = input("Please enter your function, it should look similar to the function above: ")
        trimmed_input = untrimmed_input.replace(r"\\s", "")
        opening_paren_count = trimmed_input.count("(")
        closing_paren_count = trimmed_input.count(")")
        if opening_paren_count != closing_paren_count:
            if opening_paren_count > closing_paren_count:
                print("Your parenthesis do not match!")
            continue  # continue tells the current loop to "restart itself" in this case that's the while loop
        pattern = re.compile(r"([a-zA-Z_]+|\(|\)|\d+(\.\d+)?|\+|-|\*|/|=|%|\^)")
        for token in re.finditer(pattern, trimmed_input):
            token_string = token.group()
            if token_string == "(":
                pass
            elif token_string == ")":
                try:
                    right_operand = operand_stack.get_nowait()
                    left_operand = operand_stack.get_nowait()
                    operator = operator_stack.get_nowait()
                    function_string = "(" + left_operand + operator + right_operand + ")"
                    operand_stack.put(function_string)
                except queue.Empty:
                    print(untrimmed_input + "Formatting is incorrect!")
            elif is_numeric(token_string) or token_string in [tuple_field[3] for tuple_field in values_of_influence]:
                operand_stack.put(token_string)
            elif token_string in ["+", "-", "*", "/", "=", "%", "^"]:
                operator_stack.put(token_string)
            else:
                print("Invalid input")
                operand_stack.empty()
                operator_stack.empty()
        return operand_stack.get_nowait()


def create_apply_effect():
    bundle = {
        "upgradeName": apply_effect_upg[3],
        "effectToApply": prompt_for_ore_strategy("Which ore effect would you like this upgrade to apply? ", False)
    }

    return bundle


def create_cooldown_upgrade():
    bundle = {
        "upgradeName": cooldown_upg[3],
        "upgrade": prompt_for_upg_type("Which upgrade would you like to be applied on a cooldown? ", False),
        "cooldownTime": prompt_for_float("Enter the cooldown time in seconds: "),
    }

    return bundle


# TODO: Make some of the prompts optional
def create_incremental_upgrade():
    bundle = {
        "upgradeName": incremental_upg[3],
        "baseModifier": prompt_for_float("Enter the base Modifier: "),
        "trueStep": prompt_for_upgrade_function(),
        "trueBranchOperator": prompt_for_operator(
            "How would you like the result of trueStep to be applied to the modifier?"),
        "falseStep": prompt_for_upgrade_function(),
        "falseBranchOperator": prompt_for_operator(
            "How would you like the result of the falseStep to be applied to the modifier?"),
        "numericOperator": prompt_for_operator("How do you want this upgrade to modify the ore property? "),
        "valueToModify": prompt_for_vtm("Which value do you want this upgrade to be applied to? "),
        "triggerCondition": prompt_for_string("Enter the trigger condition: "),
        "threshold": prompt_for_upgrade_function(),
    }

    return bundle
