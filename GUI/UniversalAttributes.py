from typing import Union

from PyQt6.QtWidgets import QWidget

from GUI.CustomWidgets.InputField import InputField
from GUI.JsonSerializable import JsonSerializable
from GUI.Validators.StringValidator import StringValidator
from GUI.Validators.Validator import ValidationResult


class UniversalAttributes(QWidget, JsonSerializable):
    def __init__(self, ):
        super().__init__()
        self.itemName = InputField("Name", StringValidator(), "name", str)
        self.itemDescription = InputField("Description", StringValidator(), "description", str)
        # self.itemID =

    def toDict(self) -> dict:
        return {
            self.itemName.toDict(),
            self.itemDescription.toDict(),
        }

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        return [self.itemName.validate(), self.itemDescription.validate()]
