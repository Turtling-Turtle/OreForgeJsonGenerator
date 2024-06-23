from typing import Union

from GUI.CustomWidgets.InputField import InputField
from GUI.JsonSerializable import JsonSerializable
from GUI.StrategyWidgets.StrategyWidget import StrategyWidget, createVTMWidget, createOperatorWidget
from GUI.Validators.FunctionValidator import FunctionValidator
from GUI.Validators.StringValidator import StringValidator
from GUI.Validators.Validator import ValidationResult


class InfluencedUpgradeWidget(StrategyWidget, JsonSerializable):
    def __init__(self):
        super().__init__("Influenced Upgrade")
        self.addJsonWidget(createVTMWidget())
        self.addJsonWidget(createOperatorWidget())

        functionField = InputField("Upgrade Function", StringValidator(), "upgradeFunction", str)
        functionField.validator = FunctionValidator(functionField)
        functionField.validator.setParentFieldName("Upgrade Function")

        self.addJsonWidget(functionField)

    def toDict(self) -> dict:
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.BasicUpgrade",
        }
        for widget in self.jsonWidgets:
            data.update(widget.toDict())
        return {"upgrade": data}

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        results = []
        for widget in self.jsonWidgets:
            result = widget.validate()
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
        return results
