from typing import Union

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QGroupBox, QVBoxLayout

from GUI.JsonSerializable import JsonSerializable
from GUI.UpgradeStrategyWidgets.ConstructorDictionary import returnUpgradeStrategies
from GUI.UpgradeStrategyWidgets.StrategyChoiceField import StrategyChoiceField
from GUI.UpgradeStrategyWidgets.StrategyWidget import StrategyWidget
from GUI.Validators.Validator import ValidationResult


class BundledStrategy(StrategyWidget, JsonSerializable):
    def __init__(self, choiceField):
        super().__init__(choiceField, "Bundled Upgrade", QVBoxLayout())
        self.choiceFields = []
        self.addWidget(self.nameLabel)
        self.addJsonWidget(self.strategyChoice)
        # self.boxLayout = QVBoxLayout()

        # self.groupWidget = QGroupBox()
        # self.groupWidget.setLayout(self.boxLayout)
        # self.masterLayout.addWidget(self.groupWidget)
        # self.layout.addWidget(self.groupWidget)
        self.addButton = QPushButton("Add Strategy")
        self.removeButton = QPushButton("Remove Strategy")
        # self.addJsonWidget(self.removeButton)
        # self.addJsonWidget(self.addButton)
        self.addWidget(self.removeButton)
        self.addWidget(self.addButton)

        self.addButton.clicked.connect(self.addClick)
        self.removeButton.clicked.connect(self.removeClick)
        self.addChoiceField(StrategyChoiceField(returnUpgradeStrategies()))
        # self.setLayout(self.boxLayout)

    def addClick(self):
        self.addChoiceField(StrategyChoiceField(returnUpgradeStrategies()))

    def removeClick(self):
        if len(self.choiceFields) <= 1:
            return
        else:
            self.layout.removeWidget(self.choiceFields[-1])
            self.choiceFields.remove(self.choiceFields[-1])
            # self.layout.removeWidget(self.addButton)
            # self.choiceFields.remove(self.)
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
        # self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def toDict(self) -> dict:
        results = {"upgradeName": "ore.forge.Strategies.UpgradeStrategies.BundledUpgrade"}
        listOfFields = []
        for field in self.jsonWidgets:
            fieldData = field.toDict()
            # fieldData.pop("upgrade")
            listOfFields.append(fieldData.pop("upgrade"))
        results.update({"upgrades": listOfFields})
        return {"upgrade": results}

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        results = []
        for field in self.choiceFields:
            result = field.validate()
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
        return results
