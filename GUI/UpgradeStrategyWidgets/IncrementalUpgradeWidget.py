from typing import Union

from PyQt6.QtWidgets import QVBoxLayout

from GUI.UpgradeStrategyWidgets.BundledStrategy import BundledStrategy
from GUI.UpgradeStrategyWidgets.StrategyWidget import StrategyWidget
from GUI.Validators.Validator import ValidationResult


class IncrementalUpgrade(BundledStrategy):
    def __init__(self, choiceField):
        super().__init__(choiceField)
        self.setName("Incremental Upgrade")
        print(self.nameLabel.text())

    def toDict(self) -> dict:
        results = {"upgradeName": "ore.forge.Strategies.UpgradeStrategies.IncrementalUpgrade"}
        listOfFields = []
        for field in self.choiceFields:
            fieldData = field.toDict()
            listOfFields.append(fieldData.pop("upgrade"))
        results.update({"upgrades": listOfFields})
        return {"upgrade": results}
