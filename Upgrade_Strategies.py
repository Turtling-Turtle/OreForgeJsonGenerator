#!/usr/bin/env python3
# @author Nathan Ulmen
from Helper_Functions import prompt_for_vtm, prompt_for_float, prompt_for_boolean, \
    list_prompt
from Ore_Strategies import prompt_for_ore_strategy

basic_upgrade = (1, "Basic Upgrade",
                 "A basic upgrade modifies an ore property by either addition, subtraction, multiplication, division, or modulo",
                 "ore.forge.Strategies.UpgradeStrategies.BasicUpgrade")

bundled_upg = (2, "Bundled Upgrade",
               "Select to bundle up different types of upgrades. EX: you want an upgrader that multiplies ore value and substracts ore Temperature.",
               "ore.forge.Strategies.UpgradeStrategies.BundledUPG")

conditional_upg = (3, "Conditional Upgrade", "A conditional upgrade. Will on type of upgrade if the condition is true and an else upgrade if condition is false.", "ore.forge.Strategies.UpgradeStrategies.ConditionalUPG")

influenced_upg = (4, "Influenced Upgrade", "Modifier is influenced/determined by another factor.",
                  "ore.forge.Strategies.UpgradeStrategies.InfluencedUPG")

resetter_upg = (
5, "Resetter Upgrade", "Resets the upgrade tags of ore. Make sure to tag or as resetter if you want it to be balanced!",
"ore.forge.Strategies.UpgradeStrategies.ResetterUPG")

apply_effect_upg = (
6, "Apply Effect", "Applies an effect to ore.", "ore.forge.Strategies.UpgradeStrategies.ApplyEffectUPG")

destruction_upg = (7, "Destroy Ore", "Destroys Ore.", "ore.forge.Strategies.UpgradeStrategies.DestructionUPG")

# These will require oreStrategy creation to be implemented:
# ApplyEffectUPG = StringIntPair('ApplyEffect', 8, "\tApplies an effect to the ore.")
# TargetedCleanser = StringIntPair('TargetedCleanser', 9, " \tRemoves an effect from the ore.")

upgrades = [basic_upgrade, bundled_upg, conditional_upg, influenced_upg, resetter_upg, apply_effect_upg,
            destruction_upg]


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
            bundle = {"upgradeName": resetter_upg[0]}
            return bundle
        elif upgrade is conditional_upg:
            return create_conditional_upg()
        elif upgrade is influenced_upg:
            return create_influenced_upg()
        elif upgrade is apply_effect_upg:
            return create_apply_effect()
        elif upgrade is destruction_upg:
            bundle = {"upgradeName": destruction_upg[0]}
            return bundle


add = (1, "Add", "Adds the modifier to the value to modify.", "ADD")
subtract = (2, "Subtract", "Subtracts the modifier from the value to modify.", "SUBTRACT")
multiply = (3, "Multiply", "Multiplies the value to modify by the modifier.", "MULTIPLY")
divide = (4, "Divide", "Divides the value to modify by the modifier.", "DIVIDE")
exponent = (5, "Exponent", "Raises the value to modify to the power of the modifier.", "EXPONENT")
assignment = (6, "Assignment", "Used to 'set' the value to modify to the value of the modifer.", "ASSIGNMENT")
modulo = (7, "Modulo", "Applies the modulo operator to two values.(Returns the remainder after two numbers are divided).", "MODULO")
operations = [add, subtract, multiply, divide, exponent, assignment, modulo]


def prompt_for_operation(prompt_string):
    while True:
        operator = list_prompt(operations, prompt_string, False)
        return operator[3]


def create_basic_upg():
    data = {
        "upgradeName": basic_upgrade[3],
        "valueToModify": prompt_for_vtm(basic_upgrade[1]),
        "operation": prompt_for_operation("Which operation would you like this upgrade to utilize? "),
        "modifier": prompt_for_float("Enter the modifier for your " + basic_upgrade[1] + ": ")
    }
    return data


# TODO: Update so that it generates until stopped, its no longer limited to just 4 values.
def create_bundled_upg():
    count = 1
    bundle = {
        "upgradeName": bundled_upg[3],
        "upgStrat" + str(count): prompt_for_upg_type("upgrade 1", False)
    }

    while True:
        count += 1
        result = prompt_for_upg_type("What would you like upgrade" + str(count) + " to do? ", True)
        if result == "null":
            return bundle
        else:
            bundle["upgStrat"+str(count)] = result


value = (1, "Ore Value", "The ores value.", "VALUE")
upgrade_count = (2, "Upgrade Count", "The ores upgrade count.", "UPGRADE_COUNT")
temperature = (3, "Temperature", "The ores temperature.", "TEMPERATURE")
multiore = (4, "Multiore", "The ores multiore.", "MULTIORE")
comparison_fields = [value, upgrade_count, temperature, multiore]


def prompt_for_condition():
    while True:
        condition = list_prompt(comparison_fields, "Which condition do you want to evaluate? ", False)
        return condition[3]


# [0] - AssociatedValue, [1]-Simple Name, [2] - Description, [3] - Real Name.
greater_than = (
1, "Greater Than", "Returns whether or not the specified value is greater than the threshold.", "GREATER_THAN")
greater_than_equal_to = (
2, "Greater Than or Equal To", "Returns whether or not the specified value is greater than or equal to the threshold.",
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
        "condition": prompt_for_condition(),
        "comparison": prompt_for_comparison(),
        "threshold": prompt_for_float("Threshold of the comparison:"),
        "ifModifier": prompt_for_upg_type("true upgrade", False),
        "elseModifier": prompt_for_upg_type("false upgrade", True)
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
    while True:
        value_of_influence = list_prompt(values_of_influence,
                                         "Which of those values would you like to influence this upgrades modifier?",
                                         False)
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
        "valueOfInfluence": prompt_for_voi(),
        "baseUpgrade": create_basic_upg(),
        "operation": prompt_for_operation(
            "How would you like this value of influence to influence/mutate the baseUpgrade?: "),
        "minModifier": optional_float_prompt("Would you like to set a min modifier? ",
                                             "Enter the minimum for the modifier: "),
        "maxModifier": optional_float_prompt("Would you like to set a max modifier? ",
                                             "Enter the maximum for the modifier: "),
        "scalar": prompt_for_float("Enter the scalar that is applied (Enter 1 if you dont want a scalar): ")
    }

    if data["minModifier"] == "null":
        del data["minModifier"]

    if data["maxModifier"] == "null":
        del data["maxModifier"]

    return data


def create_apply_effect():
    bundle = {
        "upgradeName": apply_effect_upg[3],
        "effectToApply": prompt_for_ore_strategy("Which ore effect would you like this upgrade to apply? ", False)
    }

    return bundle
