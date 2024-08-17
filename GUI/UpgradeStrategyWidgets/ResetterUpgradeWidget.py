from typing import Union

from GUI.JsonSerializable import JsonSerializable
from GUI.UpgradeStrategyWidgets.StrategyWidget import StrategyWidget
from GUI.Validators.Validator import ValidationResult


class ResetterUpgradeWidget(StrategyWidget, JsonSerializable):
    def __init__(self, strategyChoiceMenu):
        super().__init__(strategyChoiceMenu, "Resetter Upgrade")
        self.setName("Resetter Upgrade")
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.strategyChoice)

    def toDict(self) -> dict:
        return {"upgrade": {"upgradeName": "ore.forge.Strategies.ResetterUpgrade"}}

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        return ValidationResult()
