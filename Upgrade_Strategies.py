#!/usr/bin/env python3
# @author Nathan Ulmen
from Helper_Functions import prompt_for_int, prompt_for_vtm, prompt_for_float, StringIntPair

AddUPG = StringIntPair('AddUPG', 1, "\tWill add the modifier to the specified valueToModify.")
MultiplyUPG = StringIntPair('MultiplyUPG', 2, "\tWill multiply the value to modify by the modifier.")
SubtractUPG = StringIntPair('SubtractUPG', 3, "\tWill subtract the modifier from the specified valueToModify.")

BundledUPG = StringIntPair('BundledUPG', 4," \tSelect to bundle up different types of upgrades. EX: you want an upgrader that multiplies ore value and substracts ore Temperature.")
ConditionalUPG = StringIntPair('ConditionalUPG', 5,"\tA conditional upgrade. Will on type of upgrade if the condidition is true and an else upgrade if condition is false.")
InfluencedUPG = StringIntPair('InfluencedUPG', 6, "\tModifier is inluenced/determined by another factor.")

ResetterUPG = StringIntPair('ResetterUPG', 7,"\tResets the upgrade tags of ore. Make sure to tag or as ressetter if you want it to be balanced!")

# These will require oreStrategy creation to be implemented:
# ApplyEffectUPG = StringIntPair('ApplyEffect', 8, "\tApplies an effect to the ore.")
# TargetedCleanser = StringIntPair('TargetedCleanser', 9, " \tRemoves an effect from the ore.")

# UPGS = [AddUPG, MultiplyUPG, SubtractUPG, BundledUPG, ConditionalUPG, InfluencedUPG, ResetterUPG, ApplyEffectUPG]
upgrades = [AddUPG, MultiplyUPG, SubtractUPG, BundledUPG, ConditionalUPG, ResetterUPG]


def prompt_for_upg_type(strat):
    data = {

    }
    while True:
        print()
        for upg in upgrades:
            print(upg.associated_value, upg.name, upg.description)
        print("Enter 0 if you want dont want to add an upgrade. ")
        user_input = prompt_for_int("What type of Upgrade would you like " + strat + " to be? ")
        if user_input == 0:
            return "null"
        for upg in upgrades:
            if user_input == upg.associated_value:
                if upg.name in [AddUPG.name, MultiplyUPG.name, SubtractUPG.name]:
                    return create_basic_upg(data, upg.name)
                elif upg.name == BundledUPG.name:
                    return create_bundled_upg()
                elif upg.name == ResetterUPG.name:
                    bundle = {"type": ResetterUPG.name}
                    return bundle
                elif upg.name == ConditionalUPG.name:
                    return create_conditional_upg()
        print(user_input, " is not a valid Upgrade")


def create_basic_upg(data, basic_upg_type):
    data = {
        "type": basic_upg_type,
        "valueToModify": prompt_for_vtm(basic_upg_type),
        "modifier": prompt_for_float("Enter the modifier for your " + basic_upg_type + ": "),
    }
    return data


def create_bundled_upg():
    bundle = {
        "type": "BundledUPG",
        "upgStrat1": prompt_for_upg_type("upgrade 1")
            # "type": prompt_for_upg_type("upgrade 1")
    }

    if bundle["upgStrat1"] == "null":
        # del bundle["upgStrat1"]["type"]
        del bundle["upgStrat1"]
        return bundle

    bundle["upgStrat2"] = prompt_for_upg_type("upgrade 2")
        # "type": prompt_for_upg_type("upgrade 2")
        # prompt_for_upg_type("upgrade 2")


    if bundle["upgStrat2"]== "null":
        # del bundle["upgStrat2"]["type"]
        del bundle["upgStrat2"]
        return bundle

    bundle["upgStrat3"] = prompt_for_upg_type("upgrade 3")
        # "type": prompt_for_upg_type("upgrade 3")




    if bundle["upgStrat3"]== "null":
        # del bundle["upgStrat3"]["type"]
        del bundle["upgStrat3"]
        return bundle

    bundle["upgStrat4"] = prompt_for_upg_type("upgrade 4")

    if bundle["upgStrat4"] == "null":
        # del bundle["upgStrat4"]["type"]
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
        user_input = prompt_for_int("Which condition would do you want to evaluate?")
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
        user_input = prompt_for_int("Which type of comparison would you like")
        for comparison in comparison_types:
            if user_input == comparison.associated_value:
                return comparison.name
        print(user_input, "is not a valid input")


def create_conditional_upg():
    bundle = {
        "type": ConditionalUPG.name,
        "condition": prompt_for_condition(),
        "comparison": prompt_for_comparison(),
        "threshold": prompt_for_float("Threshold of the comparison:"),
        "ifModifier": prompt_for_upg_type("true upgrade"),
        "elseModifier": prompt_for_upg_type("false upgrade")
    }
    return bundle

def create_resetter_upg():
    bundle = {
        "type": ResetterUPG.name
    }

    return bundle
