import json
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QVBoxLayout, \
    QHBoxLayout, QPushButton, QMessageBox, QCheckBox

import StrategyChoice
from StrategyChoice import upgradeStrategies
from CLI.Item_Constructors import generate_item_id
from StrategyChoice import StrategyChoiceField
from GUI_Upgrade_Strategies import Color
from CustomWidgets import InputField, DropDownMenu, OptionalField, JsonSerializable

# Tiers
pinnacle = (Color.RED + "Pinnacle" + Color.END + "-TEMP DESCRIPTION- THE RAREST", "PINNACLE")
special = (Color.ORANGE + "Special" + Color.END + "-TEMP DESCRIPTION- 2nd RAREST", "SPECIAL")
exotic = (Color.YELLOW + "Exotic" + Color.END + "-TEMP DESCRIPTION - 3rd RAREST", "EXOTIC")
prestige = (Color.CYAN + "Prestige" + Color.END + "-TEMP DESCRIPTION -4 RAREST", "PRESTIGE")
epic = (Color.PURPLE + "Epic" + Color.END + "-TEMP DESCRIPTION -5th RAREST", "EPIC")
superRare = (Color.DARKCYAN + "Super Rare" + Color.END + "-TEMP DESCRIPTION -6th RAREST", "SUPER_RARE")
rare = (Color.BLUE + "Rare" + Color.END + " - TEMP DESCRIPTION - 7th RAREST", "RARE")
uncommon = (Color.GREEN + "Uncommon" + Color.END + "- TEMP DESCRIPTION - 8th RAREST", "UNCOMMON")
common = ("Common - TEMP DESCRIPTION - 9th RAREST", "COMMON")
tiers = [pinnacle, special, exotic, prestige, epic, superRare, rare, uncommon, common]


# @author Nathan Ulmen

def bold_string(text_to_bold: str):
    return "<b>" + text_to_bold + "</b>"


def underline_string(text_to_underline: str):
    return "<u>" + text_to_underline + "</u>"


class ItemCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ore Forge Item Creator")
        # self.setFixedSize(800, 250)
        # self.setWindowIcon(QIcon("icon.png"))
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.essentials_hbox = QHBoxLayout()
        self.generate_button = QPushButton("Generate Item")

        # ComboBox to choose item type
        item_type_label = QLabel(bold_string("Item Type:"))
        # layout.addWidget(self.iem_type_label)
        # self.item_type_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.essentials_hbox.addWidget(item_type_label)

        self.item_type_combo = QComboBox()
        self.item_type_combo.addItem("Dropper")
        self.item_type_combo.addItem("Furnace")
        self.item_type_combo.addItem("Upgrader")
        self.item_type_combo.addItem("Conveyor")
        # layout.addWidget(self.item_type_combo)
        self.essentials_hbox.addWidget(self.item_type_combo, Qt.AlignmentFlag.AlignLeft)

        self.essentials_hbox.addWidget(self.generate_button, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.item_type_combo.currentIndexChanged.connect(self.onItemTypeChange)

        # Print button:

        # Grid layout for item attributes
        self.layout.addLayout(self.essentials_hbox)
        self.essentials_hbox.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.createCommonUI()

        self.generate_button.clicked.connect(
            lambda: self.printJsonData())  #https://stackoverflow.com/questions/40982518/argument-1-has-unexpected-type-nonetype
        self.onItemTypeChange()
        self.show()

    def onItemTypeChange(self):
        text = self.item_type_combo.currentText()
        self.clearLayout()
        self.createCommonUI()
        if text == "Dropper":
            self.createDropperUI()
        elif text == "Furnace":
            self.createFurnaceUI()
        elif text == "Upgrader":
            self.createUpgraderUI()
        elif text == "Conveyor":
            self.createConveyorUI()

    def clearLayout(self):
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            widget = item.widget()
            self.layout.removeWidget(widget)
            if widget is not None:
                widget.deleteLater()

    def createCommonUI(self):
        self.name = InputField("Name:", label_tip="Name of the Item", edit_tip="Name of the Item")
        self.layout.addWidget(self.name)

        self.id = generate_item_id()
        self.id_label = QLabel(bold_string("ID:\t") + self.id)
        self.id_label.setToolTip("The items ID....UNFINISHED")
        self.id_label.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.id_label)

        self.description = InputField("Description:", 14, edit_tip="Description of the Item",
                                      label_tip="Description of the Item")
        self.layout.addWidget(self.description)

        self.tier = DropDownMenu(tiers, "Tier:", label_tip="The Tier of the Item", box_tip="The Tier of the Item")
        self.layout.addWidget(self.tier)

        self.shopItemField = OptionalField(InputField("Item Price", isInteger=True), "Shop Item?", "isShopItem",
                                           "itemValue")
        to_json_implmentation = lambda self: {
            self.booleanJsonKey: self.checkBox.isChecked(),
            # "isShopItem": self.checkBox.isChecked(),
            self.widgetJsonKey: self.customWidget.toJson() if self.checkBox.isChecked() else 0,
        }
        self.shopItemField.setToJson(lambda: to_json_implmentation(self.shopItemField))

        isValidImplementation = lambda self: self.customWidget.isValid() if self.checkBox.isChecked() else None
        self.shopItemField.setIsValid(lambda: isValidImplementation(self.shopItemField))

        self.layout.addWidget(self.shopItemField)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def togglePriceField(self, state):
        if state == 2:
            self.price_field.setEnabled(True)
        else:
            self.price_field.clear()
            self.price_field.setEnabled(False)

    def createDropperUI(self):

        self.oreName = InputField("Ore Name:", label_tip="The Name of the ore.", edit_tip="Name of the ore")
        self.layout.addWidget(self.oreName)

        self.oreValue = InputField("Ore Value:", isFloat=True)
        self.layout.addWidget(self.oreValue)
        self.oreValue.set_both_tips("When an Ore is sold the Ore Value is added to the players' wallet.")

        self.oreTemp = InputField("Ore Temp:", isFloat=True)
        self.layout.addWidget(self.oreTemp)
        self.oreTemp.set_both_tips("The temperature of the ore. 0 represents a neural/default value. Temperature vales "
                                   "that are less than zero indicates that the ore is cold and values greater than 0 indicate that the ore is warm.")

        self.multiore = InputField("Multiore:", isInteger=True)
        self.layout.addWidget(self.multiore)
        self.multiore.set_both_tips("Allows the player to increase the number of ore without needing to drop more ore."
                                    "Functions as a \"multiplier\" for the number of ore.")

        self.dropInterval = InputField("Drop Interval:", isFloat=True)
        self.layout.addWidget(self.dropInterval)
        self.dropInterval.set_both_tips("The interval in seconds in which the dropper produces a new Ore")

        self.strategies = StrategyChoiceField(StrategyChoice.oreEffects, "Ore Effect")
        self.dropperStrategy = OptionalField(self.strategies, "Ore Effect")

        json_behavior = lambda self: self.customWidget.toJson() if self.checkBox.isChecked() else None
        self.dropperStrategy.setToJson(lambda: json_behavior(self.dropperStrategy))

        is_valid_behavior = lambda self: self.customWidget.isValid() if self.checkBox.isChecked() else None
        self.dropperStrategy.setIsValid(lambda: is_valid_behavior(self.dropperStrategy))
        self.layout.addWidget(self.dropperStrategy)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        # oreStrategy

    def createFurnaceUI(self):
        self.pointReward = InputField("Special Point Reward", isInteger=True)
        self.layout.addWidget(self.pointReward)
        self.rewardThreshold = InputField("Special Point Reward Threshold:", isInteger=True)
        self.layout.addWidget(self.rewardThreshold)
        self.strategies = StrategyChoiceField(upgradeStrategies, "Process Effect")
        self.layout.addWidget(self.strategies)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def createUpgraderUI(self):
        self.conveyorSpeed = InputField("Conveyor Speed:", isFloat=True)
        self.maxUpgrades = InputField("Max Upgrades:", isInteger=True)
        self.strategies = StrategyChoiceField(upgradeStrategies, "Upgrade")
        # self.isResetter = OptionalField()
        self.isResetter = QCheckBox("Resets Ore?")
        self.layout.addWidget(self.conveyorSpeed)
        self.layout.addWidget(self.maxUpgrades)
        self.layout.addWidget(self.strategies)
        self.layout.addWidget(self.isResetter)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def createConveyorUI(self):
        self.conveyorSpeed = InputField("Conveyor Speed:", isFloat=True)
        self.layout.addWidget(self.conveyorSpeed)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def validateData(self):
        errorList = []
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, JsonSerializable):
                result = widget.isValid()
                if result is not None:
                    if isinstance(result, list):
                        errors = []
                        for element in result:
                            if element is not None:
                                errors.append(element)
                        errorList.extend(errors)
                    elif result:
                        errorList.append(result)
        return errorList

    def getData(self):
        errorList = self.validateData()
        if len(errorList) == 0:
            item_data = {
                "name": self.name.toJson(),
                "id": self.id,
                "description": self.description.toJson(),
                "tier": self.tier.toJson(),
                # "isShopItem": str(self.shop_checkbox.isChecked()).lower() if self.shop_checkbox is not None else "null",
                # "itemValue": int(self.price_field.text()) if (
                #             self.shop_checkbox.isChecked() and self.price_field is not None) else 0
            }
            item_data.update(self.shopItemField.toJson())
            item_data.update(self.getItemSpecificData())
            return item_data
        else:
            error_box = QMessageBox()
            error_box.setWindowTitle("Validation Error")
            error_box.setIcon(QMessageBox.Icon.Critical)
            error_text = "Data validation failed."
            for error in errorList:
                error_text += "\n" + error
            error_box.setText(error_text)
            error_box.exec()

    def getItemSpecificData(self):
        text = self.item_type_combo.currentText()
        if text == "Dropper":
            return self.getDropperData()
        elif text == "Furnace":
            return self.getFurnaceData()
        elif text == "Upgrader":
            return self.getUpgraderData()
        elif text == "Conveyor":
            return self.getConveyorData()
        else:
            return {}

    def getDropperData(self):
        dropperData = {
            "blockLayout": [
                [0, 3, 0],
                [0, 0, 0],
                [0, 0, 0],
            ],
            "oreName": self.oreName.toJson(),
            "oreValue": self.oreValue.toJson(),
            "oreTemp": self.oreTemp.toJson(),
            "multiOre": self.multiore.toJson(),
            "dropInterval": self.dropInterval.toJson(),
            "oreStrategy": self.dropperStrategy.toJson()
        }
        return dropperData

    def getFurnaceData(self):
        furnaceData = {
            "blockLayout": [
                [4, 4],
                [4, 4],
            ],
            "specialPointReward": self.pointReward.toJson(),
            "rewardThreshold": self.rewardThreshold.toJson(),
            "upgrade": self.strategies.toJson()
        }
        return furnaceData

    def getUpgraderData(self):
        upgraderData = {
            "blockLayout": [
                [2, 2],
                [1, 1]
            ],
            "conveyorSpeed": self.conveyorSpeed.toJson(),
            "upgrade": self.strategies.toJson(),
            "upgradeTag": {
                "name": self.name.toJson(),
                "id": self.id,
                "maxUpgrades": self.maxUpgrades.toJson(),
                "isResetter": True if self.isResetter.isChecked() else False
            }
        }
        return upgraderData

    def getConveyorData(self):
        data = {
            "blockLayout": [
                [1, 1],
                [1, 1]
            ],
            "conveyorSpeed": self.conveyorSpeed.toJson()
        }
        return data

    def printJsonData(self):
        data = self.getData()
        if data is not None:
            json_data = json.dumps(data, indent=4)
            print(json_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ItemCreator()
    win.show()
    sys.exit(app.exec())
