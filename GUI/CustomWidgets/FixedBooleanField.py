from typing import Union

from PyQt6.QtWidgets import QWidget

from GUI.JsonSerializable import JsonSerializable, CustomWidget
from GUI.Validators.Validator import ValidationResult


class FixedBooleanField(QWidget, JsonSerializable, CustomWidget):
    def __init__(self, fieldName: str, ):
        super().__init__()

    def toDict(self) -> dict:
        pass

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        pass
