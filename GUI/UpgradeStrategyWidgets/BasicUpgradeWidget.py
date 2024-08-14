from typing import Union

from PyQt6.QtWidgets import QVBoxLayout

from GUI.CustomWidgets.InputField import InputField
from GUI.JsonSerializable import JsonSerializable
from GUI.UpgradeStrategyWidgets.StrategyWidget import StrategyWidget, createVTMWidget, createOperatorWidget
from GUI.Validators.NumberValidator import NumberValidator
from GUI.Validators.Validator import ValidationResult


# Values ot Modify.


class BasicUpgradeWidget(StrategyWidget, JsonSerializable):
    def __init__(self, dropdownMenu, parent: object = None):
        super().__init__(dropdownMenu, "Basic Upgrade", QVBoxLayout(), parent=parent)
        self.addWidget(self.nameLabel)
        self.addWidget(self.strategyChoice)
        self.addJsonWidget(createVTMWidget())
        self.addJsonWidget(createOperatorWidget())
        self.addJsonWidget(InputField("Modifier", NumberValidator(float), "modifier", float))

    def toDict(self) -> dict:
        results = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.BasicUpgrade",
        }
        for widget in self.jsonWidgets:
            results.update(widget.toDict())
        return {"upgrade": results}

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        results = []
        for widget in self.jsonWidgets:
            result = widget.validate()
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
        return results
