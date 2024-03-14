#!/usr/bin/env python3
# @author Nathan Ulmen
from Helper_Functions import prompt_for_int, prompt_for_float
from Upgrade_Strategies import StringIntPair

BundledEffect = StringIntPair("BundledEffect", 0, '')
Inflamed = StringIntPair("Inflamed", 1, '')
FrostBite = StringIntPair("FrostBite", 2, '')
## Can add more strategies once I create them in the actual project. Currently, these are all I have.

effects = [BundledEffect, Inflamed, FrostBite]


def prompt_for_ore_strategy():
    while True:
        print()
        for element in effects:
            print(element.associated_value, element.name)
        user_input = prompt_for_int("Which type of effect do you want? ")
        for element in effects:
            if user_input == element.associated_value:
                if element.name == BundledEffect.name:
                    return create_bundled_effect()
                elif element.name == Inflamed.name or FrostBite.name:
                    return create_basic_strategy(element.name)
        print(user_input, " is an invalid input")


def create_bundled_effect():
    bundle = {
        "type": BundledEffect.name,
        "oreStrat1": prompt_for_ore_strategy(),
    }

    if bundle["oreStrat1"] == "null":
        del bundle["oreStrat1"]
        return bundle

    bundle["oreStrat2"] = prompt_for_ore_strategy()
    if bundle["oreStrat2"] == "null":
        del bundle["upgStrat2"]
        return bundle

    bundle["oreStrat3"] = prompt_for_ore_strategy()
    if bundle["oreStrat3"] == "null":
        del bundle["oreStrat3"]
        return bundle

    bundle["oreStrat4"] = prompt_for_ore_strategy()
    if bundle["oreStrat4"] == "null":
        del bundle["oreStrat4"]

    return bundle


def create_basic_strategy(effect_name):
    data = {
        "type": effect_name,
        "duration": prompt_for_float("How long would you like this effect to last? "),
        "tempChange": prompt_for_float("How much would you like the temp to change every second? ")
    }

    return data
