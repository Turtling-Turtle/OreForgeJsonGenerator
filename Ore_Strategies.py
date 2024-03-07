# @author Nathan Ulmen
from Helper_Functions import prompt_for_int
from Upgrade_Strategies import Strategy

BundledEffect = Strategy("BundledEffect", 0)
Inflamed = Strategy("Inflamed", 1)
FrostBite = Strategy("FrostBite", 2)
## Can add more strategies once I create them in the actual project. Currently, these are all I have.

effects = [BundledEffect, Inflamed, FrostBite]
def prompt_for_strategy():
    while True:
        print()
        for element in effects:
            print(element.associated_value, element.name)
        user_input = prompt_for_int("Which type of effect do you want? ")
        for element in effects:
            if user_input == element.associated_value:
                #Logic for creating that effect/strategy;
                #create_ore_strategy()
                return element.name
        print(user_input, " is an invalid input")
