#!/usr/bin/env python3
# @author Nathan Ulmen
from Helper_Functions import prompt_for_int, prompt_for_vtm, prompt_for_float, StringIntPair

basic_upgrade = ("ore.forge.Strategies.UpgradeStrategies.BasicUpgrade", "Basic Upgrade", 1,
                 "A basic upgrade modifies an ore property by either addition, subtraction, multiplication, division, or modulo")
bundled_upg = ('ore.forge.Strategies.UpgradeStrategies.BundledUPG', "Bundled Upgrade", 2,
               " \tSelect to bundle up different types of upgrades. EX: you want an upgrader that multiplies ore value and substracts ore Temperature.")
conditional_upg = ('ore.forge.Strategies.UpgradeStrategies.ConditionalUPG', "Conditional Upgrade", 3,
                   "\tA conditional upgrade. Will on type of upgrade if the condition is true and an else upgrade if condition is false.")
influenced_upg = ('ore.forge.Strategies.UpgradeStrategies.InfluencedUPG', "Influenced Upgrade", 4,
                  "\tModifier is inluenced/determined by another factor.")
resetter_upg = ('ore.forge.Strategies.UpgradeStrategies.ResetterUPG', "Resetter Upgrade", 5,
                "\tResets the upgrade tags of ore. Make sure to tag or as ressetter if you want it to be balanced!")
apply_effect_upg = (
    'ore.forge.Strategies.UpgradeStrategies.ApplyEffectUPG', "Apply Effect", 6, "\tApplies an effect to ore.")

# These will require oreStrategy creation to be implemented:
# ApplyEffectUPG = StringIntPair('ApplyEffect', 8, "\tApplies an effect to the ore.")
# TargetedCleanser = StringIntPair('TargetedCleanser', 9, " \tRemoves an effect from the ore.")

# UPGS = [AddUPG, MultiplyUPG, SubtractUPG, BundledUPG, ConditionalUPG, InfluencedUPG, ResetterUPG, ApplyEffectUPG]
upgrades = [basic_upgrade, bundled_upg, conditional_upg, influenced_upg, resetter_upg]


def prompt_for_upg_type(strat):
    data = {

    }
    while True:
        print()
        for upgrade in upgrades:
            print(upgrade[2], "-", upgrade[1], "\t", upgrade[3])
        print("Enter 0 if you want dont want to add an upgrade. ")
        user_input = prompt_for_int("What type of Upgrade would you like " + strat + " to be? ")
        if user_input == 0:
            return "null"
        for upgrade in upgrades:
            if user_input == upgrade[2]:
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
        print(user_input, "is not a valid Upgrade")


ADD = ("Add", 0)
SUBTRACT = ("Subtract", 1)
MULTIPLY = ("Multiply", 2)
DIVIDE = ("Divide", 3)
MODULO = ("Modulo", 4)
operations = [ADD, SUBTRACT, MULTIPLY, DIVIDE, MODULO]


def prompt_for_operation(prompt_string):
    while True:
        for operation in operations:
            print(operation[1], "-", operation[0])
        user_input = prompt_for_int(prompt_string)
        for operation in operations:
            if operation[1] == user_input:
                return operations[0].uper()
        else:
            print(user_input, "is not a valid input")

def create_basic_upg():
    data = {
        "upgradeName": basic_upgrade[0],
        "valueToModify": prompt_for_vtm(basic_upgrade[1]),
        "operation": prompt_for_operation("Which operation would you like this upgrade to utilize? "),
        "modifier": prompt_for_float("Enter the modifier for your " + basic_upgrade[1] + ": ")
    }


    return data



def create_bundled_upg():
    bundle = {
        "upgradeName": bundled_upg[0],
        "upgStrat1": prompt_for_upg_type("upgrade 1")
    }

    if bundle["upgStrat1"] == "null":
        del bundle["upgStrat1"]
        return bundle

    bundle["upgStrat2"] = prompt_for_upg_type("upgrade 2")
    if bundle["upgStrat2"] == "null":
        del bundle["upgStrat2"]
        return bundle

    bundle["upgStrat3"] = prompt_for_upg_type("upgrade 3")
    if bundle["upgStrat3"] == "null":
        del bundle["upgStrat3"]
        return bundle

    bundle["upgStrat4"] = prompt_for_upg_type("upgrade 4")

    if bundle["upgStrat4"] == "null":
        del bundle["upgStrat4"]

    return bundle


