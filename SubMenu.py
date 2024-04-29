import json
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QCheckBox, QVBoxLayout, \
    QHBoxLayout, QPushButton, QBoxLayout, QSpacerItem, QSizePolicy
from abc import ABC, abstractmethod

import StrategyChoices
from Helper_Functions import is_numeric
from Validators import validate_function


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

# Tiers.
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

    def isValid(self):
        pass


# TODO: Make it so input field filters out invalid characters(Ex: field that only takes numbers)
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

    def clear(self):
        self.lineEdit.setText("")

    def setEnabled(self, enabled):
        self.label.setEnabled(enabled)
        self.lineEdit.setEnabled(enabled)

    def to_json(self):
        return self.getFieldData()

    def isValid(self):
        if self.isInteger or self.isFloat:
            return is_numeric(self.lineEdit.text())
        else:
            return len(self.lineEdit.text()) > 0

    def __str__(self):
        return self.label.text()


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

    def clear(self):
        pass

    def setEnabled(self, enabled):
        self.label.setEnabled(enabled)
        self.comboBox.setEnabled(enabled)

    def to_json(self):
        for element in self.content:
            if element[0] == self.comboBox.currentText():
                return element[1]
        return None

    def isValid(self):
        return True

    def __str__(self):
        return self.label.text()


class OptionalField(QWidget, JsonSerializable):
    def __init__(self, q_widget, check_box_prompt):
        super().__init__()
        self.checkBox = QCheckBox(check_box_prompt)
        self.customWidget = q_widget
        self.checkBox.stateChanged.connect(self.on_check_box_toggle)
        self.layout = QHBoxLayout()

        self.layout.addWidget(self.checkBox)
        self.layout.addWidget(self.customWidget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)
        self.on_check_box_toggle(self.checkBox.stateChanged)

    def on_check_box_toggle(self, state):
        if state == 2:
            self.customWidget.setEnabled(True)
        else:
            self.customWidget.clear()
            self.customWidget.setEnabled(False)

    def to_json(self):
        return self.customWidget.to_json() if self.checkBox.isChecked() else None

    def isValid(self):
        return True


class BasicUpgrade(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()
        self.name = "Basic Upgrade"
        # self.nameLabel = QLabel(bold_string(self.name))
        self.vtm = DropDownMenu(vtms, "Value To Modify:")
        self.operation = DropDownMenu(numeric_operations, "Operator:")
        self.modifier = InputField("Modifier:", 12, False, True)
        self.hbox = QHBoxLayout()
        # self.hbox.addWidget(self.nameLabel)
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

    def isValid(self):
        return self.vtm.isValid() and self.operation.isValid() and self.modifier.isValid()


class BundledUpgrade(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.name = "Bundled Upgrade"
        # self.nameLabel = QLabel(bold_string(self.name))
        self.upgradeCount = 0
        self.listOfUpgrades = []
        self.layout = QVBoxLayout()
        # self.layout.addWidget(self.nameLabel)
        self.adderButton = QPushButton("Add New Upgrade")
        self.adderButton.clicked.connect(lambda: self.add_new_click())
        self.deleteButton = QPushButton("Delete Upgrade")
        self.deleteButton.clicked.connect(lambda: self.delete_click())
        self.layout.addWidget(self.adderButton)
        self.setLayout(self.layout)

    def add_upgrade(self):
        upgrade = StrategyChoices.UpgradeChoices()
        self.upgradeCount += 1
        upgrade.label.setText("Upgrade " + str(self.upgradeCount))
        self.layout.addWidget(upgrade)
        self.listOfUpgrades.append(upgrade)

        self.bind_buttons()

    def bind_buttons(self):
        if self.upgradeCount > 1:
            self.deleteButton.show()
        else:
            self.deleteButton.hide()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.deleteButton)
        self.layout.addWidget(self.adderButton)

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

    def isValid(self):
        return all(upgrade.isValid() for upgrade in self.listOfUpgrades)


class ConditionalUpgrade(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.conditionField = InputField("Condition:")
        self.trueBranch = StrategyChoices.UpgradeChoices()
        self.trueBranch.set_label_name("True Branch")
        self.falseBranch = StrategyChoices.UpgradeChoices()
        self.falseBranch.set_label_name("False Branch")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.conditionField)
        self.layout.addWidget(self.trueBranch)
        self.layout.addWidget(self.falseBranch)
        self.setLayout(self.layout)

    def to_json(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.ConditionalUpgrade",
            "condition": self.conditionField.to_json(),
            "trueBranch": self.trueBranch.to_json(),
            "falseBranch": self.falseBranch.to_json(),
        }
        return data


class InfluencedUpgrade(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.functionField = InputField("Custom Function:")
        self.numericOperator = DropDownMenu(numeric_operations, "Operator:")
        self.minModifier = OptionalField(InputField("Minimum Modifier", font_size=14, isInteger=False, isFloat=True),
                                         "Set Minimum Modifier?")
        self.maxModifier = OptionalField(InputField("Maximum Modifier:", font_size=14, isInteger=False, isFloat=True),
                                         "Set Maximum Modifier?")

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.functionField)
        self.layout.addWidget(self.numericOperator)
        self.layout.addWidget(self.minModifier)
        self.layout.addWidget(self.maxModifier)
        self.setLayout(self.layout)

    def to_json(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.InfluencedUpgrade",
            "upgradeFunction": self.functionField.to_json(),
            "numericOperator": self.numericOperator.to_json(),
            "mindModifier": self.minModifier.to_json(),
            "maxModifier": self.maxModifier.to_json(),
        }

        return data

    def isValid(self):
        return (validate_function(self.functionField.getFieldData()) and self.numericOperator.isValid() and
                self.minModifier.isValid() and self.maxModifier.isValid())


class ResetterUpgrade(QWidget, JsonSerializable):

    def to_json(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.ResetterUpgrade",
        }

        return data


class ApplyEffect(QWidget, JsonSerializable):

    def to_json(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.ApplyEffect",
        }

        return data


class DestroyOre(QWidget, JsonSerializable):

    def to_json(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.DestroyOre",
        }

        return data


class CooldownUpgrade(QWidget, JsonSerializable):
    pass


class IncrementalUpgrade(QWidget, JsonSerializable):
    pass
