# @author Nathan Ulmen

import json

from Helper_Functions import  prompt_for_tier, prompt_for_string, \
    prompt_for_float, prompt_for_int

item_type = "Dropper"
name = prompt_for_string("Enter the name of the Dropper: ")
description = prompt_for_string("Enter the Dropper's description: ")
tier = prompt_for_tier(item_type)
value = prompt_for_float("Enter the Dropper's value/price: ")


ore_name = prompt_for_string("Enter the name of the ore produced: ")
ore_price = prompt_for_float("Enter the value of the ore produced: ")
ore_temperature = prompt_for_int("Enter an integer of temperature of the ore produced: ")
multi_ore = prompt_for_int("Enter an integer for multiOre property of the ore produced: ")
drop_interval = prompt_for_float("Enter the drop interval of the Dropper: ")

dropper_data = {
    "name": name,
    "description": description,
    # "blockLayout": [
    #     [0,3,0],
    #     [0,0,0],
    #     [0,0,0]
    # ],
    "tier": tier,
    "itemValue": value,
    "oreName": ore_name,
    "oreValue": ore_price,
    "oreTemp": ore_temperature,
    "multiOre": multi_ore,
    "dropInterval": drop_interval,
    # "oreStrategy": {
    #     "strategyType": null
}

json_data = json.dumps(dropper_data, indent=4)

print(json_data)