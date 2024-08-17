from typing import Union

from PyQt6.QtWidgets import QWidget, QGroupBox, QVBoxLayout

from GUI.CustomWidgets.CheckBoxField import CheckBoxField
from GUI.CustomWidgets.InputField import InputField
from GUI.JsonSerializable import JsonSerializable
from GUI.UpgradeStrategyWidgets.ConstructorDictionary import returnUpgradeStrategies
from GUI.UpgradeStrategyWidgets.StrategyChoiceField import StrategyChoiceField
from GUI.Validators.NumberValidator import NumberValidator
from GUI.Validators.Validator import ValidationResult


class UpgraderWidget(QWidget, JsonSerializable):
    def __init__(self, ID: str, name: str):
        super().__init__()
        self.jsonWidgets = []
        # self.gridBox = QGroupBox()
        self.masterLayout = QVBoxLayout()
        self.mainLayout = QVBoxLayout()
        self.conveyorField = InputField("Conveyor Speed", NumberValidator(float), "conveyorSpeed", float)
        self.upgradeTagField = UpgradeTagWidget(ID, name)
        self.upgradeStrategy = StrategyChoiceField(returnUpgradeStrategies(), "Upgrade ")

        for field in vars(self).values():
            if isinstance(field, JsonSerializable):
                self.mainLayout.addWidget(field)

        # self.gridBox.setLayout(self.mainLayout)
        # self.masterLayout.addWidget(self.gridBox)
        self.setLayout(self.mainLayout)


class UpgradeTagWidget(QWidget, JsonSerializable):
    def __init__(self, ID: str, name: str):
        super().__init__()
        self.layout = QVBoxLayout()
        self.name = name
        self.id = ID
        self.maxUpgrades = InputField("Max Upgrades", NumberValidator(int, min_value=1), "maxUpgrades", int)
        self.isResetter = CheckBoxField("Is Resetter?", "isResetter")
        self.layout.addWidget(self.maxUpgrades)
        self.layout.addWidget(self.isResetter)
        self.setLayout(self.layout)

    def toDict(self) -> dict:
        info = {
            "name": self.name,
            "id": self.id,
        }
        info.update(self.maxUpgrades.toDict())
        info.update(self.isResetter.toDict())
        return {"upgradeTag": info}

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        return self.maxUpgrades.validate()
