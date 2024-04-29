import random

from Helper_Functions import Color, prompt_for_string, prompt_for_tier, prompt_for_boolean, prompt_for_float, \
    prompt_for_int
from CLI.Upgrade_Strategies import prompt_for_upg_type


# @author Nathan Ulmen

def common_attributes(item_type):
    common_data = {
        "name": prompt_for_string("Enter the " + item_type + "'s name: "),
        "id": generate_item_id(),
        "description": prompt_for_string("Enter the" + item_type + "'s description: "),
        "tier": prompt_for_tier(item_type),
        "isShopItem": prompt_for_boolean("Is this " + item_type + " bought with cash? "),
        "itemValue": prompt_for_float(
            "Enter the " + item_type + "'s value/price ( 0 is recommended if the item isn't bought with cash) ")
    }

    return common_data


def generate_item_id():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    nums = "0123456789"
    item_id = ""
    for i in range(3):
        item_id += nums[random.randint(0, len(nums) - 1)]
    item_id += "-"
    for i in range(8):
        item_id += chars[random.randint(0, len(chars) - 1)]
    return item_id


def create_furnace():
    print("You are now creating a " + Color.BOLD + Color.UNDERLINE + "Furnace" + Color.END)
    furnace_data = common_attributes("Furnace")
    furnace_data.update({
        "blockLayout": [
            [4, 4],
            [4, 4]
        ],
        "specialPointReward": prompt_for_int("Enter the Furnace's special point reward: "),
        "rewardThreshold": prompt_for_int("Enter the Furnace's special point reward threshold: "),
        "upgrade": prompt_for_upg_type("Enter the Furnace's process effect: ", False)
    })

    return furnace_data


def create_upgrader():
    print("You are now creating a " + Color.BOLD + Color.UNDERLINE + "Upgrader" + Color.END)
    upgrader_data = common_attributes("Upgrader")
    upgrader_data.update({
        "blockLayout": [
            [2, 2],
            [1, 1]
        ],
        "conveyorSpeed": prompt_for_float("Enter the Upgraders conveyor speed: "),
        "upgrade": prompt_for_upg_type("the primary upgrade ", False),
        "upgradeTag": {
            "name": upgrader_data.get("name"),
            "id": upgrader_data.get("id"),
            "maxUpgrades": prompt_for_int(
                "Enter the maximum number of times you want this upgrade to apply to an ore before the ore needs to be reset: "),
            "isResetter": prompt_for_boolean(
                "Does this Upgrader reset Ore? (Should select yes if you selected ResetterUPG as one of the upgrades): ")
        },
    })

    return upgrader_data


def create_dropper():
    print("You are now creating a " + Color.BOLD + Color.UNDERLINE + "Dropper" + Color.END)
    dropper_data = common_attributes("Dropper")
    dropper_data.update({
        "blockLayout": [
            [0, 3, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
        "oreName": prompt_for_string("Enter the name of the ore that the dropper will produce: "),
        "oreValue": prompt_for_float("Enter the value of the ore that the dropper will produce: "),
        "oreTemp": prompt_for_int(
            "Enter an integer value that for the temperature of the ore that the dropper will produce: "),
        "multiOre": prompt_for_int(
            "Enter an integer value for the Multi-Ore property of the ore that the dropper will produce: "),
        "dropInterval": prompt_for_float("Enter the drop interval(in seconds) of the dropper: "),
        # "oreStrategy": create_ore_strategy(),
    })

    return dropper_data


def create_conveyor():
    print("You are now creating a " + Color.BOLD + Color.UNDERLINE + "Conveyor" + Color.END)
    conveyor_data = common_attributes("Conveyor")
    conveyor_data.update({
        "blockLayout": [
            [1, 1],
            [1, 1]
        ],
        "conveyorSpeed": prompt_for_float("Enter the speed of the Conveyor, the default/base speed is 1: ")
    })

    return conveyor_data
