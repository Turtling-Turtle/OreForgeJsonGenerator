# @author Nathan Ulmen
from Helper_Functions import prompt_for_tier, prompt_for_string, \
    prompt_for_float


def create_conveyor():
    print("Welcome, you are creating a Conveyor. Enter the values to print the Conveyor in in Json.")

    item_type = "Conveyor"

    conveyor_data = {
        "name": prompt_for_string("Enter the name of the Conveyor: "),
        "description": prompt_for_string("Enter the Conveyor's description: "),
        # "blockLayout": [
        #     [1,1],
        #     [1,1]
        # ],
        "tier": prompt_for_tier(item_type),
        "itemValue": prompt_for_float("Enter the value/price of the Conveyor: "),
        "conveyorSpeed": prompt_for_float("Enter the speed of the Conveyor, the default/base speed is 1: ")
    }

    return conveyor_data
