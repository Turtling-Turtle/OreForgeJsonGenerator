import json
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QCheckBox, QVBoxLayout, \
    QHBoxLayout, QPushButton, QBoxLayout, QSpacerItem, QSizePolicy
from abc import ABC, abstractmethod

import StrategyChoices


class Color:
    RED = "<font color='red'>"
    ORANGE = "<font color='orange'>"
    YELLOW = "<font color='yellow'>"
    CYAN = "<font color='cyan'>"
    PURPLE = "<font color='purple'>"
    DARKCYAN = "<font color='darkcyan'>"
    BLUE = "<font color='blue'>"
    GREEN = "<font color='green'>"
    END = "</font>"


# Values to Modify
ore_value = ("Ore Value", "ORE_VALUE")
temperature = ("Ore Temperature", "TEMPERATURE")
multiore = ("Multiore", "MULTIORE")
speed = ("Ore Speed", "SPEED")
vtms = [ore_value, temperature, multiore, speed]

# Numeric Operators:
add = ("Add - Adds the modifier to the value to modify.", "ADD")
subtract = ("Subtract - Subtracts the modifier from the value to modify.", "SUBTRACT")
multiply = ("Multiply - Multiplies the value to modify by the modifier.", "MULTIPLY")
divide = ("Divide - Divides the value to modify by the modifier.", "DIVIDE")
exponent = ("Exponent - Raises the value to modify to the power of the modifier.", "EXPONENT")
assignment = ("Assignment - Used to 'set' the value to modify to the value of the modifier.", "ASSIGNMENT")
modulo = ("Modulo - Returns the remainder after two numbers are divided.",
          "MODULO")
numeric_operations = [add, subtract, multiply, divide, exponent, assignment, modulo]

pinnacle = (Color.RED + "Pinnacle" + Color.END + "-TEMP DESCRIPTION- THE RAREST", "PINNACLE")
special = (Color.ORANGE + "Special" + Color.END + "-TEMP DESCRIPTION- 2nd RAREST", "SPECIAL")
exotic = (Color.YELLOW + "Exotic" + Color.END + "-TEMP DESCRIPTION - 3rd RAREST", "EXOTIC")
prestige = (Color.CYAN + "Prestige" + Color.END + "-TEMP DESCRIPTION -4 RAREST", "PRESTIGE")
epic = (Color.PURPLE + "Epic" + Color.END + "-TEMP DESCRIPTION -5th RAREST", "EPIC")
super_rare = (Color.DARKCYAN + "Super Rare" + Color.END + "-TEMP DESCRIPTION -6th RAREST", "SUPER_RARE")
rare = (Color.BLUE + "Rare" + Color.END + " - TEMP DESCRIPTION - 7th RAREST", "RARE")
uncommon = (Color.GREEN + "Uncommon" + Color.END + "- TEMP DESCRIPTION - 8th RAREST", "UNCOMMON")
common = ("Common - TEMP DESCRIPTION - 9th RAREST", "COMMON")
tiers = [pinnacle, special, exotic, prestige, epic, super_rare, rare, uncommon, common]


def bold_string(text_to_bold):
    return "<b>" + text_to_bold + "</b>"


# This should be treated as an interface
class JsonSerializable:

    def to_json(self):
        pass


# TODO: Make it so input field filters out invalid characters
class InputField(QWidget, JsonSerializable):

    def __init__(self, LabelName, font_size=14, isInteger=False, isFloat=False):
        super().__init__()
        self.hbox = QHBoxLayout()
        self.isInteger = isInteger
        self.isFloat = isFloat
        self.label = QLabel(bold_string(LabelName))
        self.label.setFont(QFont("Arial", font_size))
        self.lineEdit = QLineEdit()
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.lineEdit)
        self.hbox.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.hbox)

    def getFieldData(self):
        if self.isInteger:
            return int(self.lineEdit.text())
        elif self.isFloat:
            return float(self.lineEdit.text())

        return self.lineEdit.text()

    def to_json(self):
        return self.getFieldData()


class DropDownMenu(QWidget, JsonSerializable):
    # element[0] is display name, element[1] is real/true name.
    def __init__(self, content, label_name):
        super().__init__()
        self.label = QLabel(bold_string(label_name))
        self.comboBox = QComboBox()
        self.content = content
        for element in content:
            self.comboBox.addItem(element[0])
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.comboBox)
        self.hbox.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.hbox)

    def to_json(self):
        for element in self.content:
            if element[0] == self.comboBox.currentText():
                return element[1]
        return None


