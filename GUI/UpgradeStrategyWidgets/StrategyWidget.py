from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QLayout, QGroupBox, QBoxLayout

from GUI.CustomWidgets.DropDownMenu import DropDownMenu
from GUI.JsonSerializable import JsonSerializable
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

    def __init__(self, strategyChoiceMenu, strategyName: str = None, layout: QBoxLayout = None,
                 parent: QWidget = None):
        super().__init__(parent=parent)
        self.jsonWidgets = []
        self.strategyChoice = strategyChoiceMenu.dropDownMenu
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.masterLayout = QVBoxLayout()
        self.groupBox = QGroupBox()
        # self.layout = layout
        self.groupBox.setLayout(self.layout)
        self.masterLayout.addWidget(self.groupBox)
        self.setLayout(self.masterLayout)
        #
        #
        self.strategyName = strategyName
        self.nameLabel = QLabel(bold_string(strategyName + ":"))
        self.nameLabel.setFont(QFont("Arial", 16))
        #
        # self.layout.addWidget(self.nameLabel)

    def addJsonWidget(self, jsonWidget: JsonSerializable):
        self.jsonWidgets.append(jsonWidget)
        self.layout.addWidget(jsonWidget)

    def addWidget(self, widget: QWidget):
        self.layout.addWidget(widget)

    def setName(self, newName: str):
        self.strategyName = newName
        self.nameLabel.setText(bold_string(newName))
        self.nameLabel.setFont(QFont("Arial", 16))

    def addToJsonWidgetList(self, jsonWidget: JsonSerializable):
        self.jsonWidgets.append(jsonWidget)


def createVTMWidget():
    return DropDownMenu("Value To Modify", "valueToModify", valuesToModify)


def createOperatorWidget():
    return DropDownMenu("Operator", "operator", numericOperators)
