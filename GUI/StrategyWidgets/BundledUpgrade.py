from typing import Union

from GUI.JsonSerializable import JsonSerializable
from GUI.StrategyWidgets.StrategyWidget import StrategyWidget
from GUI.Validators.Validator import ValidationResult


class BundledUpgrade(StrategyWidget, JsonSerializable):
    def __init__(self):
        super().__init__("Bundled Upgrade")

    def toDict(self) -> dict:
        pass

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        pass

