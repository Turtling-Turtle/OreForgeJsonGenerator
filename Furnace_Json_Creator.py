# @author Nathan Ulmen

import json
import Helper_Functions

# Commented out fields are very complex/difficult to handle, would need more time to finish.

furnace_data = {
    "name": Helper_Functions.prompt_for_string("Enter the Furnace's name: "),
    "description": Helper_Functions.prompt_for_string("Enter the Furnace's description: "),
    # "blockLayout": [
    #   [4, 4],
    #   [4, 4]
    # ],
    "tier": Helper_Functions.prompt_for_tier("Furnace"),
    "itemValue": Helper_Functions.prompt_for_float("Enter the Furnace's price/value: "),
    # "upgrade": {
    #   "type": "AddUPG",
    #   "modifier": 2.0,
    #   "ValueToModify": "ORE_VALUE"
    # },
    "specialPointReward": Helper_Functions.prompt_for_int("Enter the Furnace's special point reward: "),
    "rewardThreshold": Helper_Functions.prompt_for_int("Enter the Furnace's reward threshold: ")
}

json_data = json.dumps(furnace_data, indent=4)

print(json_data)
