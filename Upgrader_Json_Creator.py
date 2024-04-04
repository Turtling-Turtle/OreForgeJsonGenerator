#!/usr/bin/env python3
# @author Nathan Ulmen
from Helper_Functions import prompt_for_string, prompt_for_tier, prompt_for_float, prompt_for_boolean, Color, \
    prompt_for_int
from Upgrade_Strategies import prompt_for_upg_type


def create_upgrader():
    print("You are now creating a " + Color.BOLD + Color.UNDERLINE + "Upgrader" + Color.END)

    name = prompt_for_string("Enter the Upgraders name: ")
    upgrader_data = {
        "name": name,
        "description": prompt_for_string("Enter the Upgraders description: "),
        "blockLayout": [
            [2, 2],
            [1, 1]
        ],
        "tier": prompt_for_tier("Upgrader"),
        "isShopItem": prompt_for_boolean("Is the Upgrader bought with Cash? "),
        "itemValue": prompt_for_float("Enter the Upgraders price/value (0 is recommended if the item isn't bought with cash): "),
        "conveyorSpeed": prompt_for_float("Enter the Upgraders conveyor speed: "),
        "upgrade": prompt_for_upg_type("the primary upgrade ", False),
        "upgradeTag": {
            "name": name,
            "maxUpgrades": prompt_for_int("Enter the maximum number of times you want this upgrade to apply to an ore before the ore needs to be reset: "),
            "isResetter": prompt_for_boolean("Does this Upgrader reset Ore? (Should select yes if you selected ResetterUPG as one of the upgrades): ")
        },
    }

    return upgrader_data
