# Line 1
# @author Nathan Ulmen


from Helper_Functions import prompt_for_tier, prompt_for_string, \
    prompt_for_float, prompt_for_int, Color, prompt_for_boolean


def create_dropper():
    print("You are now creating a " + Color.BOLD + Color.UNDERLINE + "Dropper" + Color.END)

    item_type = "Dropper"

    dropper_data = {
        "name": prompt_for_string("Enter the name of the Dropper: "),
        "description": prompt_for_string("Enter the Dropper's description: "),
        # "blockLayout": [
        #     [0, 3, 0],
        #     [0, 0, 0],
        #     [0, 0, 0]
        # ],
        "tier": prompt_for_tier(item_type),
        "isShopItem": prompt_for_boolean("Is the Dropper bought with Cash? "),
        "itemValue": prompt_for_float("Enter the Dropper's value/price: "),
        "oreName": prompt_for_string("Enter the name of the ore that the dropper will produce: "),
        "oreValue": prompt_for_float("Enter the value of the ore that the dropper will produce: "),
        "oreTemp": prompt_for_int("Enter an integer value that for the temperature of the ore that the dropper will produce: "),
        "multiOre": prompt_for_int("Enter an integer value for the Multi-Ore property of the ore that the dropper will produce: "),
        "dropInterval": prompt_for_float("Enter the drop interval(in seconds) of the dropper: "),
        # "oreStrategy": {
        #     "strategyType": null,
        # },
    }

    return dropper_data
