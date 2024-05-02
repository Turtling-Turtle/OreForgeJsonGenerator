import json
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QCheckBox, QVBoxLayout, \
    QHBoxLayout, QPushButton, QBoxLayout, QSpacerItem, QSizePolicy, QToolTip
from abc import ABC, abstractmethod

import StrategyChoice
from Helper_Functions import is_numeric
from Validators import validate_function

"""
Types of Errors:
    * Field filled out incorrectly(not putting an int or float in a field that only accepts and int or float.)
    * A required field is left empty.
    * Syntax error(a function or condition has incorrect syntax/is invalid)
        * Give more descriptive errors based on the syntax error. 
    
    
"""


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
    def __init__(self, LabelName, font_size=14, isInteger=False, isFloat=False, label_tip=None, edit_tip=None):
        super().__init__()
        self.name = LabelName
        self.hbox = QHBoxLayout()
        self.isInteger = isInteger
        self.isFloat = isFloat
        self.label = QLabel(bold_string(LabelName))
        self.label.setToolTip(label_tip)
        self.label.setFont(QFont("Arial", font_size))
        self.lineEdit = QLineEdit()
        self.lineEdit.setToolTip(label_tip)
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
        if len(self.lineEdit.text()) <= 0:
            return "*" + self.name + " is empty"
        elif self.isInteger:
            try:
                int(self.lineEdit.text())
                return
            except ValueError:
                return "* Input in " + self.name + " field is not an integer"
        elif self.isFloat:
            if is_numeric(self.lineEdit.text()):
                return
            else:
                return "* Input in " + self.name + " field is not a valid float"

    def __str__(self):
        return self.label.text()

    def set_label_tip(self, text):
        self.label.setToolTip(text)

    def set_edit_tip(self, text):
        self.lineEdit.setToolTip(text)

    def set_both_tips(self, text):
        self.set_label_tip(text)
        self.set_edit_tip(text)


class DropDownMenu(QWidget, JsonSerializable):
    # element[0] is display name, element[1] is real/true name.
    def __init__(self, content, label_name, label_tip=None, box_tip=None):
        super().__init__()
        self.label = QLabel(bold_string(label_name))
        self.label.setFont(QFont("Arial", 14))
        self.label.setToolTip(label_tip)
        self.comboBox = QComboBox()
        self.comboBox.setToolTip(box_tip)
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
        return

    def __str__(self):
        return self.label.text()


class OptionalField(QWidget, JsonSerializable):
    def __init__(self, q_widget, check_box_prompt, boolean_field, widget_field):
        super().__init__()
        self.checkBox = QCheckBox(check_box_prompt)
        self.customWidget = q_widget
        self.checkBox.stateChanged.connect(self.on_check_box_toggle)
        self.layout = QHBoxLayout()

        self.layout.addWidget(self.checkBox)
        self.layout.addWidget(self.customWidget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.booleanField = boolean_field
        self.widget_field = widget_field
        self.setLayout(self.layout)
        self.on_check_box_toggle(self.checkBox.stateChanged)

    def on_check_box_toggle(self, state):
        if state == 2:
            self.customWidget.setEnabled(True)
        else:
            self.customWidget.clear()
            self.customWidget.setEnabled(False)

    def to_json(self):
        pass

    def isValid(self):
        pass

    def setIsValid(self, function):
        self.isValid = function

    def set_to_json(self, method):
        self.to_json = method


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
        return self.modifier.isValid()

    def __str__(self):
        self.name = "Basic Upgrade"
        return self.name


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
        self.add_upgrade()

    def add_upgrade(self):
        upgrade = StrategyChoice.StrategyChoiceField(StrategyChoice.upgradeStrategies)
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
        fields = []
        for upgrade in self.listOfUpgrades:
            if upgrade.isValid() is not None:
                fields.append(upgrade.isValid())
        return fields

    def __str__(self):
        self.name = "Bundled Upgrade"
        return self.name


class ConditionalUpgrade(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.name = "Conditional Upgrade"
        self.conditionField = InputField("Condition:")
        self.trueBranch = StrategyChoice.StrategyChoiceField(StrategyChoice.upgradeStrategies)
        self.trueBranch.set_label_name("True Branch")
        self.falseBranch = StrategyChoice.StrategyChoiceField(StrategyChoice.upgradeStrategies)
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

    def isValid(self):
        raise ValueError("Not IMPLEMENTED YET!!!")

    def __str__(self):
        self.name = "Conditional Upgrade"
        return self.name


class InfluencedUpgrade(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.name = "Influenced Upgrade"
        self.functionField = InputField("Custom Function:")
        self.numericOperator = DropDownMenu(numeric_operations, "Operator:")
        self.minModifier = OptionalField(InputField("Minimum Modifier", font_size=14, isInteger=False, isFloat=True),
                                         "Set Minimum Modifier?", None, "minModifier")
        self.maxModifier = OptionalField(InputField("Maximum Modifier:", font_size=14, isInteger=False, isFloat=True),
                                         "Set Maximum Modifier?", None, "maxModifier")

        valid = lambda self: self.customWidget.isValid() if self.checkBox.isChecked() else None

        json = lambda self: {self.widget_field: self.customWidget.to_json()} if self.checkBox.isChecked() else None

        self.minModifier.setIsValid(lambda: valid(self.minModifier))
        self.minModifier.set_to_json(lambda: json(self.minModifier))

        self.maxModifier.setIsValid(lambda: valid(self.maxModifier))
        self.maxModifier.set_to_json(lambda: json(self.maxModifier))

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
        }
        if self.minModifier.to_json() is not None:
            data.update(self.minModifier.to_json())
        if self.maxModifier.to_json() is not None:
            data.update(self.maxModifier.to_json())

        return data

    def isValid(self):
        results = [
            validate_function(self.functionField.getFieldData()),
            self.functionField.isValid(),
            self.minModifier.isValid(),
            self.maxModifier.isValid()
        ]

        errors = []
        for element in results:
            if element is not None:
                errors.append(element)

        return errors

    def __str__(self):
        self.name = "Influenced Upgrade"
        return self.name


class ResetterUpgrade(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()
        self.label = QLabel("Resetter Upgrade")
        self.label.setFont(QFont(bold_string("Arial"), 14))
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def to_json(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.ResetterUpgrade",
        }

        return data

    def isValid(self):
        return

    def __str__(self):
        self.name = "Resetter Upgrade"
        return self.name


class ApplyEffect(QWidget, JsonSerializable):

    def to_json(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.ApplyEffect",
        }

        return data

    def __str__(self):
        self.name = "Apply Effect"
        return self.name


class DestroyOre(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()
        self.label = QLabel("Destroy Ore Upgrade")
        self.label.setFont(QFont(bold_string("Arial"), 14))
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def to_json(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.DestroyOre",
        }

        return data

    def isValid(self):
        return

    def __str__(self):
        self.name = "Destroy Ore"
        return self.name


class CooldownUpgrade(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()

    def __str__(self):
        self.name = "Cooldown Upgrade"
        return self.name


class IncrementalUpgrade(QWidget, JsonSerializable):
    pass

    def __str__(self):
        self.name = "Incremental Upgrade"
        return self.name
