from typing import Union

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox

from GUI.CustomWidgets.CheckBoxField import CheckBoxField
from GUI.CustomWidgets.InputField import InputField
from GUI.JsonSerializable import JsonSerializable
from GUI.UpgradeStrategyWidgets.Constants import returnUpgradeStrategies
from GUI.UpgradeStrategyWidgets.StrategyChoiceField import StrategyChoiceField
from GUI.UpgradeStrategyWidgets.StrategyWidget import StrategyWidget
from GUI.Validators.ConditionValidator import ConditionValidator
from GUI.Validators.Validator import ValidationResult


class ConditionalUpgradeWidget(StrategyWidget, JsonSerializable):

    def __init__(self, strategyChoiceField, parent: QWidget = None):
        super().__init__(strategyChoiceField, "Conditional Upgrade", QVBoxLayout(), parent=parent)
        self.addWidget(self.nameLabel)
        self.addWidget(self.strategyChoice)
        self.addJsonWidget(InputField("Condition", ConditionValidator(), "condition", str))
        self.addJsonWidget(StrategyChoiceField(returnUpgradeStrategies(), strategyName="True Branch Strategy", ))

        self.toggle = CheckBoxField("Enable False Branch?", "")
        self.toggle.checkBox.stateChanged.connect(self.update)
        self.toggle.checkBox.setChecked(False)
        self.addWidget(self.toggle)

        self.falseBranch = StrategyChoiceField(returnUpgradeStrategies(), strategyName="False Branch Strategy")
        self.addWidget(self.falseBranch)
        self.update()

    def update(self) -> None:
        if self.toggle.checkBox.isChecked():
            self.falseBranch.setDisabled(False)
        else:
            self.falseBranch.setDisabled(True)

    def toDict(self) -> dict:
        results = {
            "upgradeName": "ore.forge.Strategies.UpgradeStrategies.ConditionalUpgrade",
        }

        for widget in self.jsonWidgets:
            if isinstance(widget, StrategyChoiceField):
                trueBranch = widget.toDict()
                trueBranch["trueBranch"] = trueBranch.pop("upgrade")
                results.update(trueBranch)
            else:
                results.update(widget.toDict())
        if self.toggle.checkBox.isChecked():
            falseBranch = self.falseBranch.toDict()
            falseBranch["falseBranch"] = falseBranch.pop("upgrade")
            results.update(falseBranch)
        return {"upgrade": results}

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        results = []
        for widget in self.jsonWidgets:
            result = widget.validate()
            print(widget.label.text())
            assert result is not None
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
        if self.toggle.checkBox.isChecked():
            result = self.falseBranch.validate()
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
        return results
