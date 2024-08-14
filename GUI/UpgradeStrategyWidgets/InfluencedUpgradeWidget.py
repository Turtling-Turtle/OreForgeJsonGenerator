from typing import Union

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from GUI.CustomWidgets.InputField import InputField
from GUI.CustomWidgets.OptInWidgetField import OptInWidgetField
from GUI.JsonSerializable import JsonSerializable
from GUI.UpgradeStrategyWidgets.StrategyWidget import StrategyWidget, createVTMWidget, createOperatorWidget
from GUI.Validators.FunctionValidator import FunctionValidator
from GUI.Validators.NumberValidator import NumberValidator
from GUI.Validators.StringValidator import StringValidator
from GUI.Validators.Validator import ValidationResult


class InfluencedUpgradeWidget(StrategyWidget, JsonSerializable):
    def __init__(self, choiceField, parent: QWidget = None):
        super().__init__(choiceField, "Influenced Upgrade", QVBoxLayout(), parent=parent)
        self.addWidget(self.nameLabel)
        self.addWidget(self.strategyChoice)
        self.addJsonWidget(createVTMWidget())
        self.addJsonWidget(
            createOperatorWidget().setBothToolTip("How the result of the upgrade function will be applied to the ore."))

        self.minModifier = OptInWidgetField("Enable Minimum Modifier", "",
                                            InputField("Min Modifier", NumberValidator(float), "minModifier", float))
        self.maxModifier = OptInWidgetField("Enable Maximum Modifier", "",
                                            InputField("Max Modifier", NumberValidator(float), "maxModifier", float))

        functionField = InputField("Upgrade Function", StringValidator(), "upgradeFunction", str)
        functionField.validator = FunctionValidator(functionField)
        functionField.validator.setParentFieldName("Upgrade Function")

        self.addJsonWidget(functionField)
        self.addJsonWidget(self.minModifier)
        self.addJsonWidget(self.maxModifier)

    def toDict(self) -> dict:
        data = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.InfluencedUpgrade",
        }
        for widget in self.jsonWidgets:
            result = widget.toDict()
            if result:
                data.update(result)
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
