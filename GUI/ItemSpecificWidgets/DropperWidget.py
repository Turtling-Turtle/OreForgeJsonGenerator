from typing import Union

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from GUI.CustomWidgets.InputField import InputField
from GUI.JsonSerializable import JsonSerializable
from GUI.Validators.NumberValidator import NumberValidator
from GUI.Validators.StringValidator import StringValidator
from GUI.Validators.Validator import ValidationResult


class DropperWidget(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.jsonWidgets = []
        self.masterLayout = QVBoxLayout()
        self.mainLayout = QVBoxLayout()
        self.dropperBehaviorField = DropperBehaviorWidget()
        self.oreStatsField = OreStatsWidget()

        for field in vars(self).values():
            if isinstance(field, JsonSerializable):
                self.mainLayout.addWidget(field)

        self.setLayout(self.mainLayout)


class DropperBehaviorWidget(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.orePerMinute = InputField("Ore Per Minute", NumberValidator(float), "orePerMinute", float)
        self.oreInBurst = InputField("Ore In Burst", NumberValidator(int), "burstCount", int)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.orePerMinute)
        self.layout.addWidget(self.oreInBurst)

    def toDict(self) -> dict:
        data = {}
        data.update(self.orePerMinute.toDict())
        data.update(self.oreInBurst.toDict())
        return data

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        return [self.orePerMinute.validate(), self.oreInBurst.validate()]


class OreStatsWidget(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.oreName = InputField("Ore Name", StringValidator(), "oreName", str)
        self.oreValue = InputField("Ore Value", NumberValidator(float), "oreValue", float)
        self.oreTemperature = InputField("Ore Temperature", NumberValidator(float), "oreTemp", float)
        self.multiOre = InputField("MultiOre", NumberValidator(int), "multiOre", int)
        self.layout = QVBoxLayout()
        for field in vars(self).values():
            if isinstance(field, JsonSerializable):
                self.layout.addWidget(field)

    def toDict(self) -> dict:
        info = {}
        for field in vars(self).values():
            if isinstance(field, JsonSerializable):
                info.update(field.toDict())
        return info

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        results = []
        for field in vars(self).values():
            if isinstance(field, JsonSerializable):
                result = field.validate()
                results.extend(result) if isinstance(result, list) else results.append(result)
        return results
