from typing import Union

from PyQt6.QtWidgets import QVBoxLayout, QPushButton

from GUI.CustomWidgets.InputField import InputField
from GUI.JsonSerializable import JsonSerializable
from GUI.UpgradeStrategyWidgets.BundledStrategy import BundledStrategy
from GUI.UpgradeStrategyWidgets.ConstructorDictionary import returnUpgradeStrategies
from GUI.UpgradeStrategyWidgets.StrategyChoiceField import StrategyChoiceField
from GUI.UpgradeStrategyWidgets.StrategyWidget import StrategyWidget
from GUI.Validators.NumberValidator import NumberValidator
from GUI.Validators.Validator import ValidationResult, Validator

"""
[
{"chance": x
upgradeInfo
},



]
"""


class RandomUpgradeWidget(StrategyWidget, JsonSerializable):
    def __init__(self, choiceField):
        super().__init__(choiceField, "Random Upgrade", QVBoxLayout())
        self.chanceFields = []
        self.choiceFields = []
        self.addWidget(self.nameLabel)
        self.addJsonWidget(self.strategyChoice)

        self.addButton = QPushButton("Add Strategy")
        self.removeButton = QPushButton("Remove Strategy")
        # self.addJsonWidget(self.removeButton)
        # self.addJsonWidget(self.addButton)
        self.addWidget(self.removeButton)
        self.addWidget(self.addButton)

        self.addButton.clicked.connect(self.addClick)
        self.removeButton.clicked.connect(self.removeClick)
        self.addNewChanceField()
        self.addChoiceField(StrategyChoiceField(returnUpgradeStrategies()))
        # self.setLayout(self.boxLayout)

    def addClick(self):
        self.addNewChanceField()
        self.addChoiceField(StrategyChoiceField(returnUpgradeStrategies()))

    def removeClick(self):
        if len(self.choiceFields) <= 1:
            return
        else:
            self.layout.removeWidget(self.chanceFields[-1])
            self.chanceFields.remove(self.chanceFields[-1])

            self.layout.removeWidget(self.choiceFields[-1])

            self.choiceFields.remove(self.choiceFields[-1])

            self.bindButtons()

    def addChoiceField(self, choiceField):
        self.choiceFields.append(choiceField)
        self.layout.addWidget(choiceField)
        self.bindButtons()

    def bindButtons(self):
        self.layout.removeWidget(self.removeButton)
        self.layout.removeWidget(self.addButton)
        if len(self.choiceFields) > 1:
            self.removeButton.show()
        else:
            self.removeButton.hide()
        self.layout.addWidget(self.removeButton)
        self.layout.addWidget(self.addButton)

    def addNewChanceField(self):
        validator = NumberValidator(float, 0.01, 100)
        chanceField = InputField("Activation Chance", validator, "chance", float)
        self.chanceFields.append(chanceField)
        self.addToJsonWidgetList(chanceField)
        self.layout.addWidget(chanceField)

    def toDict(self) -> dict:
        results = {"upgradeName": "ore.forge.Strategies.UpgradeStrategies.RandomUpgrade"}
        collectionOfUpgrades = []
        for i in range(0, len(self.choiceFields)):
            fieldData = self.choiceFields[i].toDict()
            chanceField = self.chanceFields[i].toDict()
            tempDict = {}
            tempDict.update(chanceField)
            tempDict.update(fieldData)
            collectionOfUpgrades.append(tempDict.pop(
                "upgrade"))  # Removes the upgrade key from the dict then merges the value with current dict.
        results.update({"upgrades": collectionOfUpgrades})
        return results

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        results = []
        for i in range(0, len(self.choiceFields)):
            results.append(self.chanceFields[i].validate())
            result = self.choiceFields[i].validate()
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
        return results
