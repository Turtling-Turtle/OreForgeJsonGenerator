from typing import Union

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QComboBox

from GUI.JsonSerializable import JsonSerializable
from GUI.Validators.Validator import ValidationResult, Validator
from Helper_Functions import bold_string


class DropDownMenu(QWidget, JsonSerializable):
    """
    A DropDownMenu takes a list of Tuples.
    [0] is the display name of the element.
    [1] is the valueName of the element.
    """

    def __init__(self, fieldName: str, validator: Validator, keyName: str, content: list[tuple[str, str]]):
        super().__init__(fieldName, validator, keyName)
        self.label = QLabel(bold_string(fieldName))
        self.label.setFont(QFont("Arial", 14))

        self.dropDown = QComboBox()
        self.options = content
        for element in self.options:
            self.dropDown.addItem(element[0])

    def toDict(self) -> dict:
        for option in self.options:
            if option[0] == self.dropDown.currentText():
                return {self.keyName: option[1]}

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        return ValidationResult()

    def setLabelToolTip(self, toolTip: str):
        self.label.setToolTip(toolTip)
        return self

    def setDropDownToolTip(self, toolTip: str):
        self.dropDown.setToolTip(toolTip)
        return self
