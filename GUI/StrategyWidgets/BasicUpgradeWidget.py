from typing import Union

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QGridLayout

from GUI.CustomWidgets.DropDownMenu import DropDownMenu
from GUI.CustomWidgets.InputField import InputField
from GUI.JsonSerializable import JsonSerializable
from GUI.StrategyWidgets.StrategyWidget import StrategyWidget, createVTMWidget, createOperatorWidget
from GUI.Validators.NumberValidator import NumberValidator
from GUI.Validators.Validator import ValidationResult


# Values ot Modify.


class BasicUpgradeWidget(StrategyWidget, JsonSerializable):
    def __init__(self, parent=None):
        super().__init__("Basic Upgrade")

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
