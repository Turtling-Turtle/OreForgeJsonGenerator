from queue import LifoQueue

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, \
    QHBoxLayout

import StrategyChoice
from CustomWidgets import InputField, DropDownMenu, OptInField, JsonSerializable, bold_string
from Validators import validate_function, validate_condition


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


class BasicUpgrade(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()
        self.name = "Basic Upgrade"
        self.vtm = DropDownMenu(valuesToModify, "Value To Modify:")
        self.operation = DropDownMenu(numericOperators, "Operator:")
        self.modifier = InputField("Modifier:", 12, False, True)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.vtm)
        self.hbox.addWidget(self.operation)
        self.hbox.addWidget(self.modifier)
        self.setLayout(self.hbox)

    def toJson(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.BasicUpgrade",
            "valueToModify": self.vtm.toJson(),
            "operation": self.operation.toJson(),
            "modifier": self.modifier.toJson(),
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
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.bundle = StrategyChoice.Bundle(StrategyChoice.upgradeStrategyInfo)
        self.layout.addWidget(self.bundle)

    def toJson(self):
        return self.bundle.toJson()

    def isValid(self):
        return self.bundle.isValid()

    def __str__(self):
        self.name = "Bundled Upgrade"
        return self.name


class ConditionalUpgrade(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.name = "Conditional Upgrade"
        self.conditionField = InputField("Condition:")
        self.trueBranch = StrategyChoice.StrategyChoiceField(StrategyChoice.upgradeStrategies, "True Branch")
        self.falseBranch = OptInField(StrategyChoice.StrategyChoiceField(StrategyChoice.upgradeStrategies,
                                                                            "False Branch"), "False Branch?")

        valid = lambda self: self.customWidget.isValid() if self.checkBox.isChecked else None
        json = lambda self: self.customWidget.toJson() if self.checkBox.isChecked else None
        self.falseBranch.setIsValid(lambda: valid(self.falseBranch))
        self.falseBranch.setToJson(lambda: json(self.falseBranch))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.conditionField)
        self.layout.addWidget(self.trueBranch)
        self.layout.addWidget(self.falseBranch)
        self.setLayout(self.layout)

    def toJson(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.ConditionalUpgrade",
            "condition": self.conditionField.toJson(),
            "trueBranch": self.trueBranch.toJson(),
        }
        if self.falseBranch.checkBox.isChecked():
            data.update({"falseBranch": self.falseBranch.toJson()})
        return data

    def isValid(self):
        results = []
        results.append(validate_condition(self.conditionField.getFieldData()))
        if isinstance(self.trueBranch.isValid(), list):
            results.extend(self.trueBranch.isValid())
        else:
            results.append(self.trueBranch.isValid())
        if self.falseBranch.checkBox.isChecked():
            if isinstance(self.falseBranch.isValid(), list):
                results.extend(self.falseBranch.isValid())
            else:
                results.append(self.falseBranch.isValid())
        return results
        # raise ValueError("Not IMPLEMENTED YET!!!")

    def __str__(self):
        self.name = "Conditional Upgrade"
        return self.name


class InfluencedUpgrade(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.name = "Influenced Upgrade"
        self.functionField = InputField("Custom Function:")
        self.numericOperator = DropDownMenu(numericOperators, "Operator:")
        self.minModifier = OptInField(InputField("Minimum Modifier", isFloat=True), "Set Minimum Modifier?",
                                      widgetJsonKey="minModifier")
        self.maxModifier = OptInField(InputField("Maximum Modifier:", isFloat=True), "Set Maximum Modifier?",
                                      widgetJsonKey="maxModifier")
        self.valueToModify = DropDownMenu(valuesToModify, "Value To Modify:")

        valid = lambda self: self.customWidget.isValid() if self.checkBox.isChecked() else None

        json = lambda self: {self.widgetJsonKey: self.customWidget.toJson()} if self.checkBox.isChecked() else None

        self.minModifier.setIsValid(lambda: valid(self.minModifier))
        self.minModifier.setToJson(lambda: json(self.minModifier))

        self.maxModifier.setIsValid(lambda: valid(self.maxModifier))
        self.maxModifier.setToJson(lambda: json(self.maxModifier))

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.functionField)
        self.layout.addWidget(self.valueToModify)
        self.layout.addWidget(self.numericOperator)
        self.layout.addWidget(self.minModifier)
        self.layout.addWidget(self.maxModifier)

        self.setLayout(self.layout)

    def toJson(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.InfluencedUpgrade",
            "upgradeFunction": self.validatedFunction,
            "valueToModify": self.valueToModify.toJson(),
            "numericOperator": self.numericOperator.toJson(),
        }
        if self.minModifier.toJson() is not None:
            data.update(self.minModifier.toJson())
        if self.maxModifier.toJson() is not None:
            data.update(self.maxModifier.toJson())

        return data

    def isValid(self):
        results = [
            validate_function(self.functionField.getFieldData()),
            # self.functionField.isValid(),
            self.minModifier.isValid(),
            self.maxModifier.isValid()
        ]

        if isinstance(results[0], LifoQueue):
            self.validatedFunction = results[0].get_nowait()
            results.remove(results[0])

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

    def toJson(self):
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
    def __init__(self):
        super().__init__()
        self.effectChoice = StrategyChoice.StrategyChoiceField(StrategyChoice.oreEffects, "Effect")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.effectChoice)
        self.setLayout(self.layout)

    def toJson(self):
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.ApplyEffect",
            "effectToApply": self.effectChoice.toJson()
        }

        return data

    def isValid(self):
        return self.effectChoice.isValid()

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

    def toJson(self):
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
