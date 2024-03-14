#!/usr/bin/env python3
# @author Nathan Ulmen


from Helper_Functions import prompt_for_string, prompt_for_tier, prompt_for_float, prompt_for_int, Color, \
    prompt_for_boolean
from Upgrade_Strategies import prompt_for_upg_type


def create_furnace():
    print("You are now creating a " + Color.BOLD + Color.UNDERLINE + "Furnace" + Color.END)

    furnace_data = {
        "name": prompt_for_string("Enter the Furnace's name: "),
        "description": prompt_for_string("Enter the Furnace's description: "),
        # "blockLayout": [
        #   [4, 4],
        #   [4, 4]
        # ],
        "tier": prompt_for_tier("Furnace"),
        "isShopItem": prompt_for_boolean("Is the Furnace bought with Cash? "),
        "itemValue": prompt_for_float("Enter the Furnace's price/value (0 is recommended if the item isn't bought with cash): "),
        "specialPointReward": prompt_for_int("Enter the Furnace's special point reward: "),
        "rewardThreshold": prompt_for_int("Enter the Furnace's special point reward threshold: "),
        "upgrade": prompt_for_upg_type("Enter the Furnace's process effect: ")
    }

    return furnace_data


