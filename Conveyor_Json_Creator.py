# @author Nathan Ulmen
from Helper_Functions import prompt_for_tier, prompt_for_string, \
    prompt_for_float, Color, prompt_for_boolean


def create_conveyor():
    print("You are now creating a " + Color.BOLD + Color.UNDERLINE + "Conveyor" + Color.END)

    item_type = "Conveyor"

    conveyor_data = {
        "name": prompt_for_string("Enter the name of the Conveyor: "),
        "description": prompt_for_string("Enter the Conveyor's description: "),
        # "blockLayout": [
        #     [1,1],
        #     [1,1]
        # ],
        "tier": prompt_for_tier(item_type),
        "isShopItem": prompt_for_boolean("Is the Conveyor bought with Cash? "),
        "itemValue": prompt_for_float("Enter the Conveyor's price/value (0 is recommended if the item isn't bought "
                                      "with cash): "),
        "conveyorSpeed": prompt_for_float("Enter the speed of the Conveyor, the default/base speed is 1: ")
    }

    return conveyor_data
