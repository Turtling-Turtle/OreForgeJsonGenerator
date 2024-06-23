from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QCheckBox, QHBoxLayout

from GUI.JsonSerializable import JsonSerializable, CustomWidget
from GUI.Validators.Validator import ValidationResult
from Helper_Functions import bold_string


def setToolTip(widget: QWidget, toolTip: str):
    widget.setToolTip(toolTip)


class CheckBoxField(QWidget, JsonSerializable, CustomWidget):
    def __init__(self, fieldName: str, keyName: str):
        QWidget.__init__(self)
        CustomWidget.__init__(self, fieldName, keyName, valueType=bool)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(bold_string(fieldName))
        self.label.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.label)

        self.checkBox = QCheckBox()
        self.layout.addWidget(self.checkBox)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

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
