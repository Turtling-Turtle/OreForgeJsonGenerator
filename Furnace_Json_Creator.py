# @author Nathan Ulmen

import json

from Helper_Functions import prompt_for_string, prompt_for_tier, prompt_for_float, prompt_for_int, color
from Upgrade_Strategies import prompt_for_upg_type

print(color.UNDERLINE + color.BOLD + "Welcome, you are creating a Furnace." + color.END)

furnace_data = {
    "name": prompt_for_string("Enter the Furnace's name: "),
    "description": prompt_for_string("Enter the Furnace's description: "),
    # "blockLayout": [
    #   [4, 4],
    #   [4, 4]
    # ],
    "tier": prompt_for_tier("Furnace"),
    "itemValue": prompt_for_float("Enter the Furnace's price/value: "),
    "specialPointReward": prompt_for_int("Enter the Furnace's special point reward: "),
    "rewardThreshold": prompt_for_int("Enter the Furnace's reward threshold: "),
    "upgrade": {
      "type": prompt_for_upg_type("furnace"),
    },
}

json_data = json.dumps(furnace_data, indent=4)

print(json_data)

#Prints to Text file.
# with open("FurnaceAsJson.txt", "w") as file:
#     json.dump(furnace_data, file, indent=4)