# data = {
#     "upgradeName": basic_upgrade[3],
#     "valueToModify": prompt_for_vtm(basic_upgrade[1]),
#     "operation": prompt_for_operator("Which operation would you like this upgrade to utilize? "),
#     "modifier": prompt_for_float("Enter the modifier for your " + basic_upgrade[1] + ": ")
# }
class StrategyWidget(QHBoxLayout, JsonSerializable):
    """A Strategy Widget is a collection of InputFields and is meant to encapsulate an Upgrade Strategy.
    It's also responsible for returning all JSON info necessary for that particular upgrade strategy."""

    def __init__(self, real_name, is_upgrade_strategy=False, is_ore_effect=False):
        super().__init__()
        self.real_name = real_name
        self.isUpgradeStrategy = is_upgrade_strategy
        self.isOreEffect = is_ore_effect
        self.inputFields = []

    def to_json(self):
        if self.isUpgradeStrategy:
            data = {"upgradeName": self.real_name}
        elif self.isOreEffect:
            data = {"effectName": self.real_name}
        else:
            raise Exception("Invalid strategy type")
        for inputField in self.inputFields:
            data.update(inputField.to_json())
        return data

    def appendInputField(self, inputField):
        self.addWidget(inputField, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.inputFields.append(inputField)


class SubMenu(JsonSerializable):
    def __init__(self, strategy_widgets):
        self.strategyWidgets = strategy_widgets
        pass

    def to_json(self):
        data = {}
        for strategy in self.strategyWidgets:
            data.update(strategy.to_json())
        return data


class BasicUpgrade(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()
        self.name = "Basic Upgrade"
        self.nameLabel = QLabel(bold_string(self.name))
        self.vtm = DropDownMenu(vtms, "Value To Modify:")
        self.operation = DropDownMenu(numeric_operations, "Operator:")
        self.modifier = InputField("Modifier:", 12, False, True)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.nameLabel)
        self.hbox.addWidget(self.vtm)
        self.hbox.addWidget(self.operation)
        self.hbox.addWidget(self.modifier)
        self.setLayout(self.hbox)

    def to_json(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.BasicUpgrade",
            "valueToModify": self.vtm.to_json(),
            "operation": self.operation.to_json(),
            "modifier": self.modifier.to_json(),
        }
        return data


class BundledUpgrade(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.name = "Bundled Upgrade"
        self.nameLabel = QLabel(bold_string(self.name))
        self.index = 0
        self.upgradeCount = 0
        self.listOfUpgrades = []
        self.hboxList = []
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.nameLabel)
        self.addNewButton = QPushButton("Add New Upgrade")
        self.addNewButton.clicked.connect(lambda: self.add_new_click())
        self.deleteButton = QPushButton("Delete Upgrade")
        self.deleteButton.clicked.connect(lambda: self.delete_click())
        self.layout.addWidget(self.addNewButton)
        self.setLayout(self.layout)

    def add_upgrade(self):
        upgrade = StrategyChoices.UpgradeChoices()

        self.upgradeCount += 1

        # upgrade.nameLabel.setText(str(self.upgradeCount) + ". " + upgrade.name + ":")

        upgrade.label.setText("Upgrade" + str(self.upgradeCount))

        self.layout.addWidget(upgrade)
        self.listOfUpgrades.append(upgrade)

        self.bind_buttons()

    def remove_buttons(self):
        self.layout.removeWidget(self.deleteButton)
        self.layout.addWidget(self.addNewButton)

    def bind_buttons(self):
        if self.upgradeCount > 1:
            self.deleteButton.show()
        else:
            self.deleteButton.hide()
        self.layout.addWidget(self.deleteButton)
        self.layout.addWidget(self.addNewButton)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def add_new_click(self):
        self.add_upgrade()

    def delete_click(self):
        if self.upgradeCount > 1:
            self.upgradeCount -= 1
            last = self.listOfUpgrades[-1]
            self.listOfUpgrades.remove(last)
            self.layout.removeWidget(last)
            last.deleteLater()
            self.bind_buttons()

    def to_json(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.BundledUpgrade",
        }
        count = 1
        for upgrade in self.listOfUpgrades:
            data["upgStrat" + str(count)] = upgrade.to_json()
            count += 1
        return data


class ConditionalUpgrade(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()

class InfluencedUpgrade(QWidget, JsonSerializable):
    pass

class ResetterUpgrade(QWidget, JsonSerializable):
    pass

class ApplyEffect(QWidget, JsonSerializable):
    pass

class DestroyOre(QWidget, JsonSerializable):
    pass

class CooldownUpgrade(QWidget, JsonSerializable):
    pass

class IncrementalUpgrade(QWidget, JsonSerializable):
    pass