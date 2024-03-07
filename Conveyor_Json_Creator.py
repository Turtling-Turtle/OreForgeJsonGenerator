# @author Nathan Ulmen
import json
import re
from Helper_Functions import prompt_for_tier, prompt_for_string, \
    prompt_for_float

print("Welcome, you are creating a Conveyor. Enter the values to print the Conveyor in in Json.")


# might not need this...
# def determine_item_type():
#     isValid = False
#     while not isValid:
#         print('0 - Conveyor')
#         print('1 - Mine')
#         print('2 - Furnace')
#         print('3 - Upgrader')
#         input_type = input("Enter the type of item you would like to create")
#     try:
#         input_type = int(input_type)
#         if input_type in range(0,3):
#             isValid = True
#             if input_type == 0: #wish that python had switch statements 😔
#                 create_conveyor()
#             elif input_type == 1:
#                 create_mine()
#             elif input_type == 2:
#                 create_furnace()
#             elif input_type == 3:
#                 create_upgrader()
#         else:
#             print("Invalid Input")
#     except ValueError:
#         print("Invalid Input")


item_type = "Conveyor"

name = prompt_for_string("Enter the name of the Conveyor: ")
description = prompt_for_string("Enter the Conveyor's description: ")
tier = prompt_for_tier(item_type)
value = prompt_for_float("Enter the value/price of the Conveyor: ")


conveyor_data = {
    "name": name,
    "description": description,
    # "blockLayout": [
    #     [1,1],
    #     [1,1]
    # ],
    "tier": tier,
    "itemValue": value,
    "conveyorSpeed": prompt_for_float("Enter the speed of the Conveyor, the default/base speed is 1: ")
}

json_data = json.dumps(conveyor_data, indent=4)

print(json_data)
