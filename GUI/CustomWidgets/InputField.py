from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit

from GUI.JsonSerializable import JsonSerializable
from Helper_Functions import bold_string
from GUI.Validators.Validator import ValidationResult, Validator


class InputField(QWidget, JsonSerializable):

    def __init__(self, fieldName: str, validator: Validator, keyName: str, valueType: type):
        super().__init__(fieldName, validator, keyName, valueType)
        if valueType not in (int, float, str):
            raise ValueError(f'Value type {valueType} is not supported')
        self.label = QLabel(bold_string(fieldName + ":"))
        self.label.setFont(QFont("Arial", 14))
        self.lineEdit = QLineEdit()

    def toDict(self) -> dict:
        return {self.keyName: self.valueType(self.lineEdit.text())}

    def validate(self) -> ValidationResult:
        return self.validator.validate(self.lineEdit.text())

    def configureLabelFont(self, fontInfo: QFont):
        self.label.setFont(fontInfo)
        return self

    def setLabelToolTip(self, toolTip: str):
        self.label.setToolTip(toolTip)
        return self

    def setLineEditToolTip(self, toolTip: str):
        self.lineEdit.setToolTip(toolTip)
        return self
