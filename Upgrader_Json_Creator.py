#Line 1
#@author Nathan Ulmen
import json
from Helper_Functions import prompt_for_string, prompt_for_tier, prompt_for_float, prompt_for_boolean
from Upgrade_Strategies import prompt_for_upg_type

def create_upgrader():
    print("Welcome, you are creating a new Upgrader. Enter the values to print the Upgrader to Json.")

    name = prompt_for_string("Enter the Upgrader's name: ")
    upgrader_data = {
        "name": name,
        "description": prompt_for_string("Enter the Upgraders description: "),
        # "blockLayout": [
        #     [0, 1, 1, 0],
        #     [0, 2, 2, 0],
        #     [0, 1, 1, 0]
        # ],
        "tier": prompt_for_tier("Upgrader"),
        "isShopItem": prompt_for_boolean("Is the Upgrader a bought with Cash? "),
        "itemValue": prompt_for_float("Enter the Upgraders value/price: "),
        "conveyorSpeed": prompt_for_float("Enter the Upgraders conveyor speed: "),
        "upgrade": {
            "type": prompt_for_upg_type("the primary upgrade"),
        },
        "upgradeTag": {
            "name": name,
            "maxUpgrades": 1,
            "isResetter": prompt_for_boolean("Does this Upgrader reset Ore? (Should only be true if you selected ResetterUPG) ")
        }
    },

    return upgrader_data


#Example Upgraders in Json form:
# [
#     {
#     "name": "Renewal Forge",
#     "description": "The Renewal Forge is a mystical apparatus forged by ancient artisans. Upgraded ore have their upgrade tags reset and value increased by 10% of their upgrade count.",
#     "blockLayout": [
#       [1, 1],
#       [1, 1]
#     ],
#     "tier": "PRESTIGE",
#     "itemValue": 0.0,
#     "conveyorSpeed" : 1.0,
#     "upgrade": {
#       "type": "BundledUPG",
#       "upgStrat1": {
#         "type": "ResetterUPG"
#       },
#       "upgStrat2": {
#         "type": "InfluencedUPG",
#         "modifier": 0.1,
#         "ValueToModify": "ORE_VALUE",
#         "ValueOfInfluence": "UPGRADE_COUNT"
#       },
#       "upgStrat3": {
#         "type": null
#       },
#       "upgStrat4": {
#         "type": null
#       }
#     },
#     "upgradeTag": {
#       "name": "Renewal Forge",
#       "maxUpgrades": 1,
#       "isResetter": true
#     }
#   },
#   {
#     "name": "Basic Upgrader",
#     "description": "A simple upgrader with a simple effect.",
#     "blockLayout": [
#       [0, 0, 0],
#       [0, 2, 0],
#       [0, 0, 0]
#     ],
#     "tier": "COMMON",
#     "itemValue": 50.0,
#     "conveyorSpeed" : 1.0,
#     "upgrade": {
#       "type": "AddUPG",
#       "modifier": 4.0,
#       "ValueToModify": "ORE_VALUE"
#     },
#     "upgradeTag": {
#       "name": "Basic Upgrader",
#       "maxUpgrades": 5,
#       "isResetter": false
#     }
#   },
#   {
#     "name": "Searing Winds",
#     "description": "Ore is touched by winds so hot it's lit ablaze.",
#     "blockLayout": [
#       [0, 0, 0],
#       [0, 2, 0],
#       [0, 0, 0]
#     ],
#     "tier": "PRESTIGE",
#     "itemValue": 0,
#     "conveyorSpeed" : 5.0,
#     "upgrade": {
#      "type": "BundledUPG",
#       "upgStrat1": {
#         "type": "ConditionalUPG",
#         "ifModifier": {
#           "type": "MultiplyUPG",
#           "valueToModify": "ORE_VALUE",
#           "modifier": 6.0
#         },
#         "elseModifier": {
#           "type": "AddUPG",
#           "valueToModify": "MULTIORE",
#           "modifier": 4.0
#         },
#         "condition": "MULTIORE",
#         "comparison": "LESS_THAN",
#         "threshold": 1.0
#       },
#         "upgStrat2": {
#           "type": "ApplyEffect",
#             "strategyType": "Inflamed",
#             "duration": 8.0,
#             "tempIncrease": 10
#         }
#     },
#     "upgradeTag": {
#       "name": "Searing Winds",
#       "maxUpgrades": 1,
#       "isResetter": false
#     }
#   }
#
# ]

