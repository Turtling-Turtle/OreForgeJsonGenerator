from typing import Union

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

from GUI.CustomWidgets.DropDownMenu import DropDownMenu
from Helper_Functions import bold_string

ore_value = ("Ore Value", "ORE_VALUE")
temperature = ("Ore Temperature", "TEMPERATURE")
multiore = ("Multiore", "MULTIORE")
speed = ("Ore Speed", "SPEED")
valuesToModify = [ore_value, temperature, multiore, speed]

# Numeric Operators:
add = ("Add - Adds the modifier to the value to modify.", "ADD")
subtract = ("Subtract - Subtracts the modifier from the value to modify.", "SUBTRACT")
multiply = ("Multiply - Multiplies the value to modify by the modifier.", "MULTIPLY")
divide = ("Divide - Divides the value to modify by the modifier.", "DIVIDE")
exponent = ("Exponent - Raises the value to modify to the power of the modifier.", "EXPONENT")
assignment = ("Assignment - Used to 'set' the value to modify to the value of the modifier.", "ASSIGNMENT")
modulo = ("Modulo - Returns the remainder after two numbers are divided.",
          "MODULO")
numericOperators = [add, subtract, multiply, divide, exponent, assignment, modulo]


class StrategyWidget(QWidget):

    def __init__(self, strategyName: str):
        super().__init__()
        self.jsonWidgets = []
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.strategyName = QLabel(bold_string(strategyName))
        self.strategyName.setFont(QFont("Arial", 16))

        self.layout.addWidget(self.strategyName, 0, 0)

    def addJsonWidget(self, jsonWidget: QWidget):
        self.jsonWidgets.append(jsonWidget)
        self.layout.addWidget(jsonWidget)


def createVTMWidget():
    return DropDownMenu("Value To Modify", "valueToModify", valuesToModify)


def createOperatorWidget():
    return DropDownMenu("Operator", "operator", numericOperators)