VALUE = StringIntPair("VALUE", 0, '')
UPGRADE_COUNT = StringIntPair("UPGRADE_COUNT", 1, '')
TEMPERATURE = StringIntPair("TEMPERATURE", 2, '')
MULTIORE = StringIntPair("MULTIORE", 3, '')
comparison_fields = [VALUE, UPGRADE_COUNT, TEMPERATURE, MULTIORE]


def prompt_for_condition():
    while True:
        print()
        for field in comparison_fields:
            print(field.associated_value, field.name, field.description)
        user_input = prompt_for_int("Which condition would do you want to evaluate? ")
        for condition in comparison_fields:
            if user_input == condition.associated_value:
                return condition.name
        print(user_input, "is not a valid input for condition")


GREATER_THAN = StringIntPair("GREATER_THAN", 0, '')
EQUAL_TO = StringIntPair("EQUAL_TO", 1, '')
LESS_THAN = StringIntPair("LESS_THAN", 2, '')

comparison_types = [GREATER_THAN, EQUAL_TO, LESS_THAN]


def prompt_for_comparison():
    while True:
        print()
        for comparison in comparison_types:
            print(comparison.associated_value, comparison.name, comparison.description)
        user_input = prompt_for_int("Which type of comparison would you like? ")
        for comparison in comparison_types:
            if user_input == comparison.associated_value:
                return comparison.name
        print(user_input, "is not a valid input")


def create_conditional_upg():
    bundle = {
        "upgradeName": conditional_upg[0],
        "condition": prompt_for_condition(),
        "comparison": prompt_for_comparison(),
        "threshold": prompt_for_float("Threshold of the comparison:"),
        "ifModifier": prompt_for_upg_type("true upgrade"),
        "elseModifier": prompt_for_upg_type("false upgrade")
    }
    return bundle


def create_resetter_upg():
    bundle = {
        "upgradeName": resetter_upg[0]
    }

    return bundle


value = ("Value", 0, "VALUE")
temperature = ("Temperature", 1, "TEMPERATURE")
multiore = ("Multiore", 2, "MULTIORE")
upgrade_count = ("Upgrade Count", 3, "UPGRADE_COUNT")
active_ore = ("Active Ore", 4, "ACTIVE_ORE")
placed_items = ("Placed Items", 5, "PLACED_ITEMS")
special_points = ("Special Points", 6, "SPECIAL_POINTS")
wallet = ("Wallet", 7, "WALLET")
prestige_level = ("Prestige Level", 8, "PRESTIGE_LEVEL")
values_of_influence = [value, temperature, multiore, upgrade_count, active_ore, placed_items, special_points, wallet, prestige_level]

# prompt for value of influence
def prompt_for_VOI():
    while True:
        for voi in values_of_influence:
            print(voi[1], "-", voi[0])
        user_input = prompt_for_int("Which value would you like to influence the modifier of this upgrade? ")
        for voi in values_of_influence:
            if user_input == voi[1]:
                return voi[3]
        print(user_input, "is not a valid input")

def optional_prompt(prompt_string1, prompt_string2):
    if prompt_for_float(prompt_string1):
        return prompt_for_float(prompt_string2)
    else:
        return "null"

def create_influenced_upg():
    data = {
        "valueOfInfluence": prompt_for_VOI(),
        "baseUpgrade": create_basic_upg(),
        "operation": prompt_for_operation("How would you like this value of influence to influence/mutate the baseUpgrade?: "),
        "minModifier": optional_prompt("Would you like to set a min modifier? ", "Enter the minimum for the modifier: "), # Should make custom prompt for this and max modifier.
        "maxModifier": optional_prompt("Would you like to set a max modifier? ", "Enter the maximum for the modifier: "),
        "scalar": prompt_for_float("Enter the scalar that is applied: ")
    }

    if data["minModifier"] == "null":
        del data["minModifier"]

    if data["maxModifier"] == "null":
        del data["maxModifier"]

    return data
