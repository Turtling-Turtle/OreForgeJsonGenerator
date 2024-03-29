#!/usr/bin/env python3
# @author Nathan Ulmen

import json

from Conveyor_Json_Creator import create_conveyor
from Dropper_Json_Creator import create_dropper
from Furnace_Json_Creator import create_furnace
from Helper_Functions import prompt_for_boolean, Color, list_prompt
from Upgrader_Json_Creator import create_upgrader


dropper = (1, "Dropper", "Produces Ore.", '')
furnace = (2, "Furnace", "Sells Ore.", '')
upgrader = (3, "Upgrader", "Upgrades Ore.", '')
conveyor = (4, "Conveyor", "Moves Ore.", '')
items = [dropper, furnace, upgrader, conveyor]



# json.dumps() is used to print to console. Prints in json form.
# json.dump() is used to write to file. Prints in json form.

# Drives the program
def main():
    data = []
    while True:
        print("0 - " + Color.BOLD + "Quit Item Creation" + Color.END)
        user_input = list_prompt(items, "Which type of Item would you like to create? ", True)

        if user_input == 0:
            if len(data) != 0:
                if prompt_for_boolean("Would you like to print the data to a file? "):
                    if prompt_for_boolean("Would you like to overwrite the existing file? "):
                        with open("ItemAsJson.txt", "w") as file:
                            json.dump(data, file, indent=4)  # Overwrites File
                    else:
                        with open("ItemAsJson.txt", "a") as file:
                            json.dump(data, file, indent=4)  # Appends to file
            quit()
        elif user_input == dropper:  # I wish python supported switch statements
            created_dropper = create_dropper()
            print(json.dumps(created_dropper, indent=4))
            data.append(created_dropper)
        elif user_input == furnace:
            created_furnace = create_furnace()
            print(json.dumps(created_furnace, indent=4))
            data.append(created_furnace)
        elif user_input == upgrader:
            created_upgrader = create_upgrader()
            print(json.dumps(created_upgrader, indent=4))
            data.append(created_upgrader)
        elif user_input == conveyor:
            created_conveyor = create_conveyor()
            print(json.dumps(created_conveyor, indent=4))
            data.append(created_conveyor)
        print("Item Created")
        if prompt_for_boolean("Would you like to quit Item Creation?"):
            if prompt_for_boolean("Would you like to print the data to a file?"):
                if prompt_for_boolean("Would you like to overwrite the existing file?"):
                    with open("ItemAsJson.txt", "w") as file:
                        json.dump(data, file, indent=4)  # Overwrites File
                else:
                    with open("ItemAsJson.txt", "a") as file:
                        json.dump(data, file, indent=4)  # Appends to Text file.
                quit()
            quit()


main()
