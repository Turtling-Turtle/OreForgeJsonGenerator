from typing import Union

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout

from GUI.JsonSerializable import JsonSerializable, CustomWidget
from Helper_Functions import bold_string
from GUI.Validators.Validator import ValidationResult, Validator


class InputField(QWidget, JsonSerializable, CustomWidget):

    def __init__(self, fieldName: str, validator: Validator, keyName: str, valueType: type):
        QWidget.__init__(self)
        CustomWidget.__init__(self, fieldName, keyName, validator=validator, valueType=valueType)
        if valueType not in (int, float, str):
            raise ValueError(f'Value type {valueType} is not supported')
        self.layout = QHBoxLayout()

        self.label = QLabel(bold_string(fieldName + ":"))
        self.label.setFont(QFont("Arial", 14))
        self.lineEdit = QLineEdit()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineEdit)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)

    def toDict(self) -> dict:
        return {self.keyName: self.valueType(self.lineEdit.text())}

    def validate(self) -> ValidationResult:
        return self.validator.validate(self.lineEdit.text())

    def getValue(self) -> Union[int, float, str, bool]:
        return self.valueType(self.lineEdit.text())

    def configureLabelFont(self, fontInfo: QFont):
        self.label.setFont(fontInfo)
        return self

    def setLabelToolTip(self, toolTip: str):
        self.label.setToolTip(toolTip)
        return self

    def setLineEditToolTip(self, toolTip: str):
        self.lineEdit.setToolTip(toolTip)
        return self
