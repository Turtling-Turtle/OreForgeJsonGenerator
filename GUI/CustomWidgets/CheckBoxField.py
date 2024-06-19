from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QCheckBox

from GUI.JsonSerializable import JsonSerializable
from GUI.Validators.Validator import ValidationResult, Validator
from Helper_Functions import bold_string


def setToolTip(widget: QWidget, toolTip: str):
    widget.setToolTip(toolTip)


class CheckBoxField(QWidget, JsonSerializable):
    def __init__(self, fieldName: str, validator: Validator, keyName: str):
        super().__init__(fieldName, validator, keyName, bool)
        self.label = QLabel(bold_string(fieldName))
        self.label.setFont(QFont("Arial", 14))

        self.checkBox = QCheckBox()

    def toDict(self) -> dict:
        return {self.keyName: bool(self.checkBox.isChecked())}

    def validate(self) -> ValidationResult:
        return ValidationResult()

    def setLabelToolTip(self, toolTip: str):
        self.label.setToolTip(toolTip)
        return self

    def setCheckBoxToolTip(self, toolTip: str):
        self.checkBox.setToolTip(toolTip)
        return self
