from typing import Union

from GUI.JsonSerializable import JsonSerializable
from GUI.UpgradeStrategyWidgets.StrategyWidget import StrategyWidget
from GUI.Validators.Validator import ValidationResult


class DestructionUpgradeWidget(StrategyWidget, JsonSerializable):
    def __init__(self, strategyChoiceMenu):
        super().__init__(strategyChoiceMenu, "Destruction Upgrade")
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.strategyChoice)
        self.setName("Destruction Upgrade")

    def toDict(self) -> dict:
        return {"upgrade": {"upgradeName": "ore.forge.Strategies.UpgradeStrategies.DestructionUpgrade"}}

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        return ValidationResult()
