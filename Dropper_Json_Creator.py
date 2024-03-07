# Line 1
# @author Nathan Ulmen

import json

from Helper_Functions import prompt_for_tier, prompt_for_string, \
    prompt_for_float, prompt_for_int

print("Welcome, you are creating a Dropper. Enter teh values to print the created Dropper in json.")

item_type = "Dropper"

dropper_data = {
    "name": prompt_for_string("Enter the name of the Dropper: "),
    "description": prompt_for_string("Enter the Dropper's description: "),
    # "blockLayout": [
    #     [0,3,0],
    #     [0,0,0],
    #     [0,0,0]
    # ],
    "tier": prompt_for_tier(item_type),
    "itemValue": prompt_for_float("Enter the Dropper's value/price: "),
    "oreName": prompt_for_string("Enter the name of the ore produced: "),
    "oreValue": prompt_for_float("Enter the value of the ore produced: "),
    "oreTemp": prompt_for_int("Enter an integer value that you want to represent produced ore's temperature: "),
    "multiOre": prompt_for_int("Enter an integer for multiOre property of the ore produced: "),
    "dropInterval": prompt_for_float("Enter the drop interval of the Dropper: "),
    # "oreStrategy": {
    #     "strategyType": null,
    # }
}

json_data = json.dumps(dropper_data, indent=4)

print(json_data)
# Prints to Text file.
# with open("DrpperAsJson.txt", "w") as file:
#     json.dump(dropper_data, file, indent=4)Prints to Text file.
